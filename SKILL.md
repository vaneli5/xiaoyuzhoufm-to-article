# 小宇宙 FM 转文章 Skill

将小宇宙FM播客链接转换为结构化文章。

## 使用场景

用户给出小宇宙FM播客链接，skill 将：
1. 抓取播客页面内容（使用 jina.ai）
2. 提取标题、简介、Show Notes 和 Transcript
3. 使用 AI 生成自然流畅的文章
4. 可选：发布到 Clawpress

## 工作流程

### Step 1: 验证链接格式
支持以下格式：
- `https://www.xiaoyuzhoufm.com/episode/xxxxxxxx`
- `https://xiaoyuzhoufm.com/episode/xxxxxxxx`

### Step 2: 抓取内容
使用 jina.ai API 提取页面完整内容：
```bash
curl -s "https://r.jina.ai/https://www.xiaoyuzhoufm.com/episode/${episode_id}"
```

### Step 3: 解析内容
从抓取的内容中提取：
- 标题
- 播客名称
- 时长
- 简介/Show Notes
- Transcript（如果有）

### Step 4: 生成文章
使用 AI 模型（如 MiniMax）将内容转换为流畅的中文文章，包含：
- 标题
- 引言/背景
- 核心内容总结（按主题/时间轴组织）
- 关键要点
- 结尾

### Step 5: 输出
- 直接输出文章到对话
- 可选：发布到 Clawpress

## 输出格式

```
# [生成的文章标题]

[正文内容]

---
来源: [播客名称]
时长: [时长]
原始链接: [原始链接]
```

## 示例

用户输入：
> https://www.xiaoyuzhoufm.com/episode/63806c695f348ff5d90980fd

输出：
> # 反脆弱：从动荡中获益的能力
> 
> [AI 生成的文章内容]
> 
> ---
> 来源: 任鑫这周找谁学
> 时长: 50分钟
> 原始链接: https://www.xiaoyuzhoufm.com/episode/63806c695f348ff5d90980fd
