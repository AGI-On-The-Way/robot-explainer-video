# 宇树科技主题口播视频

中文竖版口播视频，1080×1920。

## 下载（不用登录）

| 视频 | 时长 | 下载 |
|---|---|---|
| 机器人卖给了谁？四个问号版（数字人版） | 4 分 16 秒 | [视频 robot-questions.mp4](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v4/robot-questions.mp4)（约 152 MB）· [字幕](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v4/robot-questions.srt) |
| 机器人卖给了谁？（数字人版） | 4 分 18 秒 | [视频 robot-buyers.mp4](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v3/robot-buyers.mp4)（约 160 MB）· [字幕](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v3/robot-buyers.srt) |
| 机器人爆发，还是预期先行？ | 4 分 46 秒 | [视频 robot-explainer.mp4](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v2/robot-explainer.mp4)（约 161 MB）· [字幕](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v2/robot-explainer.srt) |

## 说明

- 视频仅作上市公司及产业研究分享，不构成投资建议。
- 数据来自公司财报、招股书和公开报道，以公司公告为准。来源见 [data/numbers.json](data/numbers.json)。
- 机器人和背景视频由 AI 生成，只是示意，不代表宇树的产品或真实场景。
- 《机器人卖给了谁？》两个版本都是数字人版：声音和口型由 AI 合成，已获出镜者本人授权，画面全程标注。《机器人爆发，还是预期先行？》为出镜者原声，画面做了清晰度增强。
- 产品照片来自宇树科技新闻稿（PR Newswire），原文截图来自澎湃新闻和虎嗅，版权归原权利人。

## 制作

全部在一台 Mac 上本地完成，使用免费工具：

| 环节 | 工具 |
|---|---|
| 图片 | Z-Image-Turbo |
| 视频 | Wan 2.2 TI2V-5B |
| 配乐 | ACE-Step 1.5 |
| 声音克隆 | CosyVoice3 |
| 对口型 | MuseTalk 1.5 |
| 人像放大 | Real-ESRGAN x2plus |
| 画面渲染 | Remotion |

[workflow/](workflow) 里是可以单独使用的三个脚本：`sfx.py` 合成提示音，`ai_assets.py` 生成示意视频，`upscale.py` 放大视频。

本仓库没有附开源许可，视频和代码未授权给他人再使用。
