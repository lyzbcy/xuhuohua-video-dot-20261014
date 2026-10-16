# 健身系列剪辑交接 · 2026-10-16

本仓库已补制作组件；原始素材仍在 `fitness-materials-20261015` Release。不要只下载自动生成的 Source code ZIP，它不含原始视频。

1. 先读用户原文 [agent.txt](agent.txt)、[本次制作Skill](SKILL.md)，再按需读通用制作Skill及案例。当前用户要求优先于历史SOP。
2. 下载原素材29个分包；依[下载说明](下载说明.txt)、[分包清单](分包清单.csv)和SHA256清单核验、拼接8个ZIP。工具：`python tools/materials.py --input <分包目录> --output <工作目录>`。
3. 在同一Release下载 `fitness-editing-kit-20261016-v0.5.7.zip` 与 `fitness-selected-stickers-20261016.zip`，按 `FITNESS_KIT_SHA256SUMS.txt` 校验，解压到同一工作目录。前者包括本文档、相对路径Skill、模板、RPG原图和可播放范例；后者含424张精选PNG及逐文件清单。
4. `python tools/check_environment.py`检查环境；仅缺少的依赖按需安装。无需运行Windows桌面、无需NVENC，RPG模板有CPU编码路线。云端生图、生歌、TTS、SSH和耳听能力各自确认，不能用本机跑通过代替本机以外实测。
5. 训练数据读取见[SSH与训练数据Skill](skills/ssh-tencent-cloud-connect/SKILL.md)，其中已记录服务器地址、SSH用户名与预期hostname。原素材文件名指向2026-10-06，先与原声/元信息核对日期，再只读取对应日。仅密码或私钥等认证信息由用户私下提供，不在仓库里。
6. 本次先制作一张三栏构图示意让用户确认；随后制作带真人口播、声音、字幕和数据的代表样段。歌曲有多个候选就先供用户试听选择，再锁定音源。

预览示意与歌曲选择是用户原文要求；不要增加整片逐组审批等旧SOP门槛。收到用户后续指令时按其最新要求继续。

## 完整性与状态

原Release的29个分包已按文件名、字节数、GitHub SHA256与分包清单逐项核对。此次没有重新下载10GB原素材，也没有连接云服务器或开始剪辑。新增组件的清单/哈希见 `KIT_MANIFEST.json`，核验范围见 `KIT_VERIFICATION.json`。

第三方剪辑参考提供原来源和具体秒数拆解，公开包不重复分发其视频副本；原创RPG01可直接播放，不含私人实拍、对白或平台歌曲。参考内出现的网址仅用于取材，不自动放进成片。
