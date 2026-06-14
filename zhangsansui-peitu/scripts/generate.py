#!/usr/bin/env python3
"""
张三岁配图（开源内核版）· 可选自动出图脚本（纯文字内核，无参考图）

这是一个【可选】便利脚本，给用 OpenAI gpt-image 的用户一键自动出图。
不用它也行：skill 会把 prompt 给你，贴进任何文生图工具（即梦/MJ/SD/Nano Banana…）即可。

安全：
- 用的是【你自己的】OpenAI key，从环境变量 OPENAI_API_KEY 或本地文件 ~/.zhangsansui-peitu.key 读取。
- 脚本绝不含任何 key，也不会上传到任何第三方。

用法：
    # 先在 shell 里设置 OPENAI_API_KEY，或写入 ~/.zhangsansui-peitu.key
    python3 scripts/generate.py \
        --slug 01-no-topic --scene "she lowers a small bucket into a neutral old well and pulls it back up empty, looking stunned" \
        --labels "没选题, 空桶" --out ./张三岁配图 --n 2
"""
import os, sys, json, base64, time, argparse, urllib.request, urllib.error

KERNEL = ("Cute kawaii chibi sticker illustration, extra thick rounded dark chocolate-brown marker outline, flat solid colors, no gradients, "
"plain pure white #FFFFFF background with lots of empty clean white space. Consistent character: a small round chibi "
"girl, big head, short stubby limbs, wearing a soft pink hooded onesie with two upright rounded bunny ears on the "
"hood; brown blunt-cut bangs peek out under the hood; simple face = two small black dot eyes, soft pink round blush, "
"a tiny short curved smile. Scene: ")

SUFFIX = (" 16:9 horizontal, the character is small at about one sixth of the image height, ONE single strong physical "
"action, the character's pink is the only warm color, only a few tiny color accents, real props in neutral "
"grey/white/kraft/wood/dark. {labels} No UI screenshot, no app interface, no extra logos, no big title text, no "
"poster gradient, no sticker die-cut border, no busy background, generous clean white space.")

def get_key():
    k = os.environ.get("OPENAI_API_KEY")
    if k: return k.strip()
    f = os.path.expanduser("~/.zhangsansui-peitu.key")
    if os.path.exists(f): return open(f).read().strip()
    sys.exit("ERROR: 没找到 key。请先在 shell 里设置 OPENAI_API_KEY，或写入 ~/.zhangsansui-peitu.key\n"
             "（用的是你自己的 key；不想自动出图就别用本脚本，直接拿 skill 给的 prompt 去自己的工具生。）")

def build_labels(s):
    parts = [p.strip() for p in s.split(",") if p.strip()] if s else []
    if not parts: return ""
    q = " and ".join(parts) if len(parts) <= 2 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return f"Two or three very short handwritten-style Chinese labels reading {q}."

def gen(key, prompt, n, size):
    body = json.dumps({"model":"gpt-image-1","prompt":prompt,"n":n,"size":size,"quality":"high","background":"opaque"}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--scene", required=True, help="英文场景动作描述")
    ap.add_argument("--labels", default="", help="中文标签，逗号分隔，≤3 个")
    ap.add_argument("--out", default="./张三岁配图", help="输出目录")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--size", default="1536x1024")
    a = ap.parse_args()
    key = get_key()
    os.makedirs(a.out, exist_ok=True)
    prompt = KERNEL + a.scene.rstrip(". ") + "." + SUFFIX.format(labels=build_labels(a.labels))
    for attempt in range(8):
        try:
            d = gen(key, prompt, a.n, a.size)
            for i, x in enumerate(d["data"], 1):
                p = os.path.join(a.out, f"{a.slug}-{chr(96+i)}.png")
                open(p, "wb").write(base64.b64decode(x["b64_json"]))
                print("saved", p)
            return
        except urllib.error.HTTPError as e:
            if e.code == 429:
                w = 30 + attempt*10; print(f"429 限速，等 {w}s（gpt-image 约 5 张/分）"); time.sleep(w)
            else:
                sys.exit(f"HTTP {e.code}: {e.read().decode()[:400]}")
    sys.exit("多次 429 后放弃，稍后再试")

if __name__ == "__main__":
    main()
