import os
import re

# ================= 配置區域 =================
BAHA_FOLDER = ""  # 由 main.py 動態指定
BILI_FOLDER = ""  # 由 main.py 動態指定
OUTPUT_FOLDER = "Merged_Danmu"
# ===========================================

def extract_episode_no(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def parse_xml_danmaku(file_path):
    danmakus = []
    if not file_path or not os.path.exists(file_path):
        return danmakus
    
    pattern = re.compile(r'<d p="(.*?)">(.*?)</d>')
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        matches = pattern.findall(content)
        for p, text in matches:
            try:
                time_s = float(p.split(',')[0])
            except:
                time_s = 0.0
            danmakus.append({'p': p, 'text': text, 'time': time_s})
    return danmakus

def merge():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    baha_files = {}
    if BAHA_FOLDER and os.path.exists(BAHA_FOLDER):
        for f in os.listdir(BAHA_FOLDER):
            if f.endswith(".xml"):
                no = extract_episode_no(f)
                if no is not None: baha_files[no] = os.path.join(BAHA_FOLDER, f)

    bili_files = {}
    if BILI_FOLDER and os.path.exists(BILI_FOLDER):
        for f in os.listdir(BILI_FOLDER):
            if f.endswith(".xml"):
                no = extract_episode_no(f)
                if no is not None: bili_files[no] = os.path.join(BILI_FOLDER, f)

    # 取得兩者聯集的集數
    all_nos = sorted(set(list(baha_files.keys()) + list(bili_files.keys())))

    if not all_nos:
        print("沒有找到任何可處理的 XML 檔案。")
        return

    print(f"開始處理，來源：[巴哈: {'有' if baha_files else '無'}] [B站: {'有' if bili_files else '無'}]")

    for no in all_nos:
        combined_list = []
        sources = []
        
        if no in baha_files:
            combined_list.extend(parse_xml_danmaku(baha_files[no]))
            sources.append("巴哈")
        
        if no in bili_files:
            combined_list.extend(parse_xml_danmaku(bili_files[no]))
            sources.append("B站")

        if not combined_list:
            continue

        # 按時間排序
        combined_list.sort(key=lambda x: x['time'])

        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<i>',
            '  <chatserver>chat.bilibili.com</chatserver>',
            f'  <chatid>merged_{no}</chatid>'
        ]
        for dm in combined_list:
            xml_lines.append(f'  <d p="{dm["p"]}">{dm["text"]}</d>')
        xml_lines.append('</i>')

        output_name = os.path.join(OUTPUT_FOLDER, f"第{no:02d}集_處理後彈幕.xml")
        with open(output_name, "w", encoding="utf-8") as f:
            f.write("\n".join(xml_lines))
        
        source_str = "+".join(sources)
        print(f"  [完成] 第 {no} 集 ({source_str})：共 {len(combined_list)} 條")

if __name__ == "__main__":
    # 獨立執行時的自動偵測
    current_dirs = os.listdir(".")
    BAHA_FOLDER = next((d for d in current_dirs if d.endswith("_baha") and os.path.isdir(d)), "")
    BILI_FOLDER = next((d for d in current_dirs if d.endswith("_bili") and os.path.isdir(d)), "")
    merge()
    input("\n處理結束，按 Enter 退出...")
