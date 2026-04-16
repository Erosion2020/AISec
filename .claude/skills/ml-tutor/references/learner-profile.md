# 学生画像与学习记录

本文件定义 `.claude/ml-learner-profile.md` 的完整管理逻辑。
**前提**：只有 `profile_enabled = true` 时，本文件中涉及读写 profile 的操作才生效。

---

## 第零步：确定工作目录 + 学习记录权限

**首先确定工作目录**（每次会话均执行）：
- 通过 `pwd` 获取当前绝对路径，即为「工作目录」
- Skill目录 = 工作目录 + `/.claude/skills/ml-tutor`
- profile 文件路径 = 工作目录 + `/.claude/ml-learner-profile.md`

检查 profile 文件是否存在：

**情况 A：文件不存在**（首次使用）

向用户发出一次询问：

> 顺便问一下——我可以在本地记录一点你的学习进度吗？这样下次继续学的时候，我能知道你上次学到哪里、哪些概念已经熟了，不用从头开始。文件只存在你自己的电脑上，你随时可以删。

- 用户**同意** → `profile_enabled = true`，创建文件并写入初始结构
- 用户**拒绝** → `profile_enabled = false`，本次会话内不再提起，不创建文件

**情况 B：文件已存在**

直接 `profile_enabled = true`，读取文件，进入正常流程。

`profile_enabled` 一旦确定为 `false`，本次会话内不再询问，也不尝试读写文件。

---

## 路径体系说明

本 skill 运行时涉及两个根目录，所有路径以其中之一为锚点：

- **工作目录**：用户实际学习的项目目录，即 Claude Code 启动时的 `pwd` 输出值。
- **Skill目录**：skill 自身所在目录，= 工作目录 + 路径分隔符 + `.claude/skills/ml-tutor`。

**平台识别**：通过 `pwd` 输出格式判断当前平台：
- 输出以 `/` 开头（如 `/Users/...` 或 `/home/...`）→ macOS / Linux，路径分隔符为 `/`
- 输出以盘符开头（如 `C:\...` 或 `D:\...`），或在 Git Bash 下为 `/c/...` 等→ Windows，路径分隔符为 `\`（拼接系统调用路径时）

**平台和路径写入 profile 一次，后续全程复用，不再重新判断。**

---

## Profile 文件格式

文件路径（绝对）：`<工作目录>/.claude/ml-learner-profile.md`

```markdown
## 基础配置
操作系统：（Windows / macOS / Linux）
工作目录：（绝对路径，由 pwd 写入，例：
  macOS/Linux：/Users/yourname/workspace/AISec
  Windows：D:\WorkSpace\AISec）
Skill目录：（绝对路径，例：
  macOS/Linux：/Users/yourname/workspace/AISec/.claude/skills/ml-tutor
  Windows：D:\WorkSpace\AISec\.claude\skills\ml-tutor）

## 导师性格
已选风格：（文件名，如 lee-style.md）
性格文件：（绝对路径，例：
  macOS/Linux：/Users/yourname/workspace/AISec/.claude/skills/ml-tutor/references/personas/lee-style.md
  Windows：D:\WorkSpace\AISec\.claude\skills\ml-tutor\references\personas\lee-style.md）

## 环境配置
python解释器：（绝对路径，例：
  macOS/Linux conda：/Users/yourname/miniconda3/envs/ml-tutor/bin/python
  Windows conda：D:\miniconda3\envs\ml-tutor\python.exe）
环境类型：（conda / uv / venv / system）
最后验证时间：（YYYY-MM-DD）

## PDF 配置
PDF路径：（绝对路径）
页码偏移：（整数，通常为 1；含义：用户说"第N页"= 程序输入 N+偏移）
提取命令示例：（首次成功运行后填入完整可执行命令，例：
  macOS/Linux："/Users/yourname/.../python" "/Users/yourname/.../extract_pdf_pages.py" "/Users/yourname/.../LeeDL.pdf" 31 35
  Windows："D:\...\python.exe" "D:\...\extract_pdf_pages.py" "D:\...\LeeDL.pdf" 31 35）
当前学习进度：（如：第30页 · 第二章梯度下降）

## 学习画像
数学水平：初中（默认）
判断依据：（留空，直到有足够证据才填写）
已掌握概念：（如：梯度下降·已理解, 反向传播·待复习）
当前进度模块：（如：第二部分·深度学习基础）

## 交互日志
（格式：[YYYY-MM-DD HH:MM] [知识点] 一句话描述用户的表现）
```

---

## 初始化逻辑：各字段的缓存命中规则

读取 profile 文件后，按以下规则决定跳过哪些步骤：

| 字段 | 命中条件 | 命中时 |
|------|----------|--------|
| `工作目录` / `Skill目录` | 字段非空 | 直接用于拼接所有后续路径，无需重新 pwd |
| `性格文件` | 绝对路径非空且文件存在 | 直接读取，跳过性格选择流程 |
| `python解释器` | 绝对路径非空且可执行 | 跳过所有环境探测步骤 |
| `提取命令示例` | 字段非空 | PDF 提取时直接替换页码参数后运行，跳过一切探测 |
| `PDF路径` | 绝对路径非空 | 用户只说页码时直接使用，不再询问路径 |
| `页码偏移` | 字段非空 | 自动修正页码，不再询问 |

字段为空、文件不存在、或路径失效时，才走对应的探测/询问流程，成功后写回。
**写入时所有路径字段均使用绝对路径**，不使用相对路径。

---

## 性格选择（`已选风格`为空时触发）

读取 `references/personas/selection.md`，按其中的动态发现流程完成性格选择，
将结果写入 `已选风格` 和 `性格文件` 字段，然后立即加载对应的 persona 文件。

---

## 三阶段画像运作规则

### 第 1 次运行（文件不存在或交互日志为空）

只完成初始化（写入环境配置、性格字段），画像区块保持默认，不做任何判断。
教学时使用默认假设：数学水平初中。

### 第 2~N 次（交互日志条数 < 20）

进入**信息收集阶段**。每次写回时，向「交互日志」追加本次摘要：

```
[时间] [知识点] 一句话描述用户的表现
```

记录内容：
- 用了几轮才理解
- 是否主动追问（追问什么）
- 能否用自己的话复述
- 确认小题答对/答错了几次

**不要**在此阶段修改「数学水平」字段，证据不足时下结论是误判的主要来源。

### 第 N 次（触发评估条件）

满足以下任一条件时，触发画像重新评估：
- 交互日志条数 ≥ 20
- 文件总行数 ≥ 200 行

**评估信号表：**

| 信号 | 倾向 |
|------|------|
| 需要 3+ 轮才能理解基础类比 | 下调数学水平 |
| 1 轮理解，能复述 | 上调 |
| 主动追问"为什么用X不用Y"（机制性追问） | 明显上调 |
| 追问"这个符号是什么意思"（确认性追问） | 不算信号 |
| 答对确认小题且能解释理由 | 上调 |
| 多次在同类概念上卡住 | 下调 |

评估后重写「学习画像」区块，填入数学水平和判断依据（引用具体日志条目）。

**日志压缩：**
- 文件 < 200 行：将旧日志归纳为一段摘要，保留最近 10 条原始记录
- 文件 ≥ 200 行：删除所有旧日志，只保留画像结论和最近 10 条记录
