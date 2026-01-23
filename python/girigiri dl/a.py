import os
import sys
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from urllib.parse import urlparse, parse_qs 
import requests
from playwright.sync_api import sync_playwright

page_url = "https://bgm.girigirilove.com/playGV856-1-1/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    m3u8_urls = []

    def log_request(request):
        url = request.url
        if "playlist.m3u8" in url:
            m3u8_urls.append(url)
            print("找到 M3U8 請求:", url)

    page.on("request", log_request)
    page.goto(page_url)
    page.wait_for_timeout(5000)

    spans = page.eval_on_selector_all(
        ".anthology-list-box span",
        "elements => elements.map(el => el.textContent.trim())"
    )
    print(spans)

    if m3u8_urls:
        for m3u8_url in m3u8_urls:
            parsed = urlparse(m3u8_url)
            query_params = parse_qs(parsed.query)
            real_url = query_params.get("url", [""])[0]
            url = "/".join(real_url.split("/")[:-2]) + "/"
            print(url)
    else:
        print("沒有捕到 playlist.m3u8 請求")

    browser.close()

# 初始化配置
path = urlparse(url).path
output_folder = os.path.split(path.rstrip('/'))[1] 

XML_API_URL = "https://m3u8.girigirilove.com/api.php/Scrolling/getVodOutScrolling" 
total_episodes = len(spans)
max_workers = 10

os.makedirs(output_folder, exist_ok=True)

# 線程安全與程序管理
print_lock = Lock()
processes_lock = Lock()
active_processes = []
stop_event = Event()

# ==================== 輔助函數 ====================

def check_ffprobe():
    """檢查 ffprobe 是否安裝"""
    try:
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

FFPROBE_AVAILABLE = check_ffprobe()
duration_cache = {}

def download_xml(m3u8_url, xml_output_file, line_num, prefix):
    """下載 XML 文件"""
    try:
        payload = {"play_url": m3u8_url}
        headers = {'Content-Type': 'application/json'}
        
        print_at_line(line_num, f"{prefix}🔍 正在獲取 XML 資訊...")

        response = requests.post(XML_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        if data.get('code') != 1:
            print_at_line(line_num, f"{prefix}❌ XML API 失敗: {data.get('msg', '未知錯誤')}")
            return False

        xml_url = data['info']
        
        print_at_line(line_num, f"{prefix}📥 正在下載 XML 文件...")
        xml_response = requests.get(xml_url, timeout=10)
        xml_response.raise_for_status()

        with open(xml_output_file, 'wb') as f:
            f.write(xml_response.content)
            
        print_at_line(line_num, f"{prefix}📄 XML 文件下載完成.")
        return True

    except requests.exceptions.RequestException as e:
        print_at_line(line_num, f"{prefix}❌ 請求 XML 失敗: {e}")
        return False
    except Exception as e:
        print_at_line(line_num, f"{prefix}❌ 處理 XML 錯誤: {e}")
        return False

def get_duration(m3u8_url):
    """使用 ffprobe 獲取 m3u8 的總時長（秒）"""
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
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True, check=True)
        duration = float(result.stdout.strip())
        duration_cache[m3u8_url] = duration
        return duration
    except (subprocess.CalledProcessError, ValueError):
        return None

def time_to_seconds(time_str):
    """將 HH:MM:SS.ms 轉換為秒數"""
    try:
        parts = re.split(r'[:.]', time_str)
        h = int(parts[-4]) if len(parts) >= 4 else 0
        m = int(parts[-3])
        s = int(parts[-2])
        ms = int(parts[-1]) / (10 ** len(parts[-1]))
        return h * 3600 + m * 60 + s + ms
    except Exception:
        return 0

def format_time(seconds):
    """將秒數轉換為 MM:SS 格式"""
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_line_progress(percent, current_time, total_duration, speed):
    """繪製進度條，包含時間和速度"""
    bar_len = 50 
    filled_len = int(bar_len * percent)
    
    current_time_str = format_time(current_time)
    total_duration_str = format_time(total_duration)
    time_str = f"{current_time_str}/{total_duration_str}"
    
    speed_formatted = f"{float(speed):5.1f}" if speed != 'N/A' else ' N/A '
    
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

# ==================== 終端 UI 控制函數 ====================

def move_cursor_up(n):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def move_cursor_down(n):
    sys.stdout.write(f"\033[{n}B")
    sys.stdout.flush()

def clear_line():
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def print_at_line(line_num, text):
    """在指定行寫入完整行"""
    with print_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write(f"\033[{line_num + 1};0H")
        clear_line() 
        sys.stdout.write(text)
        sys.stdout.write("\033[u")
        sys.stdout.flush()

def print_progress_only(line_num, start_col, progress_text):
    """只更新進度條部分"""
    padding_len = 60 
    
    with print_lock:
        sys.stdout.write("\033[s") 
        sys.stdout.write(f"\033[{line_num + 1};{start_col}H")
        sys.stdout.write(progress_text.ljust(padding_len)) 
        sys.stdout.write("\033[u")
        sys.stdout.flush()
def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
# ==================== 下載函數 ====================

def download_episode(item_name, line_num):
    """下載單一集數"""
    prefix_type = 'EP' if is_number(item_name) else 'SP'
    display_name = item_name
    if display_name.startswith("SP"):
        display_name = display_name[2:] 
        pass
    
    raw_prefix = f"[{prefix_type}{display_name}]"
    prefix = raw_prefix.ljust(9)

    m3u8_url = f"{url}{item_name}/playlist.m3u8"
    output_file = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{item_name}].mp4")
    xml_file = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{item_name}].xml")
    
    total_duration = get_duration(m3u8_url)
    if total_duration is None:
        print_at_line(line_num, f"{prefix}⚠️ 無法獲取總時長，跳過")
        return 
    
    last_percent = -1
    status_text = "🚚 下載中... "
    start_col = 9 + len(status_text.strip()) + 4 + 1
    
    download_xml(m3u8_url, xml_file, line_num, prefix)
    print_at_line(line_num, f"{prefix}{status_text.strip()}") 
    
    init_progress = draw_line_progress(0, 0, total_duration, 'N/A')
    print_progress_only(line_num, start_col, init_progress)

    time_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2}\.\d+)')
    
    if stop_event.is_set():
        print_at_line(line_num, f"{prefix}🛑 已收到中止信號，取消任務")
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
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                  universal_newlines=True, encoding='utf-8', startupinfo=startupinfo)
        with processes_lock:
            active_processes.append(process)

        for line in process.stdout:
            if stop_event.is_set():
                break 
                
            match = time_pattern.search(line)
            speed_match = re.search(r'speed=\s*(\S+)x', line)

            if match:
                current_time_sec = time_to_seconds(match.group(1))
                speed = speed_match.group(1) if speed_match else 'N/A'
                percent = min(current_time_sec / total_duration, 1.0)
                current_percent = int(percent * 100)
                
                if current_percent > last_percent:
                    last_percent = current_percent
                    progress_bar_text = draw_line_progress(percent, current_time_sec, total_duration, speed)
                    print_progress_only(line_num, start_col, progress_bar_text)
                        
        process.wait()

        if stop_event.is_set():
            print_at_line(line_num, f"{prefix}🛑 下載被手動中止")
            return

        if process.returncode == 0:
            final_progress = draw_line_progress(1.0, total_duration, total_duration, 'N/A')
            print_at_line(line_num, f"{prefix}✅ 下載完成 {final_progress}")
        else:
            print_at_line(line_num, f"{prefix}❌ 下載失敗 (Code: {process.returncode})")

    except Exception as e:
        print_at_line(line_num, f"{prefix}❌ 執行錯誤: {e}")
    finally:
        if process:
            with processes_lock:
                if process in active_processes:
                    active_processes.remove(process)

# ==================== 主程序 ====================

def main():
    """主執行函數"""
    sys.stdout.write("\n" * total_episodes)
    move_cursor_up(total_episodes)
    
    executor = ThreadPoolExecutor(max_workers=max_workers)

    try:
        for idx, item_name in enumerate(spans):
            executor.submit(download_episode, item_name, idx)
        
        executor.shutdown(wait=True)

        if not stop_event.is_set():
            move_cursor_down(total_episodes) 
            clear_line() 
            print("\n🎉 所有指定項目下載完成！")
            os.system('pause') 

    except KeyboardInterrupt:
        move_cursor_down(total_episodes + 1)
        print("\n\n🚦 收到 Ctrl+C，正在中止所有下載...")
        
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
