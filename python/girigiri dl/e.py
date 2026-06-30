import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event
from urllib.parse import urlparse, parse_qs, urljoin
from playwright.sync_api import sync_playwright

import utils

# ==================== 1. 用 Playwright 逐集擷取真實位置（m3u8 或 mp4） ====================
#
# 想法：
# 列表頁(.anthology-list-box a) 上每一個 <span> 對應一個 <a href="/playGV19474-1-N/">。
# 直接用 span 文字猜測檔名(如 "SP01")常常對不上 CDN 上真正的資料夾名稱
# (如 "TakeOnMeSP01")，所以改成「真的去逐一打開每一集的頁面」，
# 攔截該頁觸發的 atom.php 請求，從它的 url= 參數還原出真正的位置。
#
# atom.php 的 url= 參數有兩種可能：
#   - 結尾是 playlist.m3u8 -> 走 utils.download_m3u8_task（ffmpeg 串流）
#   - 結尾是 .mp4          -> 走 utils.download_mp4_task（HTTP Range 分塊）
# 程式會自動判斷該用哪一種方式下載，兩種可以混在同一份清單裡。

LIST_PAGE_URL = "https://ani.girigirilove.com/playGV22116-1-1/"


def get_episode_links(page, list_page_url):
    """取得列表頁上每一個 [標籤文字, 該集頁面網址] 的對應"""
    page.goto(list_page_url)
    page.wait_for_timeout(1000)
    items = page.eval_on_selector_all(
        ".anthology-list-box a",
        """els => els.map(el => ({
            label: (el.querySelector('span') || el).textContent.trim(),
            href: el.getAttribute('href')
        }))"""
    )
    return [(it["label"], urljoin(list_page_url, it["href"])) for it in items if it["href"]]


def get_real_media_url(page, episode_page_url, wait_ms=6000):
    """打開單集頁面，攔截 atom.php 請求，回傳其 url= 參數（真正的 m3u8 或 mp4 網址）"""
    found = {"value": None}

    def on_request(request):
        if found["value"]:
            return
        if "atom.php" in request.url:
            qs = parse_qs(urlparse(request.url).query)
            real_url = qs.get("url", [None])[0]
            if real_url:
                found["value"] = real_url

    page.on("request", on_request)
    try:
        page.goto(episode_page_url)
        page.wait_for_timeout(wait_ms)
    finally:
        page.remove_listener("request", on_request)
    return found["value"]


def media_type_of(real_url: str) -> str:
    clean = real_url.split('?')[0]
    if clean.endswith(".mp4"):
        return "mp4"
    return "m3u8"  # 預設視為 m3u8 串流


def item_name_from_url(real_url):
    """從網址路徑取出該集在 CDN 上真正的資料夾/檔案名稱
       e.g. .../TakeOnMeSP01/playlist.m3u8 -> TakeOnMeSP01
            .../TakeOnMeSP01.mp4          -> TakeOnMeSP01"""
    path = urlparse(real_url).path
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    if parts[-1] == "playlist.m3u8" and len(parts) >= 2:
        return parts[-2]
    return os.path.splitext(parts[-1])[0]


def collect_episodes(list_page_url):
    """主流程：回傳 [{label, item_name, media_type, real_url}, ...]"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        links = get_episode_links(page, list_page_url)
        print(f"📋 共偵測到 {len(links)} 集連結")

        for label, episode_url in links:
            print(f"🔎 [{label}] 訪問 {episode_url} 取得真實位置 ...")
            real_url = get_real_media_url(page, episode_url)
            if not real_url:
                print(f"⚠️ [{label}] 沒有攔截到 atom.php 的 url 參數，跳過")
                continue
            mtype = media_type_of(real_url)
            item_name = item_name_from_url(real_url)
            print(f"✅ [{label}] 真實位置({mtype}): {real_url}  (item_name={item_name})")
            results.append({"label": label, "item_name": item_name,
                            "media_type": mtype, "real_url": real_url})

        browser.close()
    return results


episodes = collect_episodes(LIST_PAGE_URL)
if not episodes:
    print("❌ 沒有任何一集成功取得真實位置")
    sys.exit(1)

# ==================== 2. 初始化配置 ====================

sample_path = urlparse(episodes[0]["real_url"]).path
output_folder = sample_path.rstrip('/').split('/')[-2]
total_episodes = len(episodes)
max_workers = 10

os.makedirs(output_folder, exist_ok=True)

processes_lock = Lock()
active_processes = []
stop_event = Event()

# ---- 檔名去重複：用 (前綴類型, 顯示名稱) 當 key，重複的話自動加上 _2 / _3 ... ----
_name_seen_lock = Lock()
_name_seen = {}

def make_display_name(prefix_type, display_name):
    key = f"{prefix_type}{display_name}"
    with _name_seen_lock:
        _name_seen[key] = _name_seen.get(key, 0) + 1
        n = _name_seen[key]
    if n == 1:
        return display_name
    # 第二次起出現同名，附加序號避免覆蓋檔案
    return f"{display_name}_{n}"

# ==================== 3. 下載函數 ====================

def download_episode(ep, line_num):
    label = ep["label"]
    real_url = ep["real_url"]
    media_type = ep["media_type"]

    prefix_type = 'EP' if utils.is_number(label) else 'SP'
    raw_display_name = label[2:] if label.upper().startswith("SP") else label
    display_name = make_display_name(prefix_type, raw_display_name)

    prefix = utils.make_prefix(f"[{prefix_type}{display_name}]")
    output_file = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{display_name}].mp4")
    xml_file = os.path.join(output_folder, f"{output_folder} [{prefix_type}][{display_name}].xml")

    if media_type == "mp4":
        base_url = real_url.rsplit('/', 1)[0] + '/'
        base_name = os.path.basename(base_url.strip('/'))
        danmu_info = {
            "video_base_url": base_url,
            "base_name": base_name,
            "item_name": ep["item_name"],
            "display_label": f"{prefix_type}{display_name}",
            "save_dir": output_folder,
        }
        utils.download_mp4_task(real_url, output_file, prefix, line_num, stop_event,
                                 danmu_info=danmu_info, xml_before=True)
    else:
        utils.download_m3u8_task(real_url, output_file, xml_file, prefix, line_num,
                                  stop_event, active_processes, processes_lock)

# ==================== 4. 主程序 ====================

def main():
    print(f"\n🎬 共 {total_episodes} 集")
    print(f"📁 儲存路徑: {output_folder}\n")

    sys.stdout.write("\n" * total_episodes)
    utils.move_cursor_up(total_episodes)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        for idx, ep in enumerate(episodes):
            executor.submit(download_episode, ep, idx)
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
