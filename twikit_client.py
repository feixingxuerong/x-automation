#!/usr/bin/env python3
"""
X-Twikit: 使用 Twikit 库进行 X/Twitter 操作
无需登录，使用 Twitter 内部 API
"""

import asyncio
import os
import json
from pathlib import Path
from twikit import Client, User, Tweet


class XClient:
    """X/Twitter 客户端"""
    
    def __init__(self):
        self.cookies_file = Path(__file__).parent / "cookies.json"
        self.client = Client('zh-CN')
        self.is_logged_in = False
    
    async def login(self, username: str = None, password: str = None):
        """登录 X/Twitter"""
        if username and password:
            # 账号密码登录
            await self.client.login(username, password)
            # 保存 cookies
            await self.client.save_cookies(str(self.cookies_file))
            self.is_logged_in = True
            print(f"✅ 登录成功: {username}")
        elif self.cookies_file.exists():
            # 使用保存的 cookies
            await self.client.load_cookies(str(self.cookies_file))
            self.is_logged_in = True
            print("✅ 使用保存的 cookies 登录成功")
        else:
            print("⚠️ 未登录，需要账号密码")
    
    async def post_tweet(self, text: str) -> Tweet:
        """发布推文"""
        if not self.is_logged_in:
            print("❌ 请先登录")
            return None
        
        try:
            tweet = await self.client.create_tweet(text)
            print(f"✅ 推文已发布: {text[:50]}...")
            return tweet
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return None
    
    async def like_tweet(self, tweet_id: str) -> bool:
        """点赞推文"""
        if not self.is_logged_in:
            print("❌ 请先登录")
            return False
        
        try:
            await self.client.favorite_tweet(tweet_id)
            print(f"❤️ 已点赞: {tweet_id}")
            return True
        except Exception as e:
            print(f"❌ 点赞失败: {e}")
            return False
    
    async def retweet(self, tweet_id: str) -> bool:
        """转推"""
        if not self.is_logged_in:
            print("❌ 请先登录")
            return False
        
        try:
            await self.client.retweet(tweet_id)
            print(f"🔄 已转推: {tweet_id}")
            return True
        except Exception as e:
            print(f"❌ 转推失败: {e}")
            return False
    
    async def follow(self, username: str) -> bool:
        """关注用户"""
        try:
            await self.client.follow(username)
            print(f"✅ 已关注: @{username}")
            return True
        except Exception as e:
            print(f"❌ 关注失败: {e}")
            return False
    
    async def search(self, query: str, count: int = 10) -> list:
        """搜索推文"""
        try:
            tweets = await self.client.search(query, count)
            results = []
            for tweet in tweets:
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'author': tweet.user.name,
                    'username': tweet.user.screen_name,
                    'created_at': tweet.created_at
                })
            print(f"🔍 找到 {len(results)} 条结果")
            return results
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    async def get_user_tweets(self, username: str, count: int = 10) -> list:
        """获取用户推文"""
        try:
            user = await self.client.get_user(username)
            tweets = await user.get_tweets(count)
            results = []
            for tweet in tweets:
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at
                })
            print(f"📰 获取 @{username} 的 {len(results)} 条推文")
            return results
        except Exception as e:
            print(f"❌ 获取失败: {e}")
            return []
    
    async def get_home_timeline(self, count: int = 20) -> list:
        """获取首页时间线"""
        try:
            tweets = await self.client.get_timeline(count)
            results = []
            for tweet in tweets:
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'author': tweet.user.name,
                    'username': tweet.user.screen_name,
                    'created_at': tweet.created_at
                })
            print(f"📰 获取时间线 {len(results)} 条推文")
            return results
        except Exception as e:
            print(f"❌ 获取时间线失败: {e}")
            return []


async def main():
    """测试函数"""
    client = XClient()
    
    # 尝试登录（使用 cookies 或账号密码）
    # await client.login("username", "password")
    await client.login()  # 使用 cookies
    
    # 测试发推
    # await client.post_tweet("测试推文 from Twikit! 🤖")
    
    # 测试获取时间线
    timeline = await client.get_home_timeline(5)
    for i, tweet in enumerate(timeline, 1):
        print(f"{i}. @{tweet['username']}: {tweet['text'][:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
