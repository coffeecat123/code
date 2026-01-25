import requests
import os
import time
import re
from xml.sax.saxutils import escape

# ================= 配置區域 =================
# 如果有權限問題，請在此填入 Cookie
USER_COOKIE = "" 
# ===========================================

def get_season_episodes(start_sn):
    """解析劇集清單，不檢查 state"""
    url = "https://api.gamer.com.tw/anime/v1/video.php"
    params = {"videoSn": start_sn}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": USER_COOKIE
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers).json()
        data = resp.get('data', {})
        anime_info = data.get('anime', {})
        season_title = anime_info.get('title', f"Season_{start_sn}")
        
        # 取得 episodes 物件，裡面可能有 "0", "1" 等 key
        episodes_dict = anime_info.get('episodes', {})
        
        all_eps = []
        for ep in episodes_dict["0"]:
            all_eps.append({
                'sn': ep.get('videoSn'),
                'no': ep.get('episode')
            })
        
        # 依照集數編號排序
        all_eps.sort(key=lambda x: x['no'])
        return season_title, all_eps
    except Exception as e:
        print(f"解析劇集清單失敗: {e}")
        return None, []

def fetch_danmu(sn):
    """獲取單集彈幕"""
    url = "https://api.gamer.com.tw/anime/v1/danmu.php"
    params = {"videoSn": sn, "geo": "TW,HK"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"https://ani.gamer.com.tw/animeVideo.php?sn={sn}",
        "Cookie": USER_COOKIE
    }
    try:
        resp = requests.get(url, params=params, headers=headers).json()
        # 彈幕數據在 data -> danmu 之下
        return resp.get('data', {}).get('danmu', [])
    except:
        return []

def save_xml(danmu_list, sn, ep_no, folder):
    """儲存為 B 站 XML 格式，時間精確除以 1000"""
    mode_map = {0: 1, 1: 5, 2: 4}
    now_ts = int(time.time())
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<i>',
        '  <chatserver>chat.bilibili.com</chatserver>',
        f'  <chatid>{sn}</chatid>'
    ]
    
    for dm in danmu_list:
        text = dm.get('text', '')
        # --- 重點：時間除以 1000 ---
        raw_time = dm.get('time', 0)
        time_s = float(raw_time) / 1000.0
        
        mode = mode_map.get(dm.get('position', 0), 1)
        hex_color = dm.get('color', '#FFFFFF')
        try:
            color_dec = int(hex_color.lstrip('#'), 16)
        except:
            color_dec = 16777215
            
        # 構造 p 屬性: 秒, 模式, 字號, 顏色, 時間戳, 彈幕池, 用戶, 彈幕ID
        p = f"{time_s},{mode},25,{color_dec},{now_ts},0,bahamut,0"
        
        # 使用 escape 處理 & < >，保留其餘原始字元
        safe_content = escape(str(text))
        xml_lines.append(f'  <d p="{p}">{safe_content}</d>')
        
    xml_lines.append('</i>')
    
    # 建立檔案名
    filename = os.path.join(folder, f"第{ep_no}集_SN{sn}.xml")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    return len(danmu_list)

def run_all(start_sn):
    title, episodes = get_season_episodes(start_sn)
    if not episodes:
        print("未抓取到劇集清單。")
        return

    # 建立資料夾
    folder_name = re.sub(r'[\\/:*?"<>|]', '_', title)+"_baha"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    print(f"=== 專案標題: {title} ===")
    print(f"找到 {len(episodes)} 個集數，準備開始抓取（包含 state: 0 的劇集）...")
    
    for ep in episodes:
        sn = ep['sn']
        no = ep['no']
        
        print(f"正在處理第 {no} 集 (videoSn: {sn})...", end="", flush=True)
        
        dms = fetch_danmu(sn)
        if dms:
            count = save_xml(dms, sn, no, folder_name)
            print(f" 成功！儲存了 {count} 條彈幕 (時間已 /1000)")
        else:
            print(" 無彈幕內容 (可能該集尚未開放或真的沒有彈幕)")
            
        time.sleep(1) # 增加延遲避免被伺服器阻擋

if __name__ == "__main__":
    # 你提供的起始 videoSn
    TARGET_SN = "35241"
    run_all(TARGET_SN)
    print("\n" + "="*30)
    print("所有任務已完成！")
    input("按回車鍵 (Enter) 退出...")
