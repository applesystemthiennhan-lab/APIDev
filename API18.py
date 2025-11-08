import os
import math
import time
import threading
from pathlib import Path

# ====== Màu ======
den = "\033[1;30m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xanhd = "\033[1;34m"
hong = "\033[1;35m"
xnhac = "\033[1;36m"
trang = "\033[1;37m"
whiteb = "\033[1;37m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'
xanhla = "\033[1;92m"
do_nhat = "\033[1;91m"
vang_nhat = "\033[1;93m"
xanhduong_sang = "\033[1;94m"
hong_nhat = "\033[1;95m"
trang_sang = "\033[1;97m"
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lamd = "\033[1;34m"
lam = "\033[1;36m"
purple = "\033[35m"  
hong = "\033[1;95m"
reset = "\033[0m"

XNHAC = "\033[38;5;117m"
XANH_DUONG = XNHAC
TRANG_SANG = "\033[97m"
LUC = "\033[92m"
VANG = "\033[93m"
VANG_NHAT = "\033[33m"
DO_NHAT = "\033[91m"
XANH_LA = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

ENC_COLORS = {
    "ASCII/UTF-8": "\033[96m",
    "UTF-16LE": "\033[93m",
    "GAPPED": "\033[95m",
}


def APIScanReplace():
    def find_all_in_bytes(data: bytes, sub: bytes, start=0):
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

    def colored_prompt(desc: str):
        print(f"\n{XANH_DUONG}APIScan :{RESET} {trang_sang}{desc}{RESET}")
        return input(f"{XNHAC}> {RESET}")

    # ==== Start ====
    fn = colored_prompt("Nhập Tên File (mặc định: file.dylib):").strip() or "file.dylib"
    p = Path(fn)
    if not p.exists():
        print(f"{DO_NHAT}File không tồn tại:{RESET} {trang_sang}{fn}{RESET}")
        return

    word = colored_prompt("Nhập Từ Cần Scan :").strip()
    if not word:
        print(f"{DO_NHAT}Không có từ cần scan.{RESET}")
        return

    print(f"\n{VANG_NHAT}APIScan : {trang_sang}Đang load file...{RESET}")
    data = p.read_bytes()
    file_size = len(data)

    encodings = {
        "ASCII/UTF-8": word.encode("utf-8", errors="ignore"),
        "UTF-16LE": to_utf16le(word),
        "GAPPED": make_gapped_bytes(word),
    }

    progress_lock = threading.Lock()
    bytes_scanned = 0
    is_scanning = True

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
        print("\r" + " " * 120 + "\r", end="", flush=True)

    def scan_worker(pattern: bytes, start: int, end: int, out_list: list, overlap: int):
        nonlocal bytes_scanned
        s = max(0, start - overlap)
        e = min(file_size, end + overlap)
        segment = data[s:e]
        for off in find_all_in_bytes(segment, pattern):
            real_off = s + off
            if start <= real_off < end:
                out_list.append(real_off)
        with progress_lock:
            bytes_scanned += (end - start)

    num_threads = min(8, max(2, (threading.active_count() + 4)))
    found_entries = []
    loader_thread = threading.Thread(target=loader, daemon=True)
    loader_thread.start()

    try:
        for enc_name, pattern in encodings.items():
            if not pattern:
                continue
            chunk_count = num_threads
            chunk_size = math.ceil(file_size / chunk_count)
            overlap = max(1, len(pattern) - 1)
            offsets_collected = []
            local_threads = []
            for i in range(chunk_count):
                start = i * chunk_size
                end = min(file_size, (i + 1) * chunk_size)
                t = threading.Thread(target=scan_worker, args=(pattern, start, end, offsets_collected, overlap))
                t.start()
                local_threads.append(t)
            for t in local_threads:
                t.join()
            offsets_collected = sorted(set(offsets_collected))
            for o in offsets_collected:
                found_entries.append((enc_name, o, pattern))
    finally:
        is_scanning = False
        loader_thread.join()

    if not found_entries:
        print(f"\n{DO_NHAT}APIScan : {trang_sang}Không tìm thấy kết quả.{RESET}")
        return
    else:
        print(f"\n{XANH_LA}APIScan : {trang_sang}Đã Scan Ra Kết Quả ✅{RESET}")

    # === Hiển thị kết quả ===
    def preview_bytes_at(off, length=32):
        window = data[off:off + length]
        try:
            txt = window.decode('utf-8', errors='replace')
        except:
            txt = ''.join([f"\\x{b:02x}" for b in window[:length]])
        return txt.replace("\n", "\\n").replace("\r", "\\r")[:64]

    header = f"{trang_sang}{'Encoding':<12} │ {'Offset(HEX)':<12} │ {'Offset(DEC)':<12} │ {'Preview':<40}{RESET}"
    print(header)
    print("-" * 85)
    found_entries_sorted = sorted(found_entries, key=lambda x: x[1])
    for enc_name, off, oldb in found_entries_sorted:
        color = ENC_COLORS.get(enc_name, trang_sang)
        hex_off = f"0x{off:08x}"
        dec_off = str(off)
        preview = preview_bytes_at(off)
        print(f"{color}{enc_name:<12}{RESET} │ {trang_sang}{hex_off:<12}{RESET} │ {trang_sang}{dec_off:<12}{RESET} │ {trang_sang}{preview:<40}{RESET}")


# ==== Chạy thử ====
if __name__ == "__main__":
    APIScanReplace()
