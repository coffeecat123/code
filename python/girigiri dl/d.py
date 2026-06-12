import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from urllib.parse import urlparse, parse_qs
import requests
from playwright.sync_api import sync_playwright

import utils

# ==================== 1. Playwright 擷取 ====================

page_url = "https://ani.girigirilove.com/playGV5021-1-1/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    mp4_url = None

    def log_request(request):
        global mp4_url
        if mp4_url:
            return
        req_url = request.url
        if req_url.count('http') >= 2:
            return
        if req_url.endswith('.mp4') or ('.mp4?' in req_url):
            mp4_url = req_url.split('?')[0]
            print("✅ 找到 MP4:", mp4_url)

    page.on("request", log_request)
    page.goto(page_url)
    page.wait_for_timeout(5000)

    spans = page.eval_on_selector_all(
        ".anthology-list-box span",
        "elements => elements.map(el => el.textContent.trim())"
    )
    print("集數列表:", spans)
    browser.close()

if not mp4_url:
    print("❌ 沒有攔截到合法 MP4 請求")
    sys.exit(1)
if not spans:
    print("❌ 沒有找到集數列表")
    sys.exit(1)

# ==================== 2. 推導 BASE_URL ====================

BASE_URL  = mp4_url.rsplit('/', 1)[0] + '/'
BASE_NAME = os.path.basename(BASE_URL.strip('/'))
print(f"✅ BASE_URL: {BASE_URL}")
print(f"✅ BASE_NAME: {BASE_NAME}")

# ==================== 3. 建立任務列表 ====================

def span_to_task(t: str):
    t = t.strip()
    if t.upper().startswith("SP"):
        num = t[2:].strip()
        stem = f"SP{int(num):02d}" if num.isdigit() else f"SP{num}"
        return stem, stem
    elif utils.is_number(t):
        stem = f"{int(float(t)):02d}"
        return stem, f"EP{stem}"
    else:
        return t, f"EP{t}"

tasks       = [span_to_task(s) for s in spans]
total_tasks = len(tasks)
max_workers = 10

SAVE_DIR = f"./{BASE_NAME}"
os.makedirs(SAVE_DIR, exist_ok=True)

# stop_event：設定後所有執行緒應儘快結束
stop_event = Event()

headers = {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "i",
    "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "video",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

# ==================== 4. 下載邏輯 ====================

def download_xml_quietly(item_stem, display_label, line_num, prefix) -> bool:
    if stop_event.is_set():
        return False
    utils.print_at_line(line_num, f"{prefix}📥 正在獲取彈幕 XML...")
    try:
        return utils.download_danmu_xml(BASE_URL, BASE_NAME, item_stem, display_label, SAVE_DIR)
    except Exception:
        return False


def download_mp4(item_stem, display_label, line_num, prefix, has_xml):
    target_url = f"{BASE_URL}{item_stem}.mp4"
    save_path  = os.path.join(SAVE_DIR, f"{BASE_NAME} [{display_label[:2]}][{display_label[2:]}].mp4")

    downloaded_bytes = 0
    total_bytes      = None
    retry_count      = 0
    last_ui_update   = 0
    start_col        = utils.PROGRESS_START_COL

    utils.print_at_line(line_num, f"{prefix}{utils.STATUS_TEXT.strip()}")
    utils.print_progress_only(line_num, start_col, utils.draw_size_progress(0.0, 0, None))

    with requests.Session() as session:
        session.headers.update(headers)
        with open(save_path, 'wb') as f:
            while not stop_event.is_set():
                session.headers['range'] = f"bytes={downloaded_bytes}-"
                try:
                    # timeout=(連線超時, 讀取超時)
                    # 讀取超時設短，讓迴圈能頻繁回來檢查 stop_event
                    with session.get(target_url, stream=True,
                                     timeout=(10, 3)) as r:
                        if r.status_code == 416:
                            break
                        r.raise_for_status()

                        if total_bytes is None:
                            cr = r.headers.get('Content-Range')
                            if cr:
                                m = re.search(r'/(\d+)', cr)
                                if m:
                                    total_bytes = int(m.group(1))
                            if total_bytes is None:
                                cl = r.headers.get('Content-Length')
                                if cl:
                                    total_bytes = int(cl)

                        bytes_in_chunk = 0
                        for chunk in r.iter_content(chunk_size=128 * 1024):
                            if stop_event.is_set():
                                break
                            if chunk:
                                f.write(chunk)
                                downloaded_bytes += len(chunk)
                                bytes_in_chunk   += len(chunk)
                                now = time.time()
                                if now - last_ui_update > 0.15:
                                    pct = (downloaded_bytes / total_bytes) if total_bytes else 0.0
                                    utils.print_progress_only(
                                        line_num, start_col,
                                        utils.draw_size_progress(pct, downloaded_bytes, total_bytes)
                                    )
                                    last_ui_update = now

                        retry_count = 0
                        if bytes_in_chunk == 0:
                            break

                except requests.exceptions.Timeout:
                    # 讀取逾時：正常接龍情況，直接重試，不計入失敗次數
                    if stop_event.is_set():
                        break
                    continue

                except requests.exceptions.RequestException:
                    retry_count += 1
                    if retry_count > 5:
                        utils.print_at_line(line_num, f"{prefix}❌ 連續斷流重試失敗，跳過此集")
                        return
                    time.sleep(1.5)

    if stop_event.is_set():
        utils.print_at_line(line_num, f"{prefix}🛑 任務手動中止")
        return

    final_total = total_bytes if total_bytes else downloaded_bytes
    success_bar = utils.draw_size_progress(1.0, final_total, final_total)
    danmu_tag   = " (含彈幕)" if has_xml else " (無彈幕)"
    utils.print_at_line(line_num, f"{prefix}✅ 下載完成{danmu_tag} {success_bar}")


def download_task(item_stem, display_label, line_num):
    prefix  = utils.make_prefix(f"[{display_label}]")
    has_xml = download_xml_quietly(item_stem, display_label, line_num, prefix)
    if stop_event.is_set():
        utils.print_at_line(line_num, f"{prefix}🛑 任務手動中止")
        return
    download_mp4(item_stem, display_label, line_num, prefix, has_xml)

# ==================== 5. 主程序 ====================

def main():
    print(f"\n🎬 共 {total_tasks} 集，BASE_URL: {BASE_URL}")
    print(f"📁 儲存路徑: {SAVE_DIR}\n")

    sys.stdout.write("\n" * total_tasks)
    utils.move_cursor_up(total_tasks)

    # daemon=True：主執行緒結束時子執行緒強制跟著結束
    executor = ThreadPoolExecutor(max_workers=max_workers,
                                  thread_name_prefix="dl",
                                  initializer=None)
    futures = [
        executor.submit(download_task, item_stem, display_label, idx)
        for idx, (item_stem, display_label) in enumerate(tasks)
    ]

    try:
        # 用輪詢代替 executor.shutdown(wait=True)
        # 這樣主執行緒不會被完全阻塞，KeyboardInterrupt 能即時打進來
        while not all(f.done() for f in futures):
            time.sleep(0.2)

    except KeyboardInterrupt:
        utils.move_cursor_down(total_tasks + 1)
        print("\n\n🚦 收到 Ctrl+C，正在中止所有下載...")
        stop_event.set()
        # 不等子執行緒，直接關閉（子執行緒會靠短 timeout 自己退出）
        executor.shutdown(wait=False, cancel_futures=True)
        print("🛑 所有下載任務已中止。")
        sys.exit(1)

    executor.shutdown(wait=False)

    if not stop_event.is_set():
        utils.move_cursor_down(total_tasks)
        utils.clear_line()
        print("\n🎉 所有集數下載完成！")

if __name__ == "__main__":
    main()