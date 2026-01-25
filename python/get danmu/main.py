import os
import baha
import bili
import merge
import rename

def main():
    print("=== 動漫彈幕整合工具 (相容單一來源模式) ===")
    
    # 1. 輸入參數 (直接按 Enter 可跳過該平台)
    baha_sn = input("請輸入巴哈姆特 SN (跳過請直接按 Enter): ").strip()
    bili_ep = input("請輸入 Bilibili EP ID (跳過請直接按 Enter): ").strip()
    
    if baha_sn:
        print("\n[步驟 1/4] 正在從巴哈姆特抓取...")
        baha.run_all(baha_sn)
    else:
        print("\n[跳過] 未輸入巴哈 SN")

    if bili_ep:
        print("\n[步驟 2/4] 正在從 Bilibili 抓取...")
        bili.download_all(bili_ep)
    else:
        print("\n[跳過] 未輸入 Bilibili EP ID")
    
    # 2. 自動偵測產生的資料夾名稱
    current_dirs = os.listdir(".")
    baha_dir = next((d for d in current_dirs if d.endswith("_baha") and os.path.isdir(d)), None)
    bili_dir = next((d for d in current_dirs if d.endswith("_bili") and os.path.isdir(d)), None)
    
    # 只要其中一個存在就可以繼續
    if not baha_dir and not bili_dir:
        print("\n錯誤：找不到任何下載的彈幕資料夾，請確認 SN/EP ID 是否正確。")
        input("按 Enter 結束...")
        return

    # 3. 合併/處理彈幕
    print(f"\n[步驟 3/4] 正在處理彈幕檔案...")
    # 傳入路徑，如果不存在則傳 None
    merge.BAHA_FOLDER = baha_dir if baha_dir else ""
    merge.BILI_FOLDER = bili_dir if bili_dir else ""
    merge.merge()
    
    # 4. 重新命名配對影片
    print("\n[步驟 4/4] 正在根據影片檔名重命名彈幕...")
    rename.rename_danmu()
    
    print("\n" + "="*30)
    print("所有流程已完成！")
    print(f"處理後的 XML 儲存在: {merge.OUTPUT_FOLDER}")
    print(f"已配對的 XML 已複製到影片旁。")
    input("按回車鍵 (Enter) 退出...")

if __name__ == "__main__":
    main()
