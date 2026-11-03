# 机器人爆发，还是预期先行？

宇树科技主题的中文竖版口播视频，1080×1920，4 分 46 秒。

## 下载（不用登录）

- [视频 robot-explainer.mp4](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v2/robot-explainer.mp4)（约 161 MB）
- [字幕 robot-explainer.srt](https://github.com/AGI-On-The-Way/robot-explainer-video/releases/download/v2/robot-explainer.srt)

## 说明

- 本视频仅作上市公司及产业研究分享，不构成投资建议。
- 数据来自公司财报、招股书和公开报道，以公司公告为准。来源见 [data/numbers.json](data/numbers.json)。
- 机器人和背景视频由 AI 生成，只是示意，不代表宇树的产品或真实场景。
- 口播为出镜者原声，画面做了清晰度增强。
- 产品照片来自宇树科技新闻稿（PR Newswire），原文截图来自澎湃新闻和虎嗅，版权归原权利人。

## 制作

全部在一台 Mac 上本地完成，使用免费工具：

| 环节 | 工具 |
|---|---|
| 图片 | Z-Image-Turbo |
| 视频 | Wan 2.2 TI2V-5B |
| 配乐 | ACE-Step 1.5 |
| 人像放大 | Real-ESRGAN x2plus |
| 画面渲染 | Remotion |

[workflow/](workflow) 里是可以单独使用的三个脚本：`sfx.py` 合成提示音，`ai_assets.py` 生成示意视频，`upscale.py` 放大视频。

本仓库没有附开源许可，视频和代码未授权给他人再使用。
