    def find_all_in_bytes(data: bytes, sub: bytes, start=0):
        """Yield all offsets of sub in data using bytes.find repeatedly (fast)."""
        i = data.find(sub, start)
        while i != -1:
            yield i
            i = data.find(sub, i + 1)

    def to_utf16le(s: str) -> bytes:
        return s.encode('utf-16le', errors='ignore')

    def make_gapped_bytes(s: str) -> bytes:
        b = bytearray()
        for ch in s:
            enc = ch.encode('utf-8', errors='ignore')
            for byte in enc:
                b.append(byte)
                b.append(0)
        return bytes(b)

    
    def colored_prompt(prefix: str, desc: str):
        
    
        print(f"\n{XANH_DUONG}APIScan :{RESET} {trang_sang}{desc}{RESET}")
        return input(f"{XNHAC}> {RESET}")

    # start
    fn = colored_prompt("APIScan :", "Nhập Tên File (mặc định: file.dylib):").strip() or "file.dylib"
    p = Path(fn)
    if not p.exists():
        print(f"{DO_NHAT}File không tồn tại:{RESET} {trang_sang}{fn}{RESET}")
        return

    word = colored_prompt("APIScan :", "Nhập Từ Cần Scan :").strip()
    if not word:
        print(f"{DO_NHAT}Không có từ cần scan.{RESET}")
        return

    # read file bytes
    print(f"\n{VANG_NHAT}APIScan : {trang_sang}Đang load file...{RESET}")
    data = p.read_bytes()
    file_size = len(data)

    # prepare patterns (respect encoding)
    encodings = {
        "ASCII/UTF-8": word.encode("utf-8", errors="ignore"),
        "UTF-16LE": to_utf16le(word),
        "GAPPED": make_gapped_bytes(word),
    }

    # Progress state
    progress_lock = threading.Lock()
    bytes_scanned = 0
    is_scanning = True

    # spinner/loading animation in separate thread
    def loader():
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        idx = 0
        while is_scanning:
            with progress_lock:
                scanned = bytes_scanned
            pct = (scanned / file_size * 100) if file_size else 100
            bar_len = 30
            filled = int(bar_len * pct / 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r{XNHAC}{spinner[idx%len(spinner)]}{RESET} {trang_sang}[{bar}] {pct:5.1f}%  {trang_sang}{scanned}/{file_size} bytes{RESET}", end="", flush=True)
            idx += 1
            time.sleep(0.12)
        # clear line after finishing
        print("\r" + " " * 120 + "\r", end="", flush=True)

    # worker for scanning a single pattern in a range
    def scan_worker(pattern: bytes, start: int, end: int, out_list: list, overlap: int):
        nonlocal bytes_scanned
        # Ensure boundaries safe
        s = max(0, start - overlap)
        e = min(file_size, end + overlap)
        segment = data[s:e]
        # find all in this segment
        for off in find_all_in_bytes(segment, pattern):
            real_off = s + off
            # include only offsets that lie inside [start, end)
            if start <= real_off < end:
                out_list.append(real_off)
        # update progress
        with progress_lock:
            bytes_scanned += (end - start)

    # Orchestrate multithreaded scan per pattern
    num_threads = min(8, max(2, (threading.active_count() + 4)))  # reasonable default
    found_entries = []  # list of tuples (encoding_name, offset, bytes)
    threads = []
    loader_thread = threading.Thread(target=loader, daemon=True)
    loader_thread.start()

    try:
        for enc_name, pattern in encodings.items():
            # small optimization: if pattern is empty, skip
            if not pattern:
                continue
            # decide chunking
            chunk_count = num_threads
            chunk_size = math.ceil(file_size / chunk_count)
            # calculate overlap to handle matches across boundary
            overlap = max(1, len(pattern) - 1)
            offsets_collected = []
            local_threads = []
            for i in range(chunk_count):
                start = i * chunk_size
                end = min(file_size, (i + 1) * chunk_size)
                t = threading.Thread(target=scan_worker, args=(pattern, start, end, offsets_collected, overlap))
                t.start()
                local_threads.append(t)
            # wait for local threads
            for t in local_threads:
                t.join()
            # store unique sorted offsets for this encoding
            offsets_collected = sorted(set(offsets_collected))
            for o in offsets_collected:
                found_entries.append((enc_name, o, pattern))
    finally:
        # scanning finished
        is_scanning = False
        loader_thread.join()

    # show results
    if not found_entries:
        print(f"\n{DO_NHAT}APIScan : {trang_sang}Không tìm thấy kết quả.{RESET}")
        return
    else:
        print(f"\n{XANH_LA}APIScan : {trang_sang}Đã Scan Ra Kết Quả ✅{RESET}")

    # Build a table-like display
    def preview_bytes_at(off, length=32):
        # attempt to decode a preview safely
        window = data[off:off + length]
        try:
            txt = window.decode('utf-8', errors='replace')
        except:
            txt = ''.join([f"\\x{b:02x}" for b in window[:length]])
        # make it printable and shorter
        return txt.replace("\n", "\\n").replace("\r", "\\r")[:64]

    # Print header
    header = f"{trang_sang}{'Encoding':<12} │ {'Offset(HEX)':<12} │ {'Offset(DEC)':<12} │ {'Preview':<40}{RESET}"
    print(header)
    print("-" * 85)
    # sort by offset
    found_entries_sorted = sorted(found_entries, key=lambda x: x[1])
    for enc_name, off, oldb in found_entries_sorted:
        color = ENC_COLORS.get(enc_name, trang_sang)
        hex_off = f"0x{off:08x}"
        dec_off = str(off)
        preview = preview_bytes_at(off)
        print(f"{color}{enc_name:<12}{RESET} │ {trang_sang}{hex_off:<12}{RESET} │ {trang_sang}{dec_off:<12}{RESET} │ {trang_sang}{preview:<40}{RESET}")

    # save results to file
    out_name = f"{p.name}.scan.txt"
    lines = []
    for enc_name, off, oldb in found_entries_sorted:
        preview = preview_bytes_at(off)
        lines.append(f"{enc_name}\t0x{off:08x}\t{off}\t{preview}")
    try:
        with open(out_name, "w", encoding="utf-8", errors="ignore") as fo:
            fo.write("\n".join(lines))
        print(f"\n{LUC}Kết quả đã lưu: {trang_sang}{out_name}{RESET}")
    except Exception as e:
        print(f"\n{DO_NHAT}Không thể lưu file kết quả: {e}{RESET}")

    # -------------------------
    # Replace (crack) flow (keeps previous behavior but improved prompts)
    print(f"\n{VANG_NHAT}APIReplace :{RESET} {trang_sang}Bạn Có Crack Không? (y/n){RESET}")
    ans = input(f"{XNHAC}> {RESET}").strip().lower()
    if ans != 'y':
        print(f"{DO_NHAT}APIReplace : Hủy thao tác thay thế.{RESET}")
        return

    default_new = "APIDevCracK"
    print(f"\n{XANH_DUONG}APIReplace :{RESET} {trang_sang}Nhập từ thay thế (mặc định: {default_new}):{RESET}")
    new_text = input(f"{XNHAC}> {RESET}").strip() or default_new

    # precompute new byte sequences per encoding
    newb_map = {}
    for kind, _, oldb in found_entries_sorted:
        if kind == "UTF-16LE":
            newb_map[kind] = new_text.encode('utf-16le', errors='ignore')
        elif kind == "GAPPED":
            nb = bytearray()
            for ch in new_text:
                for byte in ch.encode('utf-8', errors='ignore'):
                    nb.append(byte); nb.append(0)
            newb_map[kind] = bytes(nb)
        else:
            newb_map[kind] = new_text.encode('utf-8', errors='ignore')

    # check if any newb longer than oldb => ask truncate
    need_truncate = False
    for kind, off, oldb in found_entries_sorted:
        nb = newb_map.get(kind, b'')
        if len(nb) > len(oldb):
            need_truncate = True
            break

    force_truncate = False
    if need_truncate:
        print(f"\n{DO_NHAT}APIReplace :{RESET} {trang_sang}Một số vùng cũ nhỏ hơn chuỗi mới. Có muốn cắt chuỗi mới (truncate) để ghi đè? (y/N){RESET}")
        q = input(f"{XNHAC}> {RESET}").strip().lower()
        if q == 'y':
            force_truncate = True
        else:
            print(f"{DO_NHAT}APIReplace : Hủy vì chuỗi mới dài hơn vùng cũ.{RESET}")
            return

    # perform backup if not exists
    bak = p.with_suffix(p.suffix + '.bak')
    if not bak.exists():
        try:
            p.replace(bak)
        except Exception as e:
            print(f"{DO_NHAT}Không thể tạo backup: {e}{RESET}")
            return
    data_mut = bytearray(bak.read_bytes())

    replaced = 0
    # iterate from high offsets to low (so we don't corrupt earlier offsets)
    for kind, off, oldb in sorted(found_entries_sorted, key=lambda x: x[1], reverse=True):
        nb = newb_map.get(kind, b'')
        # double-check current bytes still match original found pattern
        if data_mut[off:off + len(oldb)] != oldb:
            # skip mismatch
            continue

        if len(nb) <= len(oldb):
            pad = b'\x00' * (len(oldb) - len(nb))
            data_mut[off:off + len(oldb)] = nb + pad
            replaced += 1
        else:
            if force_truncate:
                data_mut[off:off + len(oldb)] = nb[:len(oldb)]
                replaced += 1
            else:
                continue

    if replaced:
        try:
            p.write_bytes(bytes(data_mut))
            print(f"\n{LUC}APIReplace : Đã Crack Xong — Đã thay {replaced} vị trí. Backup: {bak.name}{RESET}")
        except Exception as e:
            print(f"\n{DO_NHAT}APIReplace : Lỗi khi ghi file: {e}{RESET}")
    else:
        print(f"\n{DO_NHAT}APIReplace : Không có vị trí nào được thay thế.{RESET}")
