import os
import baha
import bili
import merge
import rename

def main():
    print("=== 動漫彈幕整合工具 ===")
    
    # 1. 輸入參數
    baha_sn = input("請輸入巴哈姆特動畫瘋 Video SN (例如 35241): ").strip()
    bili_ep = input("請輸入 Bilibili Episode ID (例如 779778): ").strip()
    
    print("\n[步驟 1/4] 正在從巴哈姆特抓取...")
    baha.run_all(baha_sn)
    
    print("\n[步驟 2/4] 正在從 Bilibili 抓取...")
    bili.download_all(bili_ep)
    
    # 2. 自動偵測產生的資料夾名稱
    # 尋找當下目錄中符合 _baha 和 _bili 結尾的資料夾
    current_dirs = os.listdir(".")
    baha_dir = next((d for d in current_dirs if d.endswith("_baha") and os.path.isdir(d)), None)
    bili_dir = next((d for d in current_dirs if d.endswith("_bili") and os.path.isdir(d)), None)
    
    if not baha_dir or not bili_dir:
        print("錯誤：找不到下載的資料夾，請確認 SN/EP ID 是否正確。")
        return

    # 3. 合併彈幕
    print(f"\n[步驟 3/4] 正在合併彈幕: {baha_dir} + {bili_dir} ...")
    merge.BAHA_FOLDER = baha_dir
    merge.BILI_FOLDER = bili_dir
    merge.merge()
    
    # 4. 重新命名配對影片
    print("\n[步驟 4/4] 正在根據影片檔名重命名彈幕...")
    rename.rename_danmu()
    
    print("\n" + "="*30)
    print("所有流程已完成！")
    print(f"合併後的原始檔在: {merge.OUTPUT_FOLDER}")
    print(f"已配對的 XML 已複製到影片旁。")
    input("按回車鍵 (Enter) 退出...")

if __name__ == "__main__":
    main()
