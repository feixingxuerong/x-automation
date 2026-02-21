#!/usr/bin/env python3
"""
X-Automation: Playwright Twitter/X 自动化工具
让爱弥斯能够自主运营 X 账号

支持：
- 发推文
- 浏览首页推荐
- 点赞/转推
- 搜索
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright


class XAutomation:
    """X/Twitter 自动化操作类"""
    
    def __init__(self, cookies_file: str = None):
        self.cookies_file = cookies_file or os.path.join(os.path.dirname(__file__), "x_cookies.json")
        self.browser = None
        self.context = None
        self.page = None
    
    def _fix_cookies(self, cookies):
        """修复 cookies 格式"""
        fixed = []
        for c in cookies:
            domain = c['domain']
            if domain == '.x.com':
                domain = 'x.com'
            
            same_site = c.get('sameSite')
            if same_site == 'no_restriction':
                same_site = 'None'
            elif same_site is None or same_site == 'lax':
                same_site = 'Lax'
            
            fixed.append({
                'name': c['name'],
                'value': c['value'],
                'domain': domain,
                'path': c.get('path', '/'),
                'expires': c.get('expirationDate', -1),
                'httpOnly': c.get('httpOnly', False),
                'secure': c.get('secure', True),
                'sameSite': same_site
            })
        return fixed
    
    async def launch(self, headless: bool = True):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720}
        )
        self.page = await self.context.new_page()
        
        # 加载 cookies
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file) as f:
                cookies = json.load(f)
            fixed_cookies = self._fix_cookies(cookies)
            await self.context.add_cookies(fixed_cookies)
            print(f"✅ Cookies 已加载")
        
        print(f"✅ 浏览器已启动 (headless={headless})")
        return self
    
    async def login_check(self) -> bool:
        """检查登录状态"""
        await self.page.goto("https://x.com/home", timeout=15000)
        await self.page.wait_for_timeout(3000)
        
        try:
            await self.page.wait_for_selector('[data-testid="SideNav_NewTweet_Button"]', timeout=5000)
            return True
        except:
            return False
    
    async def post_tweet(self, text: str) -> bool:
        """发布推文"""
        try:
            # 点击发推按钮打开弹窗
            await self.page.click('[data-testid="SideNav_NewTweet_Button"]')
            await self.page.wait_for_timeout(3000)
            
            # 先点击输入框聚焦
            await self.page.click('[data-testid="tweetTextarea_0"]')
            await self.page.wait_for_timeout(1500)
            
            # 用 type 输入内容（比 fill 更可靠）
            await self.page.type('[data-testid="tweetTextarea_0"]', text, delay=100)
            await self.page.wait_for_timeout(3000)
            
            # 等待发送按钮出现并点击
            btn = await self.page.wait_for_selector('[data-testid="tweetButton"]', timeout=5000)
            await btn.click()
            await self.page.wait_for_timeout(5000)
            
            print(f"✅ 推文已发布: {text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False
    
    async def get_home_timeline(self, count: int = 5) -> list:
        """获取首页推荐"""
        await self.page.goto("https://x.com/home", timeout=15000)
        await self.page.wait_for_timeout(5000)
        
        articles = await self.page.query_selector_all('article')
        results = []
        
        for article in articles[:count]:
            try:
                # 获取用户名
                user_elem = await article.query_selector('[dir="ltr"]')
                username = await user_elem.inner_text() if user_elem else '未知'
                
                # 获取内容
                text_parts = []
                spans = await article.query_selector_all('span')
                for span in spans:
                    text = await span.inner_text()
                    if len(text) > 20 and len(text) < 300:
                        text_parts.append(text)
                
                text = text_parts[0] if text_parts else '[媒体内容]'
                
                results.append({
                    'author': username,
                    'text': text
                })
            except:
                pass
        
        return results
    
    async def like_tweet(self, article=None) -> bool:
        """点赞推文"""
        try:
            if article:
                await article.click('[data-testid="like"]')
            else:
                await self.page.click('[data-testid="like"]')
            await self.page.wait_for_timeout(500)
            print("❤️ 已点赞")
            return True
        except Exception as e:
            print(f"❌ 点赞失败: {e}")
            return False
    
    async def retweet(self, article=None) -> bool:
        """转推"""
        try:
            if article:
                await article.click('[data-testid="retweet"]')
            else:
                await self.page.click('[data-testid="retweet"]')
            await self.page.wait_for_timeout(500)
            await self.page.click('[data-testid="retweetConfirm"]')
            await self.page.wait_for_timeout(1000)
            print("🔄 已转推")
            return True
        except Exception as e:
            print(f"❌ 转推失败: {e}")
            return False
    
    async def follow_user(self, username: str) -> bool:
        """关注用户"""
        try:
            # 访问用户主页
            await self.page.goto(f"https://x.com/{username}", timeout=15000)
            await self.page.wait_for_timeout(5000)
            
            # 点击关注按钮
            follow_btn = await self.page.query_selector('[data-testid*="follow"]')
            if follow_btn:
                await follow_btn.click()
                await self.page.wait_for_timeout(2000)
                print(f"✅ 已关注 @{username}")
                return True
            else:
                # 可能已经关注了，找取消关注按钮
                unfollow_btn = await self.page.query_selector('[data-testid*="unfollow"]')
                if unfollow_btn:
                    print(f"⚠️ 已关注 @{username}")
                    return True
                print(f"❌ 未找到关注按钮")
                return False
        except Exception as e:
            print(f"❌ 关注失败: {e}")
            return False
    
    async def unfollow_user(self, username: str) -> bool:
        """取消关注用户"""
        try:
            # 访问用户主页
            await self.page.goto(f"https://x.com/{username}", timeout=15000)
            await self.page.wait_for_timeout(5000)
            
            # 点击取消关注按钮
            unfollow_btn = await self.page.query_selector('[data-testid*="unfollow"]')
            if unfollow_btn:
                await unfollow_btn.click()
                await self.page.wait_for_timeout(1000)
                
                # 确认取消关注
                confirm_btn = await self.page.query_selector('[data-testid*="confirmUnfollow"]')
                if confirm_btn:
                    await confirm_btn.click()
                    await self.page.wait_for_timeout(2000)
                
                print(f"✅ 已取消关注 @{username}")
                return True
            else:
                print(f"⚠️ 未找到取消关注按钮（可能未关注）")
                return False
        except Exception as e:
            print(f"❌ 取消关注失败: {e}")
            return False
    
    async def reply_to_tweet(self, tweet_url: str, reply_text: str) -> bool:
        """回复推文"""
        try:
            # 访问推文页面
            await self.page.goto(tweet_url, timeout=15000)
            await self.page.wait_for_timeout(5000)
            
            # 点击回复按钮
            reply_btn = await self.page.query_selector('[data-testid="reply"]')
            if reply_btn:
                await reply_btn.click()
                await self.page.wait_for_timeout(3000)
                
                # 点击输入框聚焦
                await self.page.click('[data-testid="tweetTextarea_0"]')
                await self.page.wait_for_timeout(1500)
                
                # 输入回复内容
                await self.page.type('[data-testid="tweetTextarea_0"]', reply_text, delay=100)
                await self.page.wait_for_timeout(2000)
                
                # 点击发送
                send_btn = await self.page.query_selector('[data-testid="tweetButton"]')
                if send_btn:
                    await send_btn.click()
                    await self.page.wait_for_timeout(5000)
                    print(f"✅ 已回复: {reply_text[:30]}...")
                    return True
            
            print("❌ 未找到回复按钮")
            return False
        except Exception as e:
            print(f"❌ 回复失败: {e}")
            return False
    
    async def get_notifications(self, count: int = 10) -> list:
        """获取通知"""
        try:
            await self.page.goto("https://x.com/notifications", timeout=15000)
            await self.page.wait_for_timeout(8000)
            
            articles = await self.page.query_selector_all('article')
            results = []
            
            for article in articles[:count]:
                try:
                    # 获取用户名
                    name_elem = await article.query_selector('[data-testid="User-Name"]')
                    username_elem = await article.query_selector('[dir="ltr"]')
                    
                    # 获取内容
                    text_elem = await article.query_selector('[data-testid="tweetText"]')
                    
                    # 获取头像链接
                    avatar = await article.query_selector('[data-testid="UserAvatar"]')
                    
                    name = await name_elem.inner_text() if name_elem else ''
                    username = await username_elem.inner_text() if username_elem else ''
                    text = await text_elem.inner_text() if text_elem else ''
                    
                    # 提取用户名（去掉多余信息）
                    if '@' in username:
                        username = username.split('@')[-1].split()[0]
                    elif '·' in username:
                        username = username.split('·')[0].strip()
                    
                    # 判断通知类型
                    notif_type = 'other'
                    if 'liked' in username.lower():
                        notif_type = 'like'
                    elif 'replied' in username.lower() or '回复' in text:
                        notif_type = 'reply'
                    elif 'followed' in username.lower():
                        notif_type = 'follow'
                    
                    results.append({
                        'type': notif_type,
                        'user': username,
                        'text': text,
                        'element': article
                    })
                except:
                    pass
            
            print(f"📬 获取到 {len(results)} 条通知")
            return results
        except Exception as e:
            print(f"❌ 获取通知失败: {e}")
            return []
    
    async def reply_to_notification(self, notification, reply_text: str) -> bool:
        """回复通知中的推文"""
        try:
            # 点击通知进入详情
            article = notification.get('element')
            if article:
                await article.click()
                await self.page.wait_for_timeout(5000)
                
                # 下滑找到评论
                await self.page.evaluate('window.scrollBy(0, 350)')
                await self.page.wait_for_timeout(2000)
                
                # 用JS点击评论下方的reply按钮
                await self.page.evaluate('''
                    () => {
                        const buttons = document.querySelectorAll('[data-testid="reply"]');
                        if (buttons.length > 1) {
                            buttons[1].click();
                        } else if (buttons.length > 0) {
                            buttons[0].click();
                        }
                    }
                ''')
                await self.page.wait_for_timeout(3000)
                
                # 输入回复内容
                await self.page.click('[data-testid="tweetTextarea_0"]')
                await self.page.wait_for_timeout(1500)
                await self.page.type('[data-testid="tweetTextarea_0"]', reply_text, delay=100)
                await self.page.wait_for_timeout(2000)
                
                # 点击输入窗口的 Reply 按钮发送
                await self.page.evaluate('document.querySelector(\'[data-testid="tweetButtonInline"]\').click()')
                
                await self.page.wait_for_timeout(5000)
                print(f"✅ 已回复 @{notification['user']}: {reply_text[:30]}...")
                return True
            
            return False
        except Exception as e:
            print(f"❌ 回复失败: {e}")
            return False
    
    async def get_mentions(self, count: int = 10) -> list:
        """获取@我的提及"""
        try:
            await self.page.goto("https://x.com/i/connect", timeout=15000)
            await self.page.wait_for_timeout(5000)
            
            # 获取提及列表
            mentions = await self.page.query_selector_all('[data-testid="cellInnerDiv"]')
            results = []
            
            for mention in mentions[:count]:
                try:
                    user_elem = await mention.query_selector('[dir="ltr"]')
                    text_elem = await mention.query_selector('[data-testid="tweetText"]')
                    
                    user = await user_elem.inner_text() if user_elem else ''
                    text = await text_elem.inner_text() if text_elem else ''
                    
                    if user or text:
                        results.append({
                            'user': user,
                            'text': text
                        })
                except:
                    pass
            
            return results
        except Exception as e:
            print(f"❌ 获取提及失败: {e}")
            return []
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🔒 浏览器已关闭")


async def main():
    """测试函数"""
    x = XAutomation()
    await x.launch(headless=True)
    
    # 检查登录
    if await x.login_check():
        print("✅ 已登录!")
        
        # 获取首页推荐
        timeline = await x.get_home_timeline(5)
        print(f"\n📰 首页推荐 ({len(timeline)} 条):")
        for i, t in enumerate(timeline, 1):
            print(f"{i}. @{t['author']}: {t['text'][:50]}...")
    else:
        print("❌ 未登录")
    
    await x.close()


if __name__ == "__main__":
    asyncio.run(main())
