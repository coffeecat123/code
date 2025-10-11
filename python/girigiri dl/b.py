import os
import sys
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
import time 
from urllib.parse import urlparse, unquote 

# ==================================
# 設定 (無變動)
# ==================================
url = "https://love.girigirilove.net/zijian/anime/2024/09/0928/OreNoImoto/" 
if not url.endswith('/'):
    url += '/'
    
base_url_template = url + "{:02d}/playlist.m3u8" 

path = urlparse(url).path
output_folder = os.path.split(path.rstrip('/'))[1] 

# === 核心修改: 新的下載列表結構 ===
dl={
    "ep":range(1,1+1),    # EP01~EP15 (標準集數)
    "sp":range(1,1+1),    # SP01~SP16 (特別篇)
    "ep_5":[12.5],         # EP12.5 (半集)
    "sp_5":[12.5]          # SP12.5 (特別篇半集)
}

# 將所有下載項目扁平化為一個列表，用於計算 total_episodes 和分配行號
# 每個元素是 (item_type, item_number)
download_items = []
for item_type, items in dl.items():
    for item in items:
        download_items.append((item_type, item))

total_episodes = len(download_items)
max_workers = 10  # 限制最大並行下載數量，避免過多連接，可以調整
# =======================================

# --------------------
os.makedirs(output_folder, exist_ok=True)
# --------------------
# 執行緒安全與程序管理 (無變動)
print_lock = Lock()
processes_lock = Lock()
active_processes = []
stop_event = Event()
# --------------------

# --------------------
# 輔助函式 (內容無變動)

def check_ffprobe():
    """檢查 ffprobe 是否安裝並可用"""
    try:
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

FFPROBE_AVAILABLE = check_ffprobe()
duration_cache = {} 

def get_duration(m3u8_url):
    """使用 ffprobe 獲取 m3u8 的總時長（秒），並使用快取"""
    if m3u8_url in duration_cache:
        return duration_cache[m3u8_url]
    if not FFPROBE_AVAILABLE:
        return None
    try:
        command = [
            "ffprobe", "-v", "error", "-i", m3u8_url,
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1"
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        duration = float(result.stdout.strip())
        duration_cache[m3u8_url] = duration
        return duration
    except (subprocess.CalledProcessError, ValueError, IndexError):
        return None

def time_to_seconds(time_str):
    """將 FFmpeg 輸出的 time 格式 HH:MM:SS.ms 轉換為秒數"""
    try:
        parts = re.split(r'[:.]', time_str)
        if len(parts) >= 3:
            h = int(parts[-4]) if len(parts) >= 4 else 0
            m = int(parts[-3])
            s = int(parts[-2])
            ms_str = parts[-1]
            ms = int(ms_str) / (10 ** len(ms_str))
            return h * 3600 + m * 60 + s + ms
        return 0
    except Exception:
        return 0

def format_time(seconds):
    """將秒數轉換為 MM:SS 格式"""
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_line_progress(percent, current_time, total_duration, speed):
    """繪製線狀進度條，並包含時間和速度。 (bar_len = 50)"""
    bar_len = 50 
    filled_len = int(bar_len * percent)
    
    current_time_str = format_time(current_time)
    total_duration_str = format_time(total_duration)
    time_str = f"{current_time_str}/{total_duration_str}"
    
    if speed == 'N/A':
        speed_formatted = ' N/A ' 
    else:
        speed_formatted = f"{float(speed):5.1f}"
    if percent >= 1.0:
        bar = '=' * bar_len 
        speed_part = ""
    else:
        bar = '-' * filled_len + '>' + ' ' * (bar_len - filled_len - 1)
        if filled_len == 0:
            bar = ' ' * bar_len
        bar = bar[:bar_len]
        speed_part = f" ({speed_formatted}x)"

    percent_str = f"{percent * 100:.0f}%"
    
    return f"{percent_str:>4s} |{bar}| {time_str}{speed_part}"
# --------------------


# --------------------
# 終端機 UI 控制函式 (內容無變動)
def move_cursor_up(n):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def move_cursor_down(n):
    sys.stdout.write(f"\033[{n}B")
    sys.stdout.flush()

def clear_line():
    """用於非進度行（如完成、中止訊息）時，確保清除乾淨"""
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def print_at_line(line_num, text):
    """用於寫入完整行（通常是狀態改變或錯誤時）"""
    with print_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write(f"\033[{line_num + 1};0H")
        clear_line() 
        sys.stdout.write(text)
        sys.stdout.write("\033[u")
        sys.stdout.flush()

def print_progress_only(line_num, start_col, progress_text):
    """
    只更新行中進度條的部分，不清除行首。
    start_col: 進度條開始的列數 (從 1 開始)
    """
    PADDING_LEN = 60 
    
    with print_lock:
        sys.stdout.write("\033[s") 
        sys.stdout.write(f"\033[{line_num + 1};{start_col}H")
        sys.stdout.write(progress_text.ljust(PADDING_LEN)) 
        sys.stdout.write("\033[u")
        sys.stdout.flush()
# --------------------


def download_episode(item_type, item, line_num):
    """下載單一集數的函式 (已修改 PREFIX 確保對齊)"""
    
    # 初始化格式化字串
    # 將浮點數的點號替換為底線，以符合 URL 和檔名的慣例，並確保長度一致性
    item_str = f"{item:02d}" if isinstance(item, int) else str(item).replace('.', '_')
    raw_path_item = f"{item:02d}" if isinstance(item, int) else str(item) # URL 路徑中使用點號

    if item_type.startswith('ep'):
        # 處理標準集數和半集
        m3u8_url = f"{url}{raw_path_item}/playlist.m3u8"
        output_file = os.path.join(output_folder, f"OreNoImoto_EP{item_str}.mp4")
        RAW_PREFIX = f"[EP{raw_path_item}]" # 原始前綴 (不含空格)

    elif item_type.startswith('sp'):
        # 處理特別篇和特別篇半集
        # 檔案和 URL 使用 SP + 編號
        m3u8_url = f"{url}SP{raw_path_item}/playlist.m3u8"
        output_file = os.path.join(output_folder, f"OreNoImoto_SP{item_str}.mp4")
        RAW_PREFIX = f"[SP{raw_path_item}]" # 原始前綴 (不含空格)
    else:
        # 項目類型錯誤
        print_at_line(line_num, f"[ERROR] 未知的項目類型: {item_type}")
        return

    # ======================================================
    # === 核心修改：固定 PREFIX 寬度 (10 字元) ===
    FIXED_PREFIX_LEN = 9
    # 使用 ljust() 填充空格，確保 PREFIX 佔用固定寬度
    PREFIX = RAW_PREFIX.ljust(FIXED_PREFIX_LEN)
    # ===========================================
    
    total_duration = get_duration(m3u8_url)
    last_percent = -1 
    
    STATUS_TEXT = "🚚 下載中... " 
    
    # 計算進度條開始的列數
    # START_COL = 固定前綴長度 + 狀態文字長度 + 1 (ANSI 座標從 1 開始)
    START_COL = FIXED_PREFIX_LEN + len(STATUS_TEXT.strip())+4 + 1 

    # 將錯誤/跳過訊息中的 PREFIX 替換為固定寬度版本
    if total_duration is None:
        print_at_line(line_num, f"{PREFIX}⚠️ 無法獲取總時長 ({m3u8_url})，跳過")
        return 
    
    # === 步驟 1: 初始化行，只寫入一次前綴和狀態文字 ===
    print_at_line(line_num, f"{PREFIX}{STATUS_TEXT.strip()}") 
    
    # 立即用 print_progress_only 寫入初始進度條 (0%)
    init_progress = draw_line_progress(0, 0, total_duration, 'N/A')
    print_progress_only(line_num, START_COL, init_progress)

    time_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2}\.\d+)')
    
    if stop_event.is_set():
        # 中止訊息也使用固定寬度 PREFIX
        print_at_line(line_num, f"{PREFIX}🛑 已收到中止信號，取消任務")
        return

    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = None
    try:
        command = [
            "ffmpeg", "-v", "error", "-hide_banner", "-stats", 
            "-protocol_whitelist", "file,http,https,tcp,tls", 
            "-i", m3u8_url, "-c", "copy", "-y", output_file
        ]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8', startupinfo=startupinfo)
        with processes_lock:
            active_processes.append(process)

        # 讀取進度並解析
        for line in process.stdout:
            if stop_event.is_set():
                break 
                
            match = time_pattern.search(line)
            speed_match = re.search(r'speed=\s*(\S+)x', line)

            if total_duration and match:
                current_time_str = match.group(1)
                current_time_sec = time_to_seconds(current_time_str)
                speed = speed_match.group(1) if speed_match else 'N/A'
                
                if total_duration > 0:
                    percent = min(current_time_sec / total_duration, 1.0)
                    current_percent = int(percent * 100)
                    
                    # 只有當百分比增加時才刷新 UI
                    if current_percent > last_percent:
                        last_percent = current_percent
                        
                        progress_bar_text = draw_line_progress(percent, current_time_sec, total_duration, speed)
                        
                        # === 核心：只更新進度條部分，不閃爍前綴 ===
                        print_progress_only(line_num, START_COL, progress_bar_text)
                        
            
        process.wait()

        # 檢查是否因為被中止而退出 (用 print_at_line 覆蓋整個行)
        if stop_event.is_set():
            print_at_line(line_num, f"{PREFIX}🛑 下載被手動中止")
            return

        if process.returncode == 0:
            # 確保 100% 完成時的顯示 (用 print_at_line 覆蓋整個行，狀態文字改變)
            final_progress = draw_line_progress(1.0, total_duration, total_duration, 'N/A')
            print_at_line(line_num, f"{PREFIX}✅ 下載完成 {final_progress}")
            return
        else:
            # 下載失敗 (用 print_at_line 覆蓋整個行)
            print_at_line(line_num, f"{PREFIX}❌ 下載失敗 (Code: {process.returncode})")

    except Exception as e:
        print_at_line(line_num, f"{PREFIX}❌ 執行錯誤: {e}")
    finally:
        if process:
            with processes_lock:
                if process in active_processes:
                    active_processes.remove(process)

    if not stop_event.is_set() and process and process.returncode != 0:
        print_at_line(line_num, f"{PREFIX}🚫 下載任務失敗")


def main():
    """主執行函式 (內容無變動)"""
    sys.stdout.write("\n" * total_episodes)
    move_cursor_up(total_episodes)
    
    executor = ThreadPoolExecutor(max_workers=max_workers)

    try:
        # 遍歷扁平化後的下載項目，idx 作為行號
        for idx, (item_type, item) in enumerate(download_items):
            executor.submit(download_episode, item_type, item, idx)
        
        executor.shutdown(wait=True)

        if not stop_event.is_set():
            move_cursor_down(total_episodes) 
            clear_line() 
            print("\n🎉 所有指定項目下載完成！")
            os.system('pause') 

    except KeyboardInterrupt:
        move_cursor_down(total_episodes + 1)
        print("\n\n🚦 收到 Ctrl+C！正在中止所有下載...")
        
        stop_event.set()

        with processes_lock:
            procs_to_terminate = list(active_processes)
        
        for p in procs_to_terminate:
            try:
                p.terminate()
            except ProcessLookupError:
                pass

        executor.shutdown(wait=False, cancel_futures=True)

        print("🛑 所有下載任務已中止。")
        sys.exit(1)

if __name__ == "__main__":
    main()