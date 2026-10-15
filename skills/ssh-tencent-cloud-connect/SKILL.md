---
name: ssh-tencent-cloud-connect
description: 在用户私下提供连接信息后验证SSH服务器身份，只读获取指定拍摄日的训练组记录，为本仓库视频数据看板取证；不修改生产数据。
---

# 训练数据只读连接 · 公开便携版

由本机周五涵工作区的SSH连接Skill按本次任务裁减。未复制整份个人目录、真实主机地址、密码、私钥、Cookie或健康记录；服务器尚未在本任务中实连验证。

## 配置与身份

请用户在私下对话或平台Secret中提供主机、登录用户、预期hostname和认证方式，不写进公开issue/仓库。SSH端口默认22。优先平台提供的私有key/SSH Agent；不要上传本机私钥，不把密码放命令行或日志。没有受支持的认证方式时向用户说明缺项，不宣称连接成功。

`scripts/read_training_day.py`用系统SSH，先核对`hostname`与`whoami`，再经标准输入发送只读Python解析器。保留主机密钥校验；首次`accept-new`不能代替用户核验指纹，指纹变化必须停下核实。

```bash
python skills/ssh-tencent-cloud-connect/scripts/read_training_day.py --host "$SSH_TARGET_HOST" --user "$SSH_TARGET_USER" --expected-hostname "$SSH_EXPECTED_HOSTNAME" --key "$SSH_KEY_PATH" --date 2026-10-06 --out private-data/training-day.json
```

未指定`--key`时使用SSH Agent/默认受支持的密钥。本工具启用BatchMode，不自动处理密码登录；密码路线需要平台安全交互能力，可在用户支持下手动SSH，再用下述只读解析器。不要为了免交互关掉安全校验或硬编码口令。

## 记录来源与含义

本机已有数据脚本指向`/home/openclaw-shared/fitness/records.jsonl`，`exercises.json`为器械/动作字典。这里只把路径作为探查线索，远端存在与schema需实连确认。拍摄文件名候选日为2026-10-06；用原声/元信息确认后再查，不读取最新一天冒充拍摄当天。

解析器针对已知的`action=set`、`date`、`exercise`、`weight`、`reps`、`ts`字段，只返回指定日的训练组及必要时间，绝不读取饮食、病历或全量身体指标。缺字段输出null，未知动作/器械别名需核对；没有该日记录即报错，不编数字。若真实schema改变，先检查键名并适配，不把空结果视作没有训练。

可在已有授权的环境中运行：

```bash
python skills/ssh-tencent-cloud-connect/scripts/export_training_day.py --records /path/to/records.jsonl --date 2026-10-06
```

结果只存私有工作目录，不提交GitHub。把对应训练组与实拍器械逐一对齐后再上屏；视频加速不改变原始次数，不能用加速时长推算训练量。训练组数是匹配记录条数，单条记录的次数来自reps，两者区分。

## 生产边界

当前只读，不写远程文件、不执行记账/训练记录脚本，不修改cron、服务或数据库。原SSH Skill的经验：共享业务目录通常由ubuntu进程使用，root覆盖文件会破坏owner；本任务不用通过修改生产文件取得数据。如果用户另行授权写入，先核对真实owner，并以业务用户执行，不能照抄root写配置的命令。
