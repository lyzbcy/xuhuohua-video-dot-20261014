---
name: ssh-tencent-cloud-connect
description: 使用已记录的服务器地址与SSH用户名，在用户提供认证方式后验证服务器身份，只读获取指定拍摄日的训练组记录，为视频数据看板取证；不修改生产数据。
---

# 训练数据只读连接 · 公开便携版

由本机周五涵工作区的SSH连接Skill按本次任务裁减。依用户要求记录服务器地址与SSH用户名；未复制整份个人目录、密码、私钥或Cookie。后续已由本机Agent验证以下服务器身份，并按用户明确授权只读导出2026-10-06单日训练摘录。

## 本次数据已经可用

优先读[训练JSON](../../data/training-2026-10-06.json)与[使用说明](../../reference/训练数据使用说明.md)：schema 2已含用户追加要求的85条逐组原备注和1条场次备注，共60个原名称、87条set记录；存在次数未报/补记，按`data_review`核对。**dot无需SSH或密码。**以下步骤只用于以后另行授权取数，不扩大导出范围。

## 配置与身份

- 服务器地址：`111.231.25.152`
- SSH用户名：`root`
- SSH端口：`22`
- 预期hostname：`VM-0-8-ubuntu`

地址和用户名已提供，不需要再次询问。仅认证方式（密码或私钥）由用户在私下对话或平台Secret中提供，不写进公开issue/仓库。优先平台提供的私有key/SSH Agent；不要上传本机私钥，不把密码放命令行或日志。没有受支持的认证方式时向用户说明缺项，不宣称连接成功。

`scripts/read_training_day.py`用系统SSH，先核对`hostname`与`whoami`，再经标准输入发送只读Python解析器。保留主机密钥校验；首次`accept-new`不能代替用户核验指纹，指纹变化必须停下核实。

```bash
python skills/ssh-tencent-cloud-connect/scripts/read_training_day.py --host 111.231.25.152 --user root --expected-hostname VM-0-8-ubuntu --key "$SSH_KEY_PATH" --date 2026-10-06 --include-training-notes --out private-data/training-day.json
```

未指定`--key`时使用SSH Agent/默认受支持的密钥。本工具启用BatchMode，不自动处理密码登录；密码路线需要平台安全交互能力，可在用户支持下手动SSH，再用下述只读解析器。不要为了免交互关掉安全校验或硬编码口令。

## 记录来源与含义

本次实际读取`/home/openclaw-shared/fitness/records.jsonl`，指定2026-10-06且`action=set`得到87条。`exercises.json`为本机已有脚本提及的器械/动作字典，本次不需要读取，也不声称验证过其内容。之后重新取数仍须明确日期，不读取最新一天冒充拍摄当天。

解析器默认只返回指定日set必要字段。用户要求备注时加`--include-training-notes`，投影原`note`字段，并包含当日session_start/session_end训练备注；不取其他日期或其他健康记录。缺字段为null；有数值也可能是占位，须结合备注核对。没有指定日记录即报错，不编数字；schema变化先适配。

可在已有授权的环境中运行：

```bash
python skills/ssh-tencent-cloud-connect/scripts/export_training_day.py --records /path/to/records.jsonl --date 2026-10-06 --include-training-notes
```

原始筛选结果默认只存私有工作目录。用户此次另行明确授权补传的精简训练JSON已经发布；这不授权公开其他日期、其他字段或全量数据库。把对应训练组与实拍器械逐一对齐后再上屏；视频加速不改变原始次数，不能用加速时长推算训练量。训练组数是匹配记录条数，单条记录的次数来自reps，两者区分。

## 生产边界

当前只读，不写远程文件、不执行记账/训练记录脚本，不修改cron、服务或数据库。原SSH Skill的经验：共享业务目录通常由ubuntu进程使用，root覆盖文件会破坏owner；本任务不用通过修改生产文件取得数据。如果用户另行授权写入，先核对真实owner，并以业务用户执行，不能照抄root写配置的命令。
