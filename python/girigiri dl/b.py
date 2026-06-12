import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from urllib.parse import urlparse

import utils

# ==================== 1. 配置 ====================

url = "https://ai.girigirilove.net/zijian/oldanime/2026/04/TongariBoushinoAtelier/"
if not url.endswith('/'):
    url += '/'

path = urlparse(url).path
output_folder = os.path.split(path.rstrip('/'))[1]

dl = {
    "ep":   range(9, 12),
    "sp":   range(1, 1),
    "ep_5": [],
    "sp_5": []
}

# 扁平化下載清單：每個元素為 (item_type, item_number)
download_items = [
    (item_type, item)
    for item_type, items in dl.items()
    for item in items
]

total_episodes = len(download_items)
max_workers = 10

os.makedirs(output_folder, exist_ok=True)

processes_lock = Lock()
active_processes = []
stop_event = Event()

# ==================== 2. 下載函數 ====================

def download_episode(item_type, item, line_num):
    # 格式化集數字串
    item_str     = f"{item:02d}" if isinstance(item, int) else str(item).replace('.', '_')
    raw_path_str = f"{item:02d}" if isinstance(item, int) else str(item)

    if item_type.startswith('ep'):
        m3u8_url    = f"{url}{raw_path_str}/playlist.m3u8"
        output_file = os.path.join(output_folder, f"{output_folder} [EP][{item_str}].mp4")
        xml_file    = os.path.join(output_folder, f"{output_folder} [EP][{item_str}].xml")
        prefix      = utils.make_prefix(f"[EP{raw_path_str}]")
    elif item_type.startswith('sp'):
        m3u8_url    = f"{url}SP{raw_path_str}/playlist.m3u8"
        output_file = os.path.join(output_folder, f"{output_folder} [SP][{item_str}].mp4")
        xml_file    = os.path.join(output_folder, f"{output_folder} [SP][{item_str}].xml")
        prefix      = utils.make_prefix(f"[SP{raw_path_str}]")
    else:
        utils.print_at_line(line_num, f"[ERROR] 未知的項目類型: {item_type}")
        return

    # 修正雙斜線問題
    m3u8_url = m3u8_url.replace('//playlist.m3u8', '/playlist.m3u8')

    total_duration = utils.get_duration(m3u8_url)
    if total_duration is None:
        utils.print_at_line(line_num, f"{prefix}⚠️ 無法獲取總時長 ({m3u8_url})，跳過")
        return

    utils.download_m3u8_xml(m3u8_url, xml_file, line_num, prefix)
    utils.print_at_line(line_num, f"{prefix}{utils.STATUS_TEXT.strip()}")
    utils.print_progress_only(line_num, utils.PROGRESS_START_COL,
                               utils.draw_time_progress(0, 0, total_duration, 'N/A'))

    utils.run_ffmpeg_download(m3u8_url, output_file, prefix, line_num,
                               total_duration, stop_event, active_processes, processes_lock)

# ==================== 3. 主程序 ====================

def main():
    sys.stdout.write("\n" * total_episodes)
    utils.move_cursor_up(total_episodes)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        for idx, (item_type, item) in enumerate(download_items):
            executor.submit(download_episode, item_type, item, idx)
        executor.shutdown(wait=True)

        if not stop_event.is_set():
            utils.move_cursor_down(total_episodes)
            utils.clear_line()
            print("\n🎉 所有指定項目下載完成！")
            os.system('pause')

    except KeyboardInterrupt:
        utils.move_cursor_down(total_episodes + 1)
        print("\n\n🚦 收到 Ctrl+C！正在中止所有下載...")
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