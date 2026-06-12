import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import requests

import utils

# ==================== 1. 配置與初始化 ====================

BASE_URL  = "https://ana.girigirilove.top/zijian/anime/2024/0424/TamakoMarket/"
BASE_NAME = os.path.basename(BASE_URL.strip('/'))
SAVE_DIR  = f"./{BASE_NAME}"
os.makedirs(SAVE_DIR, exist_ok=True)

dl = {
    "ep":   range(3, 4),
    "sp":   range(1, 1),
    "ep_5": [],
    "sp_5": []
}

tasks = []
for i in dl["ep"]:   tasks.append((f"{i:02d}", f"EP{i:02d}"))
for i in dl["sp"]:   tasks.append((f"SP{i:02d}", f"SP{i:02d}"))
for i in dl["ep_5"]: tasks.append((f"{i}", f"EP{i}"))
for i in dl["sp_5"]: tasks.append((f"SP{i}", f"SP{i}"))

total_tasks = len(tasks)
max_workers = 3
stop_event  = Event()

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

# ==================== 2. 下載函數 ====================

def download_task(item_name, display_label, line_num):
    prefix    = utils.make_prefix(f"[{display_label}]")
    target_url = f"{BASE_URL}{item_name}.mp4"
    save_path  = os.path.join(SAVE_DIR, f"{BASE_NAME} [{display_label[:2]}][{display_label[2:]}].mp4")

    utils.print_at_line(line_num, f"{prefix}🔍 正在建立快取連線...")

    downloaded_bytes = 0
    total_bytes      = None
    retry_count      = 0
    last_ui_update   = 0

    start_col = utils.PROGRESS_START_COL
    utils.print_at_line(line_num, f"{prefix}{utils.STATUS_TEXT.strip()}")
    utils.print_progress_only(line_num, start_col, utils.draw_size_progress(0.0, 0, None))

    with requests.Session() as session:
        session.headers.update(headers)
        with open(save_path, 'wb') as f:
            while not stop_event.is_set():
                session.headers['range'] = f"bytes={downloaded_bytes}-"
                try:
                    with session.get(target_url, stream=True, timeout=15) as r:
                        if r.status_code == 416:
                            break
                        r.raise_for_status()

                        if total_bytes is None:
                            content_range = r.headers.get('Content-Range')
                            if content_range:
                                m = re.search(r'/(\d+)', content_range)
                                if m:
                                    total_bytes = int(m.group(1))

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
                                    percent = (downloaded_bytes / total_bytes) if total_bytes else 0.0
                                    utils.print_progress_only(
                                        line_num, start_col,
                                        utils.draw_size_progress(percent, downloaded_bytes, total_bytes)
                                    )
                                    last_ui_update = now

                        retry_count = 0
                        if bytes_in_chunk == 0:
                            break

                except requests.exceptions.RequestException:
                    retry_count += 1
                    if retry_count > 5:
                        utils.print_at_line(line_num, f"{prefix}❌ 連續斷流重試失敗，跳過此集")
                        return
                    time.sleep(1.5)

    if stop_event.is_set():
        utils.print_at_line(line_num, f"{prefix}🛑 任務手動中止")
        return

    utils.print_at_line(line_num, f"{prefix}⚡ 影片完成，正在獲取彈幕 XML...")
    has_xml = utils.download_danmu_xml(BASE_URL, BASE_NAME, item_name, display_label, SAVE_DIR)

    final_total = total_bytes if total_bytes else downloaded_bytes
    success_bar = utils.draw_size_progress(1.0, final_total, final_total)
    danmu_tag   = " (含彈幕)" if has_xml else " (無彈幕)"
    utils.print_at_line(line_num, f"{prefix}✅ 下載完成{danmu_tag} {success_bar}")

# ==================== 3. 主程序 ====================

def main():
    if total_tasks == 0:
        print("💡 下載清單為空，請檢查 dl 字典中的 range 設定。")
        return

    print(f"🎬 已載入 {total_tasks} 個任務，準備進行多線程分塊並行接龍下載與彈幕同步...\n")
    sys.stdout.write("\n" * total_tasks)
    utils.move_cursor_up(total_tasks)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        for idx, (item_name, display_label) in enumerate(tasks):
            executor.submit(download_task, item_name, display_label, idx)
        executor.shutdown(wait=True)

        if not stop_event.is_set():
            utils.move_cursor_down(total_tasks)
            utils.clear_line()
            print("\n🎉 [大功告成] 所有指定集數與彈幕 XML 全部下載完畢！")

    except KeyboardInterrupt:
        utils.move_cursor_down(total_tasks + 1)
        print("\n\n🚦 偵測到手動中止指令 (Ctrl+C)，正在安全關閉所有背景線程...")
        stop_event.set()
        executor.shutdown(wait=False, cancel_futures=True)
        print("🛑 所有背景下載已安全中斷。")
        sys.exit(1)

if __name__ == "__main__":
    main()