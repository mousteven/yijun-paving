# -*- coding: utf-8 -*-
"""從「岳父工程學徒-公開版」挑出已確認的案場，壓縮照片、去除 EXIF(含 GPS)，產生 cases.js。
只收錄岳父確實承作、且有工地實景照的案子；報價、合約金額、單價一律不進來。"""
import json, shutil
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\User\Projects\岳父工程學徒-公開版\photos")
DST = Path(r"C:\Users\User\Projects\yijun-paving")
OUT_PHOTOS = DST / "photos"

FULL_MAX, THUMB_MAX, Q = 1600, 640, 82

CASES = [
    {"folder": "06_大台中轉運中心", "slug": "taichung-transit",
     "title": "大臺中轉運中心興建工程", "loc": "臺中市東區", "year": "111–115年",
     "client": "見安營造股份有限公司",
     "scope": ["人字砌連鎖磚廣場", "月台候車廊道與聯絡通道鋪面", "石籠護坡牆", "圓形樹穴／花台收邊"],
     "note": "本公司承作範圍為站體周邊與月台區域之鋪面工程，屬大型交通建設案場，需配合主體工程分區分期施作。"},
    {"folder": "13_雲林肉品市場", "slug": "yunlin-meat-market",
     "title": "雲林縣肉品市場整建工程", "loc": "雲林縣虎尾鎮", "year": "112–115年",
     "client": "中鴻營造有限公司",
     "scope": ["大面積植草磚鋪設", "連鎖磚廣場", "安全島柱列與收邊"],
     "note": "本公司承作之植草磚鋪設面積為歷年案場中規模最大者之一。"},
    {"folder": "02_仁德區聯合活動中心", "slug": "rende-center",
     "title": "臺南市仁德區聯合活動中心興建工程及公園開闢工程", "loc": "臺南市仁德區", "year": "114–115年",
     "client": "弘豐營造股份有限公司",
     "scope": ["灰色連鎖磚廣場（十字對縫）", "裝置藝術廣場鋪面", "紅磚壓邊溪畔步道"],
     "note": "活動中心與相鄰公園同期施作，含廣場、步道與壓邊收頭。"},
    {"folder": "04_南屯樹德河濱公園", "slug": "shude-riverside",
     "title": "南屯樹德河濱公園護堤景觀工程", "loc": "臺中市南屯區", "year": "114–115年",
     "client": "",
     "scope": ["毛石砌擋土牆", "石籠（蛇籠）護岸", "河濱廣場鋪面", "鵝卵石馬賽克藝術牆"],
     "note": "護岸結構與景觀鋪面整合施作，工期橫跨數月。"},
    {"folder": "05_彰化芬園鄉動保防疫所", "slug": "fenyuan",
     "title": "彰化縣芬園鄉動物保護防疫所周邊工程", "loc": "彰化縣芬園鄉", "year": "115年",
     "client": "",
     "scope": ["鵝卵石填充石籠圍牆", "蝴蝶造型連鎖磚拼花廣場"],
     "note": "造型拼花需先行放樣分割，磚材依圖案分色排列。"},
    {"folder": "07_彰化花壇鄉工地及紅磚古厝植草磚廣場", "slug": "huatan",
     "title": "彰化花壇彰60鄉道人行道及廣場工程", "loc": "彰化縣花壇鄉", "year": "115年",
     "client": "",
     "scope": ["蜿蜒山路連鎖磚人行道（灰底紅磚點綴）", "大面積植草磚廣場"],
     "note": "沿線路型彎曲，需大量現場切割配磚。"},
    {"folder": "11_宏海塱墅街屋後巷", "slug": "honghai-lang",
     "title": "宏海塱墅街屋後巷鋪面工程", "loc": "彰化縣", "year": "115年",
     "client": "",
     "scope": ["連鎖磚鋪面", "花崗石鋪面", "人手孔蓋／檢查井收邊"],
     "note": "巷道內管線人手孔密集，收邊切割為本案主要施工重點。"},
    {"folder": "12_員林龍燈公園", "slug": "yuanlin-longdeng",
     "title": "員林龍燈公園景觀工程", "loc": "彰化縣員林市", "year": "115年",
     "client": "",
     "scope": ["仿木紋鵝卵石階梯", "扇形放射狀連鎖磚廣場", "崗石磚迴廊鋪設"],
     "note": "扇形放射鋪法由圓心向外施作，階梯由下而上，均依施工圖放樣。"},
    {"folder": "10_彰化中山路宏海御邸", "slug": "honghai-yudi",
     "title": "宏海御邸集合住宅巷道鋪面工程", "loc": "彰化市中山路一段", "year": "115年",
     "client": "",
     "scope": ["花崗石鋪面", "建材吊運與現場配置"],
     "note": "屬短工期快速交付案場。"},
    {"folder": "08_台中新社公所廣場", "slug": "xinshe",
     "title": "臺中市新社區公所廣場鋪面工程", "loc": "臺中市新社區", "year": "—",
     "client": "",
     "scope": ["幾何菱格紋連鎖磚廣場"],
     "note": ""},
]

def shrink(src, dst, maxpx):
    im = Image.open(src)
    im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > maxpx:
        r = maxpx / max(w, h)
        im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
    clean = Image.new("RGB", im.size)   # 新影像不帶任何 EXIF/GPS
    clean.paste(im)
    clean.save(dst, "JPEG", quality=Q, optimize=True, progressive=True)

if OUT_PHOTOS.exists():
    shutil.rmtree(OUT_PHOTOS)
OUT_PHOTOS.mkdir(parents=True)

data = []
for c in CASES:
    d = OUT_PHOTOS / c["slug"]
    (d / "t").mkdir(parents=True)
    files = sorted(p for p in (SRC / c["folder"]).iterdir() if p.suffix.lower() == ".jpg")
    names = []
    for i, p in enumerate(files, 1):
        out = f"{i:02d}.jpg"
        shrink(p, d / out, FULL_MAX)
        shrink(p, d / "t" / out, THUMB_MAX)
        names.append(out)
    data.append({k: c[k] for k in ("slug", "title", "loc", "year", "client", "scope", "note")} | {"photos": names})
    print(f"{c['slug']:22s} {len(names):3d} 張")

with open(DST / "cases.js", "w", encoding="utf-8") as f:
    f.write("const CASES = ")
    json.dump(data, f, ensure_ascii=False, indent=0)
    f.write(";\n")
print("總計", sum(len(d["photos"]) for d in data), "張")
