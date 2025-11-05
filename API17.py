    HTML_PATTERNS = [r'<!doctype', r'<html', r'<head', r'<body', r'<script', r'<div', r'<link', r'<meta']
    HTML_RE = re.compile('|'.join(HTML_PATTERNS), re.IGNORECASE)
    MIN_PRINTABLE_RUN = 4
    MAX_RESULTS = 200
    CHUNK_SIZE = 64 * 1024
    OVERLAP = 1024

    def bytes_to_printable_string(bts):
        try:
            return bts.decode('latin1', errors='replace')
        except Exception:
            return ''.join(f'\\x{c:02x}' for c in bts[:64])

    # ====== Nhập file ======
    print(f"\n{xanhduong_sang}APIScanHTM5 :{reset} {trang_sang}Nhập File Dylib Cần Scan (path):{reset}")
    filepath = input(f"{xnhac}> {reset}").strip()
    if not filepath:
        print(f"{do_nhat}APIScanHTM5 : Không có file được cung cấp.{reset}")
        return

    p = Path(filepath)
    if not p.is_file():
        print(f"{do_nhat}APIScanHTM5 : File không tồn tại: {filepath}{reset}")
        return

    file_size = p.stat().st_size
    print(f"\n{vang_nhat}APIScanHTM5 :{reset} {trang_sang}Đang chuẩn bị quét — kích thước: {file_size:,} bytes{reset}")

    # ====== Trạng thái ======
    bytes_scanned = 0
    bytes_scanned_lock = threading.Lock()
    found_lock = threading.Lock()
    found_results = []
    stop_spinner = False

    # ====== Hiển thị tiến trình ======
    def spinner_worker():
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        idx = 0
        while not stop_spinner:
            with bytes_scanned_lock:
                scanned = bytes_scanned
            pct = (scanned / file_size * 100) if file_size else 100.0
            bar_len = 30
            filled = int(bar_len * pct / 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r{xanhduong_sang}{spinner[idx % len(spinner)]}{reset} {trang_sang}[{bar}] {pct:5.1f}% {scanned:,}/{file_size:,} bytes{reset}", end='', flush=True)
            idx += 1
            time.sleep(0.1)
        print("\r" + " " * 120 + "\r", end='', flush=True)

    # ====== Hàm quét từng chunk ======
    def scan_chunk(start, end):
        nonlocal bytes_scanned
        try:
            with open(p, 'rb') as fh:
                fh.seek(max(0, start - OVERLAP))
                raw = fh.read((end - start) + OVERLAP)
        except Exception:
            with bytes_scanned_lock:
                bytes_scanned += end - start
            return

        buf = bytearray()
        local_results = []
        base_offset = max(0, start - OVERLAP)

        for i, b in enumerate(raw):
            if 32 <= b <= 126:
                buf.append(b)
            else:
                if len(buf) >= MIN_PRINTABLE_RUN:
                    run_offset = base_offset + i - len(buf)
                    if run_offset < end and (run_offset + len(buf)) > start:
                        s = bytes_to_printable_string(bytes(buf))
                        if HTML_RE.search(s):
                            local_results.append((run_offset, s))
                            if len(local_results) >= MAX_RESULTS:
                                break
                buf = bytearray()

        if len(buf) >= MIN_PRINTABLE_RUN and len(local_results) < MAX_RESULTS:
            run_offset = base_offset + len(raw) - len(buf)
            if run_offset < end:
                s = bytes_to_printable_string(bytes(buf))
                if HTML_RE.search(s):
                    local_results.append((run_offset, s))

        if local_results:
            with found_lock:
                for r in local_results:
                    if len(found_results) >= MAX_RESULTS:
                        break
                    found_results.append(r)

        with bytes_scanned_lock:
            bytes_scanned += end - start

    # ====== Chia file & khởi động quét ======
    cpu_count = max(2, (os.cpu_count() or 2))
    num_threads = min(8, cpu_count * 2)
    chunk_ranges = [(i, min(file_size, i + CHUNK_SIZE)) for i in range(0, file_size, CHUNK_SIZE)]

    spinner_t = threading.Thread(target=spinner_worker, daemon=True)
    spinner_t.start()

    threads = []
    try:
        for start, end in chunk_ranges:
            while threading.active_count() > num_threads + 2:
                time.sleep(0.01)
            t = threading.Thread(target=scan_chunk, args=(start, end))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    finally:
        stop_spinner = True
        spinner_t.join()

    # ====== Hiển thị kết quả ======
    if not found_results:
        print(f"{do_nhat}APIScanHTM5 : Không tìm thấy chuỗi HTML nào trong file.{reset}")
        out_path = p.with_name(p.name + ".apiscanned.html.txt")
        with open(out_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write("(Không tìm thấy chuỗi HTML nào trong file.)\n")
        print(f"{xanhla}APIScanHTM5 : File kết quả đã lưu:{reset} {xnhac}{out_path}{reset}")
        return

    unique = {}
    for off, s in found_results:
        unique[off] = s
    items = sorted(unique.items(), key=lambda x: x[0])

    print(f"\n{xanhduong_sang}APIScanHTM5 :{reset} {trang_sang}Kết quả tìm được ({len(items)}):{reset}")
    print(f"{trang_sang}{'No.':<4} {'Offset(HEX)':<12} {'Offset(DEC)':<12} {'Preview':<80}{reset}")
    print(f"{xanhduong_sang}{'-'*110}{reset}")

    for i, (off, s) in enumerate(items[:MAX_RESULTS], start=1):
        s_clean = s.replace("\n", "\\n").replace("\r", "\\r")
        if len(s_clean) > 76:
            s_clean = s_clean[:73] + "..."
        print(f"{luc}{i:<4}{reset} {vang}0x{off:08x}{reset} {trang_sang}{off:<12}{reset} {xnhac}{s_clean}{reset}")

    out_path = p.with_name(p.name + ".apiscanned.html.txt")
    with open(out_path, 'w', encoding='utf-8', errors='ignore') as fo:
        fo.write(f"Scan results for: {p}\nFound: {len(items)} matches\n\n")
        for i, (off, s) in enumerate(items[:MAX_RESULTS], start=1):
            fo.write(f"{i:02d}\t0x{off:08x}\t{off}\t{s}\n")

    print(f"\n{xanhla}APIScanHTM5 : File Code Scan Đã Được Lưu:{reset} {xnhac}{out_path}{reset}")
