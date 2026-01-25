import os
import requests
import time
import re
from xml.sax.saxutils import escape

# ================= 配置區域 =================
USER_COOKIE = "buvid3=7CC56DE8-43CC-89D1-F85E-E0BBAFEF0AF631370infoc; balh_server_inner=__custom__; balh_is_closed=; _uuid=3817C9BA-3F48-C6A1-8C94-C525255BE4C933541infoc; b_nut=1752853133; buvid_fp=a843904da524246ae3d1717b95165221; rpdid=|()YYuuYkkk0J'u~lk)lRJR|; CURRENT_QUALITY=0; CURRENT_FNVAL=16; b_lsid=10DBD10DCE_19BDBE4A0E3; bsource=search_google; home_feed_column=4; lang=zh-Hans; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; buvid4=AA7A737A-B54A-683D-C760-B8E87461543633152-025071823-+UDY6hIO+4nfpj/oQNOeZA%3D%3D; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjkxNzk5NTQsImlhdCI6MTc2ODkyMDY5NCwicGx0IjotMX0.lVnZRlVbKpv25X6Wiwv2CraPNArUDgUgPUxk_Zl9GAs; bili_ticket_expires=1769179894; browser_resolution=674-569" 
# ===========================================

try:
    import brotli
except ImportError:
    brotli = None

def _decode_varint(data, pos):
    result, shift = 0, 0
    while True:
        if pos >= len(data): return result, pos
        b = data[pos]
        result |= ((b & 0x7f) << shift)
        pos += 1
        if not (b & 0x80): return result, pos
        shift += 7
        if shift >= 64: raise ValueError("Varint too long")

def get_season_info(ep_id):
    url = f"https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
        "Cookie": USER_COOKIE
    }
    try:
        resp = requests.get(url, headers=headers).json()
        if resp.get('code') != 0: return None, []
        return resp['result'].get('title', 'Unknown'), resp['result'].get('episodes', [])
    except: return None, []

def parse_dm_segment(data):
    danmakus = []
    pos, length = 0, len(data)
    if data.startswith(b'{'): return None 
    try:
        while pos < length:
            key, pos = _decode_varint(data, pos)
            if (key >> 3) == 1 and (key & 0x7) == 2:
                size, pos = _decode_varint(data, pos)
                next_pos = pos + size
                dm = {'id': 0, 'progress': 0, 'mode': 0, 'fontsize': 25, 'color': 16777215, 'midHash': '', 'content': '', 'ctime': 0}
                while pos < next_pos:
                    sub_key, pos = _decode_varint(data, pos)
                    field = sub_key >> 3
                    if field == 1: dm['id'], pos = _decode_varint(data, pos)
                    elif field == 2: dm['progress'], pos = _decode_varint(data, pos)
                    elif field == 3: dm['mode'], pos = _decode_varint(data, pos)
                    elif field == 4: dm['fontsize'], pos = _decode_varint(data, pos)
                    elif field == 5: dm['color'], pos = _decode_varint(data, pos)
                    elif field == 6:
                        l, pos = _decode_varint(data, pos)
                        dm['midHash'] = data[pos:pos+l].decode('utf-8', 'ignore')
                        pos += l
                    elif field == 7:
                        l, pos = _decode_varint(data, pos)
                        # 保留原始字串，不進行任何過濾
                        dm['content'] = data[pos:pos+l].decode('utf-8', 'ignore')
                        pos += l
                    elif field == 8: dm['ctime'], pos = _decode_varint(data, pos)
                    else:
                        wire = sub_key & 0x7
                        if wire == 0: _, pos = _decode_varint(data, pos)
                        elif wire == 2: l, pos = _decode_varint(data, pos); pos += l
                        elif wire == 1: pos += 8
                        elif wire == 5: pos += 4
                danmakus.append(dm)
            else:
                wire = key & 0x7
                if wire == 0: _, pos = _decode_varint(data, pos)
                elif wire == 2: l, pos = _decode_varint(data, pos); pos += l
                elif wire == 1: pos += 8
                elif wire == 5: pos += 4
    except: pass
    return danmakus

def fetch_seg(cid, idx):
    url = f"https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={cid}&segment_index={idx}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": USER_COOKIE,
        "Accept-Encoding": "gzip, deflate, br"
    }
    resp = requests.get(url, headers=headers)
    content = resp.content
    if resp.headers.get('Content-Encoding') == 'br' and brotli:
        try: content = brotli.decompress(content)
        except: pass
    return content

def download_all(ep_id):
    season_title, episodes = get_season_info(ep_id)
    if not episodes: return
    
    folder = re.sub(r'[\\/:*?"<>|]', '_', season_title)+"_bili"
    if not os.path.exists(folder): os.makedirs(folder)
    
    print(f"=== 項目: {season_title} ===")
    for ep in episodes:
        cid = ep['cid']
        title = ep.get('share_copy', '')
        badge = ep.get('badge', '')
        
        if "預告" in badge or "預告" in title:
            print(f"  [跳過] {share_copy} (檢測為預告片)")
            continue
        print(f"正在抓取: {title}...")
        
        all_dms = []
        for i in range(1, 15):
            data = fetch_seg(cid, i)
            if not data or len(data) < 20: break
            dms = parse_dm_segment(data)
            if dms is None: return 
            if not dms: break
            all_dms.extend(dms)
            time.sleep(1)
        
        if all_dms:
            # 去重
            unique_dms = {d['id']: d for d in all_dms}.values()
            
            # --- 手動構造 XML 字串 (不使用 minidom) ---
            xml_lines = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<i>',
                '  <chatserver>chat.bilibili.com</chatserver>',
                f'  <chatid>{cid}</chatid>'
            ]
            
            for dm in unique_dms:
                # 僅轉義 XML 必要符號 (& < >)，保留所有原始控制字元
                # escape 函數會處理 & -> &amp; < -> &lt; > -> &gt;
                safe_content = escape(dm['content'])
                p = f"{dm['progress']/1000},{dm['mode']},{dm['fontsize']},{dm['color']},{dm['ctime']},0,{dm['midHash']},{dm['id']}"
                xml_lines.append(f'  <d p="{p}">{safe_content}</d>')
            
            xml_lines.append('</i>')
            
            filename = os.path.join(folder, re.sub(r'[\\/:*?"<>|]', '_', title) + ".xml")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(xml_lines))
            print(f"  [成功] 儲存 {len(unique_dms)} 條彈幕")
        time.sleep(2)

if __name__ == "__main__":
    download_all("779778")
    input("\n完成！")
