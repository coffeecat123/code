import os
import re
import sys
import time
import subprocess
import threading
from threading import Lock
import requests

# ==================== 共享狀態 ====================

print_lock = Lock()
XML_API_URL = "https://m3u8.girigirilove.com/api.php/Scrolling/getVodOutScrolling"

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
# ==================== 終端游標控制 ====================

def move_cursor_up(n):
    if n > 0:
        sys.stdout.write(f"\033[{n}A")
        sys.stdout.flush()

def move_cursor_down(n):
    if n > 0:
        sys.stdout.write(f"\033[{n}B")
        sys.stdout.flush()

def clear_line():
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def print_at_line(line_num, text):
    with print_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write(f"\033[{line_num + 1};0H")
        clear_line()
        sys.stdout.write(text)
        sys.stdout.write("\033[u")
        sys.stdout.flush()

def print_progress_only(line_num, start_col, progress_text, padding_len=65):
    with print_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write(f"\033[{line_num + 1};{start_col}H")
        sys.stdout.write(progress_text.ljust(padding_len))
        sys.stdout.write("\033[u")
        sys.stdout.flush()

# ==================== 進度條繪製 ====================

def format_time(seconds):
    """將秒數轉換為 MM:SS 格式"""
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

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

def draw_time_progress(percent, current_time, total_duration, speed, bar_len=50):
    """ffmpeg 串流用：基於時間的進度條"""
    filled_len = int(bar_len * percent)
    time_str = f"{format_time(current_time)}/{format_time(total_duration)}"
    speed_formatted = f"{float(speed):5.1f}" if speed != 'N/A' else ' N/A '

    if percent >= 1.0:
        bar = '=' * bar_len
        speed_part = ""
    else:
        bar = ('-' * filled_len + '>' + ' ' * (bar_len - filled_len - 1))[:bar_len]
        if filled_len == 0:
            bar = ' ' * bar_len
        speed_part = f" ({speed_formatted}x)"

    return f"{percent * 100:.0f}%".rjust(4) + f" |{bar}| {time_str}{speed_part}"

def draw_size_progress(percent, downloaded, total, bar_len=40):
    """HTTP 分塊下載用：基於檔案大小的進度條"""
    filled_len = int(bar_len * percent)
    dl_mb = downloaded / (1024 * 1024)
    tot_mb = total / (1024 * 1024) if total else 0

    if percent >= 1.0:
        bar = '=' * bar_len
        size_str = f"{tot_mb:.1f}MB"
    else:
        bar = ('-' * filled_len + '>' + ' ' * (bar_len - filled_len - 1))[:bar_len]
        size_str = f"{dl_mb:.1f}/{tot_mb:.1f}MB" if total else f"{dl_mb:.1f}MB"

    percent_str = f"{percent * 100:.0f}%" if total else "---%"
    return f"{percent_str:>4s} |{bar}| {size_str}"

# ==================== ffprobe ====================

def check_ffprobe():
    try:
        subprocess.run(["ffprobe", "-version"], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

FFPROBE_AVAILABLE = check_ffprobe()
_duration_cache = {}

def get_duration(m3u8_url):
    """使用 ffprobe 獲取 m3u8 總時長（秒），結果會快取"""
    if m3u8_url in _duration_cache:
        return _duration_cache[m3u8_url]
    if not FFPROBE_AVAILABLE:
        return None
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-i", m3u8_url,
             "-extension_picky", "0",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, check=True
        )
        duration = float(result.stdout.strip())
        _duration_cache[m3u8_url] = duration
        return duration
    except (subprocess.CalledProcessError, ValueError):
        return None

# ==================== XML / 彈幕下載 ====================

def download_m3u8_xml(m3u8_url, xml_save_path, line_num, prefix):
    """
    透過 API 取得彈幕 XML URL 後下載存檔（用於 m3u8 串流）。
    回傳 True/False。
    """
    try:
        print_at_line(line_num, f"{prefix}🔍 正在獲取 XML 資訊...")
        resp = requests.post(XML_API_URL,
                             json={"play_url": m3u8_url},
                             headers=headers,
                             timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get('code') != 1:
            print_at_line(line_num, f"{prefix}❌ XML API 失敗: {data.get('msg', '未知錯誤')}")
            return False

        print_at_line(line_num, f"{prefix}📥 正在下載 XML 文件...")
        xml_resp = requests.get(data['info'], headers=headers, timeout=10)
        xml_resp.raise_for_status()

        with open(xml_save_path, 'wb') as f:
            f.write(xml_resp.content)

        print_at_line(line_num, f"{prefix}📄 XML 文件下載完成.")
        return True

    except requests.exceptions.RequestException as e:
        print_at_line(line_num, f"{prefix}❌ 請求 XML 失敗: {e}")
        return False
    except Exception as e:
        print_at_line(line_num, f"{prefix}❌ 處理 XML 錯誤: {e}")
        return False

def download_danmu_xml(video_base_url, base_name, item_name, display_label, save_dir):
    """
    動態抓取彈幕 XML（用於 HTTP 直連影片）：
    方案 A：直接替換網域為 danmu. 抓靜態 XML
    方案 B：備用 API 接口
    回傳 True/False。
    """
    xml_file_name = f"{base_name} [{display_label[:2]}][{display_label[2:]}].xml"
    xml_save_path = os.path.join(save_dir, xml_file_name)

    danmu_base_url = video_base_url.replace("ana.girigirilove.top", "danmu.girigirilove.top")
    direct_xml_url = f"{danmu_base_url}{item_name}.xml"

    try:
        resp = requests.get(direct_xml_url, timeout=8)
        if resp.status_code == 200 and len(resp.content) > 100:
            with open(xml_save_path, 'wb') as f:
                f.write(resp.content)
            return True
    except Exception:
        pass

    try:
        resp = requests.get(XML_API_URL,
                            params={"id": f"{base_name}_{display_label}"},
                            timeout=8)
        if resp.status_code == 200 and len(resp.content) > 100:
            with open(xml_save_path, 'wb') as f:
                f.write(resp.content)
            return True
    except Exception:
        pass

    return False

# ==================== ffmpeg 下載核心 ====================

# 固定前綴欄位寬度（UI 對齊用）
PREFIX_LEN = 9
STATUS_TEXT = "🚚 下載中... "
# start_col：前綴 + 狀態文字可見字元數 + emoji 補償 + ANSI 座標從 1 起算
PROGRESS_START_COL = PREFIX_LEN + len(STATUS_TEXT.strip()) + 4 + 1

def _run_ffmpeg_once(m3u8_url, output_file, prefix, line_num, total_duration,
                     stop_event, active_processes, processes_lock,
                     stall_timeout, req_headers):
    """單次執行 ffmpeg，內含卡死偵測看門狗。
       回傳 'ok' / 'stalled' / 'failed' / 'aborted'"""
    time_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2}\.\d+)')

    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    header_lines = "".join(f"{k}: {v}\r\n" for k, v in req_headers.items() if k.lower() != "range")

    command = [
        "ffmpeg", "-v", "error", "-hide_banner", "-stats",
        "-extension_picky", "0",
        "-user_agent", req_headers.get("user-agent", ""),
        "-headers", header_lines,
        "-rw_timeout", "15000000",  # ffmpeg 端的讀取逾時(微秒)，避免單一請求無限期等待
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", m3u8_url, "-c", "copy", "-y", output_file
    ]

    process = None
    stalled = {"flag": False}
    last_activity = {"t": time.time()}

    def watchdog():
        while True:
            if process is None or process.poll() is not None or stop_event.is_set():
                return
            if time.time() - last_activity["t"] > stall_timeout:
                stalled["flag"] = True
                try:
                    process.kill()
                except Exception:
                    pass
                return
            time.sleep(2)

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, encoding='utf-8', startupinfo=startupinfo
        )
        with processes_lock:
            active_processes.append(process)

        wd_thread = threading.Thread(target=watchdog, daemon=True)
        wd_thread.start()

        last_percent = -1
        for line in process.stdout:
            last_activity["t"] = time.time()
            if stop_event.is_set():
                try:
                    process.kill()
                except Exception:
                    pass
                break
            match = time_pattern.search(line)
            if match:
                current_sec = time_to_seconds(match.group(1))
                speed_match = re.search(r'speed=\s*(\S+)x', line)
                speed = speed_match.group(1) if speed_match else 'N/A'
                percent = min(current_sec / total_duration, 1.0)
                current_pct = int(percent * 100)
                if current_pct > last_percent:
                    last_percent = current_pct
                    bar = draw_time_progress(percent, current_sec, total_duration, speed)
                    print_progress_only(line_num, PROGRESS_START_COL, bar)

        process.wait()

        if stop_event.is_set():
            return "aborted"
        if stalled["flag"]:
            return "stalled"
        return "ok" if process.returncode == 0 else "failed"

    except Exception as e:
        print_at_line(line_num, f"{prefix}❌ 執行錯誤: {e}")
        return "failed"
    finally:
        if process:
            with processes_lock:
                if process in active_processes:
                    active_processes.remove(process)


def run_ffmpeg_download(m3u8_url, output_file, prefix, line_num,
                        total_duration, stop_event, active_processes, processes_lock,
                        request_headers=None, stall_timeout=20, max_retries=2):
    """
    執行 ffmpeg 下載並即時更新進度條，內建卡死偵測（超過 stall_timeout 秒無新進度
    就視為卡死，自動中斷並重試，最多重試 max_retries 次）。
    回傳 True（成功）/ False（失敗）/ None（被中止）。
    """
    if stop_event.is_set():
        print_at_line(line_num, f"{prefix}🛑 已收到中止信號，取消任務")
        return None

    req_headers = request_headers or headers

    attempt = 0
    while True:
        attempt += 1
        result = _run_ffmpeg_once(m3u8_url, output_file, prefix, line_num, total_duration,
                                  stop_event, active_processes, processes_lock,
                                  stall_timeout, req_headers)

        if result == "aborted":
            print_at_line(line_num, f"{prefix}🛑 下載被手動中止")
            return None

        if result == "ok":
            final_bar = draw_time_progress(1.0, total_duration, total_duration, 'N/A')
            print_at_line(line_num, f"{prefix}✅ 下載完成 {final_bar}")
            return True

        if result == "stalled" and attempt <= max_retries:
            print_at_line(line_num, f"{prefix}⏱️ 超過{stall_timeout}秒無進度，疑似卡死，重試 ({attempt}/{max_retries})...")
            continue

        if result == "stalled":
            print_at_line(line_num, f"{prefix}❌ 重試 {max_retries} 次仍卡死，放棄此集")
        else:
            print_at_line(line_num, f"{prefix}❌ 下載失敗")
        return False

# ==================== 整合下載任務（各下載腳本直接呼叫即可） ====================

def download_m3u8_task(m3u8_url, output_file, xml_file, prefix, line_num,
                        stop_event, active_processes, processes_lock):
    """
    完整下載一集 m3u8 串流：取得時長 -> 下載彈幕 XML(API版) -> ffmpeg 下載。
    回傳值同 run_ffmpeg_download：True(成功) / False(失敗或無法取得時長) / None(被中止)。
    """
    total_duration = get_duration(m3u8_url)
    if total_duration is None:
        print_at_line(line_num, f"{prefix}⚠️ 無法獲取總時長，跳過")
        return False

    download_m3u8_xml(m3u8_url, xml_file, line_num, prefix)
    print_at_line(line_num, f"{prefix}{STATUS_TEXT.strip()}")
    print_progress_only(line_num, PROGRESS_START_COL,
                         draw_time_progress(0, 0, total_duration, 'N/A'))

    return run_ffmpeg_download(m3u8_url, output_file, prefix, line_num,
                               total_duration, stop_event, active_processes, processes_lock)


def download_mp4_task(target_url, save_path, prefix, line_num, stop_event,
                       danmu_info=None, xml_before=False, request_headers=None):
    """
    完整下載一集 HTTP 直連 mp4：Range 分塊下載（支援斷流重試/續傳）+ 彈幕 XML（直連版）。

    danmu_info: dict，需含 download_danmu_xml() 的參數
                {video_base_url, base_name, item_name, display_label, save_dir}
                傳 None 則不抓彈幕。
    xml_before: True  -> 像 d.py，先抓彈幕再下載影片
                False -> 像 c.py，先下載影片再抓彈幕
    request_headers: 不指定則使用本模組預設的 headers。
    回傳 has_xml(bool)；若中途被手動中止或斷流重試失敗，回傳 None。
    """
    req_headers = request_headers or headers
    has_xml = False

    def fetch_xml():
        if not danmu_info:
            return False
        print_at_line(line_num, f"{prefix}📥 正在獲取彈幕 XML...")
        try:
            return download_danmu_xml(**danmu_info)
        except Exception:
            return False

    if xml_before:
        has_xml = fetch_xml()
        if stop_event.is_set():
            print_at_line(line_num, f"{prefix}🛑 任務手動中止")
            return None

    downloaded_bytes = 0
    total_bytes = None
    retry_count = 0
    last_ui_update = 0
    start_col = PROGRESS_START_COL

    print_at_line(line_num, f"{prefix}{STATUS_TEXT.strip()}")
    print_progress_only(line_num, start_col, draw_size_progress(0.0, 0, None))

    with requests.Session() as session:
        session.headers.update(req_headers)
        with open(save_path, 'wb') as f:
            while not stop_event.is_set():
                session.headers['range'] = f"bytes={downloaded_bytes}-"
                try:
                    with session.get(target_url, stream=True, timeout=(10, 3)) as r:
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
                                bytes_in_chunk += len(chunk)
                                now = time.time()
                                if now - last_ui_update > 0.15:
                                    pct = (downloaded_bytes / total_bytes) if total_bytes else 0.0
                                    print_progress_only(
                                        line_num, start_col,
                                        draw_size_progress(pct, downloaded_bytes, total_bytes)
                                    )
                                    last_ui_update = now

                        retry_count = 0
                        if bytes_in_chunk == 0:
                            break

                except requests.exceptions.Timeout:
                    if stop_event.is_set():
                        break
                    continue

                except requests.exceptions.RequestException:
                    retry_count += 1
                    if retry_count > 5:
                        print_at_line(line_num, f"{prefix}❌ 連續斷流重試失敗，跳過此集")
                        return None
                    time.sleep(1.5)

    if stop_event.is_set():
        print_at_line(line_num, f"{prefix}🛑 任務手動中止")
        return None

    if not xml_before:
        has_xml = fetch_xml()

    final_total = total_bytes if total_bytes else downloaded_bytes
    success_bar = draw_size_progress(1.0, final_total, final_total)
    danmu_tag = " (含彈幕)" if has_xml else " (無彈幕)"
    print_at_line(line_num, f"{prefix}✅ 下載完成{danmu_tag} {success_bar}")
    return has_xml

# ==================== 其他工具 ====================

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def make_prefix(raw: str) -> str:
    """將原始前綴字串對齊至固定寬度"""
    return raw.ljust(PREFIX_LEN)