import os
import re
import shutil

# ================= 配置區域 =================
XML_SOURCE_FOLDER = "Merged_Danmu" 
VIDEO_FOLDER = "." 
VIDEO_EXTS = ('.mp4', '.mkv', '.avi', '.flv', '.mov')
# ===========================================

def extract_episode_id(filename):
    """
    提取帶有類型的集數 ID (例如: EP1, SP1, OVA1)
    """
    filename_upper = filename.upper()
    
    # 1. 辨識類型標籤
    prefix = "EP" # 預設為正片
    if any(k in filename_upper for k in ["SP", "特別", "SPECIAL", "特典"]):
        prefix = "SP"
    elif any(k in filename_upper for k in ["OVA", "OAD"]):
        prefix = "OVA"

    # 2. 提取數字
    # 優先找被括號包圍的數字 [01]
    bracket_match = re.search(r'[\[\(\【](\d+)[\]\)\】]', filename)
    if bracket_match:
        return f"{prefix}{int(bracket_match.group(1))}"
    
    # 排除干擾後找數字
    cleaned_name = re.sub(r'1080[pP]|720[pP]|4[kK]|2160[pP]|20\d{2}', '', filename_upper)
    match = re.search(r'(\d+)', cleaned_name)
    if match:
        return f"{prefix}{int(match.group(1))}"
    
    return None

def rename_danmu():
    if not os.path.exists(XML_SOURCE_FOLDER):
        print(f"找不到來源資料夾: {XML_SOURCE_FOLDER}")
        return

    # 1. 掃描影片檔案
    video_map = {}
    print("正在掃描影片檔案...")
    for f in os.listdir(VIDEO_FOLDER):
        if f.lower().endswith(VIDEO_EXTS):
            ep_id = extract_episode_id(f)
            if ep_id:
                video_base_name = os.path.splitext(f)[0]
                video_map[ep_id] = video_base_name
                print(f"  找到影片: {ep_id} -> {f}")

    if not video_map:
        print("找不到影片檔案。")
        return

    # 2. 掃描 XML 並配對
    print("\n開始配對並重命名彈幕...")
    xml_files = [f for f in os.listdir(XML_SOURCE_FOLDER) if f.endswith(".xml")]
    
    success_count = 0
    for xml_f in xml_files:
        xml_id = extract_episode_id(xml_f)
        
        if xml_id in video_map:
            new_xml_name = video_map[xml_id] + ".xml"
            src_path = os.path.join(XML_SOURCE_FOLDER, xml_f)
            dst_path = os.path.join(VIDEO_FOLDER, new_xml_name)
            
            shutil.copy2(src_path, dst_path)
            print(f"  [成功] {xml_f}  ==>  {new_xml_name}")
            success_count += 1
        else:
            print(f"  [跳過] {xml_f} (找不到對應的 {xml_id} 影片)")

    print(f"\n任務完成！成功配對 {success_count} 個檔案。")

if __name__ == "__main__":
    rename_danmu()
    input("\n按 Enter 退出...")
