import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from urllib.parse import urlparse, parse_qs
import requests
from playwright.sync_api import sync_playwright

import utils

# ==================== 1. 用 Playwright 抓取 M3U8 網址與集數列表 ====================

page_url = "https://ani.girigirilove.com/playGV788-1-1/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    m3u8_urls = []

    def log_request(request):
        if "playlist.m3u8" in request.url:
            m3u8_urls.append(request.url)
            print("找到 M3U8 請求:", request.url)

    page.on("request", log_request)
    page.goto(page_url)
    page.wait_for_timeout(5000)

    spans = page.eval_on_selector_all(
        ".anthology-list-box span",
        "elements => elements.map(el => el.textContent.trim())"
    )
    print(spans)

    if m3u8_urls:
        url = ""
        for m3u8_url in m3u8_urls:
            extracted_url = parse_qs(urlparse(m3u8_url).query).get("url", [""])[0]
            if extracted_url:
                url = "/".join(extracted_url.split("/")[:-2]) + "/"
                print(f"✅ 成功從參數提取 URL: {url}")
                break
        if not url:
            url = "/".join(m3u8_urls[0].split("/")[:-2]) + "/"
            print(f"⚠️ 沒找到參數，使用原始第一條網址: {url}")
    else:
        print("❌ 沒有捕到 playlist.m3u8 請求")
        browser.close()
        sys.exit()

    browser.close()

# ==================== 2. 初始化配置 ====================

path = urlparse(url).path
output_folder = os.path.split(path.rstrip('/'))[1]
total_episodes = len(spans)
max_workers = 10

os.makedirs(output_folder, exist_ok=True)

processes_lock = Lock()
active_processes = []
stop_event = Event()

# ==================== 3. 下載函數 ====================

def download_episode(item_name, line_num):
    prefix_type = 'EP' if utils.is_number(item_name) else 'SP'
    display_name = item_name[2:] if item_name.startswith("SP") else item_name
    prefix = utils.make_prefix(f"[{prefix_type}{display_name}]")

    m3u8_url  = f"{url}{item_name}/playlist.m3u8"
    output_file = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{display_name}].mp4")
    xml_file    = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{display_name}].xml")

    total_duration = utils.get_duration(m3u8_url)
    if total_duration is None:
        utils.print_at_line(line_num, f"{prefix}⚠️ 無法獲取總時長，跳過")
        return

    utils.download_m3u8_xml(m3u8_url, xml_file, line_num, prefix)
    utils.print_at_line(line_num, f"{prefix}{utils.STATUS_TEXT.strip()}")
    utils.print_progress_only(line_num, utils.PROGRESS_START_COL,
                               utils.draw_time_progress(0, 0, total_duration, 'N/A'))

    utils.run_ffmpeg_download(m3u8_url, output_file, prefix, line_num,
                               total_duration, stop_event, active_processes, processes_lock)

# ==================== 4. 主程序 ====================

def main():
    sys.stdout.write("\n" * total_episodes)
    utils.move_cursor_up(total_episodes)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        for idx, item_name in enumerate(spans):
            executor.submit(download_episode, item_name, idx)
        executor.shutdown(wait=True)

        if not stop_event.is_set():
            utils.move_cursor_down(total_episodes)
            utils.clear_line()
            print("\n🎉 所有指定項目下載完成！")
            os.system('pause')

    except KeyboardInterrupt:
        utils.move_cursor_down(total_episodes + 1)
        print("\n\n🚦 收到 Ctrl+C，正在中止所有下載...")
        stop_event.set()
        with processes_lock:
            procs = list(active_processes)
        for p in procs:
            try:
                p.terminate()
            except ProcessLookupError:
                pass
        executor.shutdown(wait=False, cancel_futures=True)
        print("🛑 所有下載任務已中止。")
        sys.exit(1)

if __name__ == "__main__":
    main()