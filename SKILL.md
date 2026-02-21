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

```
爸爸: 发一条推文
爱弥斯: 好的！发送什么内容？
```

### 浏览首页

```
爸爸: 看看首页有什么
爱弥斯: 获取首页推荐中...
```

## 重要提示

- 使用爸爸提供的 Cookies 登录
- 无头模式运行（服务器环境）
- 需要先有 x_cookies.json 文件

## 项目位置

`/root/.openclaw/workspace/projects/x-automation/`

## 文件结构

```
x-automation/
├── x_bot.py        # 主程序
├── x_cookies.json # 登录Cookies（爸爸提供）
├── README.md      # 项目文档
└── requirements.txt
```
