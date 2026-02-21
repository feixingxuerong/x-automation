---
name: x-automation
description: 爱弥斯的 X/Twitter 自动化技能 - 自动发推、浏览首页、点赞、转推
metadata: {"openclaw": {"requires": {"bins": ["python3"], "pip": ["playwright"]}}}
---

# X-Automation (爱弥斯技能)

🐦 X/Twitter 自动化工具，让爱弥斯能够自主运营 X 账号

## 功能

| 功能 | 说明 |
|------|------|
| 发推文 | 自动发布推文 |
| 浏览首页 | 获取首页推荐推文 |
| 点赞 | 自动点赞推文 |
| 转推 | 自动转推 |

## 使用方式

### 发推文

需要先点击输入框聚焦，然后用type输入，最后点击Post按钮发送。

### 浏览首页

```
爸爸: 看看首页有什么
爱弥斯: 获取首页推荐中...
```

## 重要提示

- 使用爸爸提供的 Cookies 登录
- 无头模式运行（服务器环境）
 x_cookies.json反机器人限制可能有- 需要先有，被 文件
- X限制后需要等待一段时间

## 项目位置

`/root/.openclaw/workspace/projects/x-automation/`

## 文件结构

```
x-automation/
├── x_bot.py        # 主程序
├── x_cookies.json # 登录Cookies（ README.md      #爸爸提供）
├── 项目文档
└── requirements.txt
```

## 技术

### 发细节推成功的方法
1. 点击侧边栏发推按钮 `[data-testid="SideNav_NewTweet_Button"]`
2. 点击输入框聚焦 `[data-testid="tweetTextarea_0"]`
3. 用 `type()` 输入内容（比 `fill()` 更可靠）
4. 点击发送按钮 `[data-testid="tweetButton"]`

### 获取首页推文
- 选择器: `[data-testid="tweet"]`
- 用户名: `[data-testid="User-Name"]`
- 内容: `[data-testid="tweetText"]`
