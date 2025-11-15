#!/usr/bin/env python3
"""
自動內容生成器 - 主程式
根據分類自動搜尋熱門事件，使用 AI 生成文章，並自動發布

使用方法：
python auto_content_generator.py --categories all --count 5 --publish
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import anthropic
import requests
from typing import List, Dict

class AutoContentGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

        # 文章分類配置
        self.categories = {
            'ai-tools': {
                'name': 'AI工具',
                'keywords': ['AI', 'ChatGPT', 'Claude', '人工智慧', '機器學習', 'AI工具'],
                'tags': ['AI', 'AI工具', '人工智慧'],
                'search_queries': [
                    'AI tools 2024',
                    'ChatGPT updates',
                    'Claude AI',
                    'Gemini AI',
                    'new AI applications'
                ]
            },
            'creativity': {
                'name': '創意思維',
                'keywords': ['創意', '設計思維', '創新', '腦力激盪', 'SCAMPER'],
                'tags': ['創意', '創新', '設計思維'],
                'search_queries': [
                    'design thinking 2024',
                    'creative innovation',
                    'brainstorming techniques',
                    'innovation methods'
                ]
            },
            'productivity': {
                'name': '生產力',
                'keywords': ['生產力', '效率', '時間管理', 'GTD', '專注'],
                'tags': ['生產力', '效率', '時間管理'],
                'search_queries': [
                    'productivity tools 2024',
                    'time management techniques',
                    'workflow optimization',
                    'productivity hacks'
                ]
            },
            'entrepreneurship': {
                'name': '創業',
                'keywords': ['創業', 'startup', '商業模式', '募資', '創新創業'],
                'tags': ['創業', 'startup', '商業'],
                'search_queries': [
                    'startup trends 2024',
                    'business innovation',
                    'entrepreneurship tips',
                    'startup funding'
                ]
            },
            'tech-trends': {
                'name': '技術趨勢',
                'keywords': ['科技', '技術', '趨勢', 'Web3', '區塊鏈'],
                'tags': ['科技', '技術', '趨勢'],
                'search_queries': [
                    'tech trends 2024',
                    'emerging technologies',
                    'future technology',
                    'tech innovations'
                ]
            },
            'personal-branding': {
                'name': '個人品牌',
                'keywords': ['個人品牌', '自媒體', '內容創作', 'LinkedIn'],
                'tags': ['個人品牌', '內容創作', '自媒體'],
                'search_queries': [
                    'personal branding 2024',
                    'content creation tips',
                    'social media strategy',
                    'building online presence'
                ]
            }
        }

    def search_trending_topics(self, category_key: str, days_back: int = 7) -> List[Dict]:
        """
        搜尋該分類的熱門話題
        使用多個來源：Google Trends API、News API、Reddit、Hacker News
        """
        print(f"🔍 搜尋 {self.categories[category_key]['name']} 的熱門話題...")

        category = self.categories[category_key]
        trending_topics = []

        # 方法 1: 使用 News API（免費版，需要 API key）
        trending_topics.extend(self._search_news_api(category))

        # 方法 2: 使用 Hacker News API（免費，無需 key）
        trending_topics.extend(self._search_hackernews(category))

        # 方法 3: 使用 Reddit API（免費，無需 key）
        trending_topics.extend(self._search_reddit(category))

        # 方法 4: 使用 Google Trends（透過 serpapi 或 pytrends）
        # trending_topics.extend(self._search_google_trends(category))

        # 去重並排序（按相關度和熱度）
        unique_topics = self._deduplicate_and_rank(trending_topics)

        return unique_topics[:5]  # 返回前 5 個最熱門的話題

    def _search_news_api(self, category: Dict) -> List[Dict]:
        """使用 News API 搜尋新聞"""
        topics = []

        # News API 需要 API key，如果沒有就跳過
        news_api_key = os.environ.get('NEWS_API_KEY')
        if not news_api_key:
            print("  ⚠️  未設定 NEWS_API_KEY，跳過 News API")
            return topics

        try:
            for query in category['search_queries'][:2]:  # 只搜尋前 2 個查詢
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': query,
                    'language': 'en',
                    'sortBy': 'popularity',
                    'pageSize': 5,
                    'apiKey': news_api_key,
                    'from': (datetime.now() - timedelta(days=7)).isoformat()
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    for article in data.get('articles', [])[:3]:
                        topics.append({
                            'title': article['title'],
                            'description': article.get('description', ''),
                            'url': article['url'],
                            'source': 'NewsAPI',
                            'published_at': article.get('publishedAt', ''),
                            'relevance': 0.8
                        })
        except Exception as e:
            print(f"  ⚠️  News API 搜尋失敗: {e}")

        return topics

    def _search_hackernews(self, category: Dict) -> List[Dict]:
        """搜尋 Hacker News 熱門文章"""
        topics = []

        try:
            # 獲取熱門文章
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                story_ids = response.json()[:30]  # 取前 30 篇

                # 獲取文章詳情
                for story_id in story_ids[:10]:  # 只檢查前 10 篇
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = requests.get(story_url, timeout=5)

                    if story_response.status_code == 200:
                        story = story_response.json()

                        # 檢查是否與分類關鍵字相關
                        title = story.get('title', '').lower()
                        if any(keyword.lower() in title for keyword in category['keywords']):
                            topics.append({
                                'title': story.get('title', ''),
                                'description': story.get('text', '')[:200],
                                'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                                'source': 'HackerNews',
                                'published_at': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                                'relevance': 0.7,
                                'score': story.get('score', 0)
                            })
        except Exception as e:
            print(f"  ⚠️  Hacker News 搜尋失敗: {e}")

        return topics

    def _search_reddit(self, category: Dict) -> List[Dict]:
        """搜尋 Reddit 熱門文章"""
        topics = []

        # 相關的 subreddit
        subreddits = {
            'ai-tools': ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT'],
            'creativity': ['creativity', 'design', 'DesignThinking'],
            'productivity': ['productivity', 'gtd', 'productivity'],
            'entrepreneurship': ['Entrepreneur', 'startups', 'smallbusiness'],
            'tech-trends': ['technology', 'Futurology', 'tech'],
            'personal-branding': ['personalbranding', 'socialmedia', 'marketing']
        }

        try:
            for subreddit in subreddits.get(list(self.categories.keys())[0], ['all'])[:2]:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {'User-Agent': 'AutoContentBot/1.0'}

                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    for post in data['data']['children'][:5]:
                        post_data = post['data']

                        # 檢查是否與分類關鍵字相關
                        title = post_data.get('title', '').lower()
                        if any(keyword.lower() in title for keyword in category['keywords']):
                            topics.append({
                                'title': post_data.get('title', ''),
                                'description': post_data.get('selftext', '')[:200],
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'source': 'Reddit',
                                'published_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                                'relevance': 0.6,
                                'score': post_data.get('score', 0)
                            })
        except Exception as e:
            print(f"  ⚠️  Reddit 搜尋失敗: {e}")

        return topics

    def _deduplicate_and_rank(self, topics: List[Dict]) -> List[Dict]:
        """去重並按相關度排序"""
        # 簡單去重（基於標題相似度）
        unique_topics = []
        seen_titles = set()

        for topic in topics:
            title_lower = topic['title'].lower()
            # 簡單的去重邏輯
            if not any(title_lower in seen or seen in title_lower for seen in seen_titles):
                unique_topics.append(topic)
                seen_titles.add(title_lower)

        # 排序（按相關度和分數）
        unique_topics.sort(key=lambda x: (x.get('relevance', 0), x.get('score', 0)), reverse=True)

        return unique_topics

    def generate_article_with_ai(self, topic: Dict, category_key: str) -> str:
        """使用 AI 生成文章"""
        if not self.client:
            print("❌ 未設定 ANTHROPIC_API_KEY，無法使用 AI 生成")
            return None

        category = self.categories[category_key]

        print(f"🤖 使用 AI 生成文章：{topic['title'][:50]}...")

        # 構建提示詞
        prompt = f"""你是一位專業的繁體中文科技部落格作家。請根據以下資訊撰寫一篇深度文章：

主題：{topic['title']}
描述：{topic.get('description', '無')}
來源連結：{topic.get('url', '無')}

文章要求：
1. 使用繁體中文
2. 字數：2000-3000 字
3. 風格：專業但易懂，有深度但不艱澀
4. 結構：
   - 引言（100-200字）：吸引讀者，說明為什麼這個主題重要
   - 核心內容（1500-2000字）：深入分析，包含實例和數據
   - 實際應用（300-500字）：如何應用到實際工作中
   - 總結與展望（200-300字）：關鍵要點和未來趨勢
5. 包含：
   - 具體的例子和案例
   - 實用的建議
   - 清晰的標題結構（使用 ##、### 標記）
   - 適當使用表格、列表來組織資訊
   - 使用 emoji 增加可讀性（但不要過度）
6. 語調：鼓勵性、實用性、前瞻性
7. 避免：過度宣傳、不實資訊、抄襲

請直接輸出完整的 Markdown 格式文章內容（不包含 front matter），從引言開始。
"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            article_content = message.content[0].text

            # 生成 front matter
            title = self._generate_title_from_content(article_content, topic['title'])
            excerpt = self._generate_excerpt_from_content(article_content)

            front_matter = f"""---
layout: single
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories:
{self._format_yaml_list([category['name']])}
tags:
{self._format_yaml_list(category['tags'])}
excerpt: "{excerpt}"
---

"""

            full_article = front_matter + article_content

            # 添加相關連結
            full_article += f"\n\n---\n\n**參考資料：**\n- [{topic['title']}]({topic['url']})\n"

            return full_article

        except Exception as e:
            print(f"❌ AI 生成文章失敗: {e}")
            return None

    def _generate_title_from_content(self, content: str, fallback: str) -> str:
        """從內容中提取或生成標題"""
        # 嘗試從內容中找到第一個標題
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line.replace('# ', '').strip()

        # 如果找不到，使用 fallback 或生成一個
        return fallback[:100]

    def _generate_excerpt_from_content(self, content: str) -> str:
        """從內容生成摘要"""
        # 取第一段非標題的文字作為摘要
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 50:
                # 取前 150 字
                excerpt = line[:150]
                if len(line) > 150:
                    excerpt += '...'
                return excerpt

        return "探索最新的技術趨勢和實用見解"

    def _format_yaml_list(self, items: List[str]) -> str:
        """格式化 YAML 列表"""
        return '\n'.join([f"  - {item}" for item in items])

    def save_article(self, content: str, category_key: str) -> str:
        """保存文章到 _posts 目錄"""
        posts_dir = Path('_posts')
        posts_dir.mkdir(exist_ok=True)

        # 生成檔案名
        today = datetime.now().strftime('%Y-%m-%d')
        # 從內容提取標題作為檔名的一部分
        title_for_filename = self._extract_title_for_filename(content)
        filename = f"{today}-{category_key}-{title_for_filename}.md"
        filepath = posts_dir / filename

        # 確保檔名唯一
        counter = 1
        while filepath.exists():
            filename = f"{today}-{category_key}-{title_for_filename}-{counter}.md"
            filepath = posts_dir / filename
            counter += 1

        # 保存文章
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 文章已保存：{filepath}")
        return str(filepath)

    def _extract_title_for_filename(self, content: str) -> str:
        """從文章內容提取標題用於檔名"""
        # 從 front matter 提取 title
        import re
        match = re.search(r'title:\s*"(.+?)"', content)
        if match:
            title = match.group(1)
            # 轉換為適合檔名的格式
            title = re.sub(r'[^\w\s-]', '', title.lower())
            title = re.sub(r'[-\s]+', '-', title)
            return title[:50]  # 限制長度

        return 'article'

    def run(self, categories: List[str], article_count: int = 1) -> List[str]:
        """運行自動內容生成"""
        print(f"\n{'='*60}")
        print("🚀 自動內容生成器")
        print(f"{'='*60}\n")

        generated_files = []

        for category_key in categories:
            if category_key not in self.categories:
                print(f"⚠️  未知分類：{category_key}，跳過")
                continue

            print(f"\n📂 處理分類：{self.categories[category_key]['name']}")
            print("-" * 60)

            # 1. 搜尋熱門話題
            topics = self.search_trending_topics(category_key)

            if not topics:
                print(f"  ⚠️  未找到相關話題，跳過此分類")
                continue

            print(f"  ✅ 找到 {len(topics)} 個熱門話題")

            # 2. 為每個話題生成文章（最多 article_count 篇）
            for i, topic in enumerate(topics[:article_count], 1):
                print(f"\n  📝 [{i}/{min(len(topics), article_count)}] 生成文章...")
                print(f"     話題：{topic['title']}")
                print(f"     來源：{topic['source']}")

                # 生成文章
                article = self.generate_article_with_ai(topic, category_key)

                if article:
                    # 保存文章
                    filepath = self.save_article(article, category_key)
                    generated_files.append(filepath)
                else:
                    print(f"  ❌ 文章生成失敗")

        return generated_files


def main():
    parser = argparse.ArgumentParser(description='自動內容生成器')
    parser.add_argument(
        '--categories',
        nargs='+',
        choices=['all', 'ai-tools', 'creativity', 'productivity',
                 'entrepreneurship', 'tech-trends', 'personal-branding'],
        default=['all'],
        help='要生成內容的分類'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='每個分類生成幾篇文章'
    )
    parser.add_argument(
        '--api-key',
        help='Anthropic API Key（或使用環境變數 ANTHROPIC_API_KEY）'
    )

    args = parser.parse_args()

    # 處理 'all' 選項
    if 'all' in args.categories:
        categories = ['ai-tools', 'creativity', 'productivity',
                      'entrepreneurship', 'tech-trends', 'personal-branding']
    else:
        categories = args.categories

    # 創建生成器
    generator = AutoContentGenerator(api_key=args.api_key)

    # 運行生成
    generated_files = generator.run(categories, args.count)

    # 總結
    print(f"\n{'='*60}")
    print("📊 生成總結")
    print(f"{'='*60}")
    print(f"✅ 成功生成 {len(generated_files)} 篇文章")
    print(f"\n生成的文章：")
    for filepath in generated_files:
        print(f"  - {filepath}")

    if generated_files:
        print(f"\n下一步：")
        print(f"1. 檢查生成的文章：ls -la _posts/")
        print(f"2. 提交到 Git：")
        print(f"   git add _posts/")
        print(f"   git commit -m '🤖 自動生成 {len(generated_files)} 篇文章'")
        print(f"   git push")
        print(f"3. GitHub Actions 會自動部署到 GitHub Pages")


if __name__ == '__main__':
    main()
