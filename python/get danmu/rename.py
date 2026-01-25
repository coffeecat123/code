import os
import re
import shutil

# ================= 配置區域 =================
# 合併後的彈幕資料夾
XML_SOURCE_FOLDER = "Merged_Danmu" 

# 影片所在的資料夾 ( "." 代表目前程式執行的目錄 )
VIDEO_FOLDER = "." 

# 支援的影片格式
VIDEO_EXTS = ('.mp4', '.mkv', '.avi', '.flv', '.mov')
# ===========================================

def extract_episode_no(filename):
    """
    從檔名提取集數數字
    支援: [01], - 01, 第01集, 01.mp4 等格式
    """
    # 優先找被括號包圍的數字，例如 [01] 或 (01)
    bracket_match = re.search(r'[\[\(\【](\d+)[\]\)\】]', filename)
    if bracket_match:
        return int(bracket_match.group(1))
    
    # 排除常見的干擾數字 (如 1080p, 720p, 2023年)
    cleaned_name = re.sub(r'1080[pP]|720[pP]|4[kK]|2160[pP]|20\d{2}', '', filename)
    
    # 找剩餘部分的數字
    match = re.search(r'(\d+)', cleaned_name)
    return int(match.group(1)) if match else None

def rename_danmu():
    if not os.path.exists(XML_SOURCE_FOLDER):
        print(f"找不到來源資料夾: {XML_SOURCE_FOLDER}，請先執行 merge.py")
        return

    # 1. 掃描影片檔案，建立 {集數: 影片全名(不含副檔名)} 的映射
    video_map = {}
    print("正在掃描影片檔案...")
    for f in os.listdir(VIDEO_FOLDER):
        if f.lower().endswith(VIDEO_EXTS):
            ep_no = extract_episode_no(f)
            if ep_no is not None:
                video_base_name = os.path.splitext(f)[0]
                video_map[ep_no] = video_base_name
                print(f"  找到影片: 第 {ep_no} 集 -> {f}")

    if not video_map:
        print("在指定目錄找不到影片檔案，請檢查 VIDEO_FOLDER 設定。")
        return

    # 2. 掃描 XML 檔案並進行重新命名/複製
    print("\n開始配對並重命名彈幕...")
    xml_files = [f for f in os.listdir(XML_SOURCE_FOLDER) if f.endswith(".xml")]
    
    success_count = 0
    for xml_f in xml_files:
        ep_no = extract_episode_no(xml_f)
        
        if ep_no in video_map:
            new_xml_name = video_map[ep_no] + ".xml"
            src_path = os.path.join(XML_SOURCE_FOLDER, xml_f)
            dst_path = os.path.join(VIDEO_FOLDER, new_xml_name)
            
            # 使用複製而非移動，以免原始合併檔不見
            shutil.copy2(src_path, dst_path)
            print(f"  [成功] {xml_f}  ==>  {new_xml_name}")
            success_count += 1
        else:
            print(f"  [跳過] {xml_f} (找不到對應的影片集數)")

    print(f"\n任務完成！共成功重新命名 {success_count} 個彈幕檔案。")
    print("現在你可以直接用播放器開啟影片，應該會自動載入彈幕了。")

if __name__ == "__main__":
    rename_danmu()
    input("\n按 Enter 退出...")
