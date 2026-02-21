# X-Automation

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8+-FFD43B?style=flat&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.40+-FF69B4?style=flat&logo=microsoft)
![License](https://img.shields.io/badge/License-MIT-FF69B4)

</p>

---

## 🎯 简介

**X-Automation** 是一个基于 Playwright 的 X/Twitter 自动化工具，让 AI 能够自主运营 X 账号。

> ⚠️ **警告**：使用自动化工具存在被封号风险，请谨慎使用。

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 📝 **发推文** | 自动发布推文 |
| 📰 **首页推荐** | 获取首页推荐推文 |
| ❤️ **点赞** | 自动点赞推文 |
| 🔄 **转推** | 自动转推 |
| 👤 **关注** | 自动关注用户 |
| 🔍 **搜索** | 搜索推文 |

---

## 🚀 快速开始

### 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 准备 Cookies

1. 在浏览器登录 X/Twitter
2. 使用 Cookie-Editor 插件导出 cookies
3. 保存到 `x_cookies.json`

### 使用方法

```python
import asyncio
from x_bot import XAutomation

async def main():
    x = XAutomation()
    await x.launch(headless=True)  # 无头模式
    
    # 检查登录状态
    if await x.login_check():
        # 获取首页推荐
        timeline = await x.get_home_timeline(5)
        for t in timeline:
            print(f"@{t['author']}: {t['text'][:50]}...")
        
        # 发推
        await x.post_tweet("Hello from X-Automation! 🤖")
    
    await x.close()

asyncio.run(main())
```

---

## 📖 API 参考

### XAutomation 类

#### `__init__(cookies_file: str)`
初始化，指定 cookies 文件路径

#### `launch(headless: bool = True)`
启动浏览器

- `headless=True`: 无头模式（服务器用）
- `headless=False`: 有头模式（本地调试用）

#### `login_check() -> bool`
检查登录状态

```python
if await x.login_check():
    print("已登录")
```

#### `post_tweet(text: str) -> bool`
发布推文

```python
await x.post_tweet("这是一条测试推文!")
```

#### `get_home_timeline(count: int = 5) -> list`
获取首页推荐

```python
timeline = await x.get_home_timeline(10)
for t in timeline:
    print(f"@{t['author']}: {t['text']}")
```

#### `like_tweet() -> bool`
点赞当前页面推文

#### `retweet() -> bool`
转推当前页面推文

#### `close()`
关闭浏览器

---

## ⚠️ 注意事项

1. **账号风险**：自动化操作可能被 X 检测并封号
2. **频率限制**：不要过于频繁操作
3. **Cookies 过期**：需要定期更新 cookies
4. **遵守规则**：遵守 X 的服务条款

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📝 License

MIT License

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/feixingxuerong">爱弥斯</a>
</p>
