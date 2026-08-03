import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event

import utils

# ==================== 1. 配置 ====================
#
# MEDIA_TYPE 決定整支腳本要用哪種下載方式：
#   "m3u8" -> 跟原本 b.py 一樣，組 {BASE_URL}{item}/playlist.m3u8，走 ffmpeg 串流下載
#   "mp4"  -> 跟原本 c.py 一樣，組 {BASE_URL}{item}.mp4，走 HTTP Range 分塊下載
#
# 兩種模式共用同一套 dl 任務清單格式 (ep / sp / ep_5 / sp_5)。

MEDIA_TYPE = ["m3u8", "mp4"][0]  # "m3u8" 或 "mp4"

BASE_URL = "https://giri.girigirilove.top/zijian/anime/2024/0424/Tamakolovestory/"
if not BASE_URL.endswith('/'):
    BASE_URL += '/'

BASE_NAME = os.path.basename(BASE_URL.rstrip('/'))
SAVE_DIR  = f"./{BASE_NAME}"
os.makedirs(SAVE_DIR, exist_ok=True)

dl = {
    "ep":   range(1, 1),   # 例: range(1, 13) 代表 EP01~EP12
    "sp":   range(1, 1),   # 例: range(1, 3)  代表 SP01~SP02
    "ep_5": [''],             # 給非整數編號用，例: ["5.5"]
    "sp_5": []
}

tasks = []
for i in dl["ep"]:   tasks.append((f"{i:02d}", f"EP{i:02d}"))
for i in dl["sp"]:   tasks.append((f"SP{i:02d}", f"SP{i:02d}"))
for i in dl["ep_5"]: tasks.append((f"{i}", f"EP{i}"))
for i in dl["sp_5"]: tasks.append((f"SP{i}", f"SP{i}"))

total_tasks = len(tasks)
max_workers = 10 if MEDIA_TYPE == "m3u8" else 3

processes_lock = Lock()
active_processes = []
stop_event = Event()

# ==================== 2. 下載函數 ====================

def download_task(item_name, display_label, line_num):
    prefix = utils.make_prefix(f"[{display_label}]")
    output_file = os.path.join(SAVE_DIR, f"{BASE_NAME} [{display_label[:2]}][{display_label[2:]}].mp4")
    xml_file    = os.path.join(SAVE_DIR, f"{BASE_NAME} [{display_label[:2]}][{display_label[2:]}].xml")

    if MEDIA_TYPE == "m3u8":
        m3u8_url = f"{BASE_URL}{item_name}/playlist.m3u8".replace('//playlist.m3u8', '/playlist.m3u8')
        utils.download_m3u8_task(m3u8_url, output_file, xml_file, prefix, line_num,
                                  stop_event, active_processes, processes_lock)

    elif MEDIA_TYPE == "mp4":
        target_url = f"{BASE_URL}{item_name}.mp4"
        danmu_info = {
            "video_base_url": BASE_URL,
            "base_name": BASE_NAME,
            "item_name": item_name,
            "display_label": display_label,
            "save_dir": SAVE_DIR,
        }
        utils.download_mp4_task(target_url, output_file, prefix, line_num, stop_event,
                                 danmu_info=danmu_info, xml_before=True)

    else:
        utils.print_at_line(line_num, f"[ERROR] 未知的 MEDIA_TYPE: {MEDIA_TYPE}")

# ==================== 3. 主程序 ====================

def main():
    if total_tasks == 0:
        print("💡 下載清單為空，請檢查 dl 字典中的 range 設定。")
        return

    print(f"🎬 已載入 {total_tasks} 個任務 (MEDIA_TYPE={MEDIA_TYPE})")
    print(f"📁 儲存路徑: {SAVE_DIR}\n")

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
            print("\n🎉 所有指定項目下載完成！")
            os.system('pause')

    except KeyboardInterrupt:
        utils.move_cursor_down(total_tasks + 1)
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