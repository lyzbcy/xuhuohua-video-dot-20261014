# 原创RPG与表情动作模板

来源：2026-10-15私人日常v2的小动画。用户80分是整条私人片评分；模板不是健身片固定剧情。这里不含私人实拍、对白或平台歌曲。

- `assets/商场像素场景.png`、`assets/双人行走精灵.png`：原创生成位图。
- `animation.py`：角色脚底对齐、行走/停下、目标交互、道具交接、反馈保持、分块alpha转场，以及表情有起止的动作。
- `render_demo.py`：Pillow + FFmpeg CPU编码，可选透明MOV或H.264示范。
- 完整可播放9.5秒范例：`../../skills/software-video-production/examples/media/RPG01-life-interaction.mp4`。

```bash
python components/rpg/render_demo.py --kind shop --out work/rpg-shop.mp4
python components/rpg/render_demo.py --kind save --transparent --out work/rpg-save.mov
python components/rpg/render_demo.py --kind ice --frame 1.7 --out work/rpg-frame.png
```

需要Python/Pillow、FFmpeg与中文字体。没有合适字体时设置`VIDEO_CJK_FONT`为实际字体文件路径；不捆绑系统商业字体。MP4示范用底色填透明区域，透明MOV用于叠真人画面；原4K实拍仍应直接解码原片。当前输出示范1920×1080，像素层为有意的风格设计，不能放大低清真人冒充4K。

迁移到本片：换成健身房区域/器械/角色动作，重新匹配训练故事。不要不加判断沿用人物关系、日期、台词或冰淇淋情节。
