# 单张生图提示词模板（开源内核版）

本版用**纯文字内核**驱动，任何文生图模型都能用。每条提示词都要把张三岁的 5 个内核特征写进去，模型才会收敛成同一个角色。

## 通用结构

```text
[风格底色] + [张三岁内核 5 特征] + [场景：一个核心物理动作 + 真实主物件] +
[2-3 个短中文标签] + [构图与留白] + [负面约束]
```

## 可复制英文模板（推荐，模型更稳）

```text
Cute kawaii chibi sticker illustration, thick dark brown clean outline, flat solid colors, no gradients,
plain pure white #FFFFFF background with lots of empty clean white space.

Consistent character: a small round chibi girl, big head, short stubby limbs, wearing a soft pink hooded
onesie with two upright rounded bunny ears on the hood; brown blunt-cut bangs peek out under the hood;
simple face = two small black dot eyes, soft pink round blush, a tiny short curved smile.

Scene: <一个清晰强烈的物理动作 + 真实主物件，物件用中性灰/白/牛皮纸/深色>.

16:9 horizontal, the character is small at about one sixth of the image height, ONE single strong physical
action, the character's pink is the only warm focal color, only a few tiny color accents.
Two or three very short handwritten-style Chinese labels reading <标签1>, <标签2>(, <标签3>).

No UI screenshot, no app interface, no extra logos, no big title text, no poster gradient,
no sticker die-cut border, no busy background, generous clean white space.
```

## 关键填空原则

- **场景动作**：只写一个核心物理动作（被拽/挡住/解结/审查/拉扯/推入）。动作要强——后仰、蹬腿、用力、被压，不要"站着拿东西"。
- **真实主物件**：1 个主物件或紧凑物件组，中性色。不要把主题里所有名词都塞进去。
- **中文标签**：≤3 个，每个 2-6 字，高频真实话术。糊了就减到 2 个重生成。
- **尺寸**：16:9（如 gpt-image 用 `1536x1024`；其他模型选最接近 16:9 的横版）。

## 可选：用参考图提高一致性

本仓库 `assets/zhangsansui-kernel-ref.png` 是内核版角色定妆图。如果你的模型支持**图生图/参考图**，把它喂进去能让角色更稳，但**不是必须**——纯文字也能复现。

> 注意：内核版定妆图只含 5 个核心特征，**不含**满配版的帽顶兔脸、爱心发夹、肚子小熊 logo。这是作者私有版的高保真层，开源版不复现这些细节。

## 中文文字不稳的处理

文生图模型对中文经常出错字、幻觉笔画。对策：

1. 标签越短越稳，优先 2-3 个常用词。
2. 一次只放确实需要的标签。
3. 错字严重时：减少标注词 → 重生成；或留白，事后用图片工具补字。
4. 把标签当"情绪点缀"，不要依赖它讲清楚信息——信息靠物理动作和物件传达。
