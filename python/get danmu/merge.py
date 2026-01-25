import os
import re
from xml.sax.saxutils import escape, unescape

# ================= 配置區域 =================
BAHA_FOLDER = "你的動畫名稱_baha"  # 巴哈資料夾名稱
BILI_FOLDER = "你的動畫名稱_bili"  # B站資料夾名稱
OUTPUT_FOLDER = "Merged_Danmu"    # 合併後的輸出資料夾
# ===========================================

def extract_episode_no(filename):
    """從檔案名提取數字作為集數判斷 (例如：第01集 -> 1)"""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def parse_xml_danmaku(file_path):
    """解析 XML 提取所有彈幕節點內容"""
    danmakus = []
    if not os.path.exists(file_path):
        return danmakus
    
    # 使用正則表達式抓取 <d p="...">內容</d> 比較不會被編碼問題干擾
    pattern = re.compile(r'<d p="(.*?)">(.*?)</d>')
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        matches = pattern.findall(content)
        for p, text in matches:
            # 取得時間 (p屬性第一個值) 用於排序
            try:
                time_s = float(p.split(',')[0])
            except:
                time_s = 0.0
            danmakus.append({
                'p': p,
                'text': text, # 這裡通常已經是 escape 過的
                'time': time_s
            })
    return danmakus

def merge():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # 建立集數映射表 {集數: 檔案路徑}
    baha_files = {}
    if os.path.exists(BAHA_FOLDER):
        for f in os.listdir(BAHA_FOLDER):
            if f.endswith(".xml"):
                no = extract_episode_no(f)
                if no is not None: baha_files[no] = os.path.join(BAHA_FOLDER, f)

    bili_files = {}
    if os.path.exists(BILI_FOLDER):
        for f in os.listdir(BILI_FOLDER):
            if f.endswith(".xml"):
                no = extract_episode_no(f)
                if no is not None: bili_files[no] = os.path.join(BILI_FOLDER, f)

    # 取得所有出現過的集數
    all_nos = sorted(set(list(baha_files.keys()) + list(bili_files.keys())))

    print(f"開始合併任務，預計處理 {len(all_nos)} 集...")

    for no in all_nos:
        combined_list = []
        
        # 讀取巴哈
        if no in baha_files:
            combined_list.extend(parse_xml_danmaku(baha_files[no]))
        
        # 讀取 Bili
        if no in bili_files:
            combined_list.extend(parse_xml_danmaku(bili_files[no]))

        if not combined_list:
            continue

        # 按時間排序 (這對播放器載入非常重要)
        combined_list.sort(key=lambda x: x['time'])

        # 構造新的 XML
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<i>',
            '  <chatserver>chat.bilibili.com</chatserver>',
            f'  <chatid>merged_{no}</chatid>'
        ]

        for dm in combined_list:
            # 這裡的 dm['text'] 已經是抓取時轉義過的，直接放進去即可
            xml_lines.append(f'  <d p="{dm["p"]}">{dm["text"]}</d>')

        xml_lines.append('</i>')

        # 儲存檔案
        output_name = os.path.join(OUTPUT_FOLDER, f"第{no:02d}集_合併彈幕.xml")
        with open(output_name, "w", encoding="utf-8") as f:
            f.write("\n".join(xml_lines))
        
        print(f"  [成功] 第 {no} 集：合併完成 (總計 {len(combined_list)} 條彈幕)")

if __name__ == "__main__":
    # 自動偵測：如果你沒改配置，嘗試尋找當前目錄下的 _baha 和 _bili 資料夾
    current_dirs = os.listdir(".")
    baha_dir = next((d for d in current_dirs if d.endswith("_baha") and os.path.isdir(d)), None)
    bili_dir = next((d for d in current_dirs if d.endswith("_bili") and os.path.isdir(d)), None)

    if baha_dir: BAHA_FOLDER = baha_dir
    if bili_dir: BILI_FOLDER = bili_dir

    print(f"設定巴哈來源: {BAHA_FOLDER}")
    print(f"設定 B 站來源: {BILI_FOLDER}")
    
    merge()
    print("\n所有合併工作已結束！檔案保存在:", OUTPUT_FOLDER)
    input("按 Enter 退出...")
