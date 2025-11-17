#!/usr/bin/env python3
"""
自動化系統監控儀表板
顯示系統運行狀態、統計數據和趨勢
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import re

class AutomationDashboard:
    def __init__(self):
        self.posts_dir = Path('_posts')
        self.stats = {
            'total_posts': 0,
            'auto_generated_posts': 0,
            'recent_7days': 0,
            'recent_30days': 0,
            'by_category': defaultdict(int),
            'by_date': defaultdict(int),
            'avg_words': 0,
            'total_words': 0
        }

    def analyze_posts(self):
        """分析所有文章"""
        if not self.posts_dir.exists():
            print("❌ 找不到 _posts 目錄")
            return

        posts = list(self.posts_dir.glob('*.md'))
        self.stats['total_posts'] = len(posts)

        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        total_words = 0

        for post in posts:
            # 檢查是否為自動生成
            with open(post, 'r', encoding='utf-8') as f:
                content = f.read()
                if '自動內容生成系統' in content or 'Auto Content Bot' in content:
                    self.stats['auto_generated_posts'] += 1

            # 統計字數
            words = len(content)
            total_words += words

            # 從檔名提取日期
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', post.name)
            if date_match:
                post_date_str = date_match.group(1)
                post_date = datetime.strptime(post_date_str, '%Y-%m-%d')

                # 統計時間範圍
                if post_date >= week_ago:
                    self.stats['recent_7days'] += 1
                if post_date >= month_ago:
                    self.stats['recent_30days'] += 1

                # 按日期統計
                self.stats['by_date'][post_date_str] += 1

            # 統計分類
            category_match = re.search(r'categories:\s*\n\s*-\s*(.+)', content)
            if category_match:
                category = category_match.group(1).strip()
                self.stats['by_category'][category] += 1

        if self.stats['total_posts'] > 0:
            self.stats['total_words'] = total_words
            self.stats['avg_words'] = total_words // self.stats['total_posts']

    def display_dashboard(self):
        """顯示儀表板"""
        print("\n" + "="*60)
        print("📊 自動化系統監控儀表板")
        print("="*60 + "\n")

        # 總覽
        print("📈 總覽")
        print("-" * 60)
        print(f"  📝 總文章數: {self.stats['total_posts']}")
        print(f"  🤖 自動生成: {self.stats['auto_generated_posts']} ({self._percentage(self.stats['auto_generated_posts'], self.stats['total_posts'])}%)")
        print(f"  📖 總字數: {self.stats['total_words']:,}")
        print(f"  📏 平均字數: {self.stats['avg_words']:,} 字/篇")
        print()

        # 時間統計
        print("📅 時間統計")
        print("-" * 60)
        print(f"  最近 7 天: {self.stats['recent_7days']} 篇")
        print(f"  最近 30 天: {self.stats['recent_30days']} 篇")
        print(f"  平均產出: {self.stats['recent_7days'] / 7:.1f} 篇/天")
        print()

        # 分類統計
        print("📂 分類統計")
        print("-" * 60)
        if self.stats['by_category']:
            sorted_categories = sorted(
                self.stats['by_category'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for category, count in sorted_categories:
                bar = "█" * int(count / max(self.stats['by_category'].values()) * 30)
                print(f"  {category:20} {count:3} {bar}")
        else:
            print("  暫無數據")
        print()

        # 最近發布
        print("📰 最近發布")
        print("-" * 60)
        recent_dates = sorted(self.stats['by_date'].items(), reverse=True)[:7]
        for date, count in recent_dates:
            print(f"  {date}: {count} 篇")
        print()

        # 預測
        self.display_predictions()

        # 建議
        self.display_recommendations()

    def display_predictions(self):
        """顯示預測"""
        print("🔮 預測與目標")
        print("-" * 60)

        if self.stats['recent_7days'] > 0:
            daily_avg = self.stats['recent_7days'] / 7

            print(f"  基於最近 7 天的平均產出：{daily_avg:.1f} 篇/天")
            print()
            print(f"  預測本月產出: {int(daily_avg * 30)} 篇")
            print(f"  預測本年產出: {int(daily_avg * 365)} 篇")
            print(f"  預測字數（年）: {int(daily_avg * 365 * self.stats['avg_words']):,} 字")
        else:
            print("  數據不足，無法預測")

        print()

    def display_recommendations(self):
        """顯示建議"""
        print("💡 系統建議")
        print("-" * 60)

        recommendations = []

        # 檢查產出頻率
        if self.stats['recent_7days'] < 7:
            recommendations.append(
                "📉 最近 7 天產出較少，建議檢查自動化工作流是否正常運行"
            )

        # 檢查分類平衡
        if self.stats['by_category']:
            max_count = max(self.stats['by_category'].values())
            min_count = min(self.stats['by_category'].values())
            if max_count > min_count * 2:
                recommendations.append(
                    "⚖️  分類不平衡，建議調整生成策略以平衡各分類"
                )

        # 檢查字數
        if self.stats['avg_words'] < 1500:
            recommendations.append(
                f"📏 平均字數 {self.stats['avg_words']} 字較少，建議提高 MIN_WORDS 設置"
            )

        # 檢查自動化比例
        auto_ratio = self._percentage(
            self.stats['auto_generated_posts'],
            self.stats['total_posts']
        )
        if auto_ratio < 50:
            recommendations.append(
                f"🤖 自動生成占比 {auto_ratio}%，可以進一步提高自動化程度"
            )

        if recommendations:
            for rec in recommendations:
                print(f"  {rec}")
        else:
            print("  ✅ 系統運行良好，無特別建議")

        print()

    def display_api_cost_estimate(self):
        """顯示 API 成本估算"""
        print("💰 成本估算")
        print("-" * 60)

        if self.stats['auto_generated_posts'] > 0:
            cost_per_article = 0.06  # USD
            total_cost = self.stats['auto_generated_posts'] * cost_per_article
            monthly_cost = (self.stats['recent_30days'] * cost_per_article) if self.stats['recent_30days'] > 0 else 0

            print(f"  累計生成: {self.stats['auto_generated_posts']} 篇")
            print(f"  累計成本: ${total_cost:.2f} (約 NT${total_cost * 30:.0f})")
            print()
            print(f"  本月生成: {self.stats['recent_30days']} 篇")
            print(f"  本月成本: ${monthly_cost:.2f} (約 NT${monthly_cost * 30:.0f})")
            print()

            if self.stats['recent_7days'] > 0:
                daily_avg = self.stats['recent_7days'] / 7
                monthly_estimate = daily_avg * 30 * cost_per_article
                print(f"  預估月成本: ${monthly_estimate:.2f} (約 NT${monthly_estimate * 30:.0f})")
        else:
            print("  暫無自動生成文章")

        print()

    def _percentage(self, part, total):
        """計算百分比"""
        if total == 0:
            return 0
        return int(part / total * 100)

    def run(self):
        """運行儀表板"""
        self.analyze_posts()
        self.display_dashboard()
        self.display_api_cost_estimate()

        # 總結
        print("="*60)
        print("💡 小提示：")
        print("  - 定期檢查儀表板以監控系統運行狀況")
        print("  - 查看 GitHub Actions 頁面了解詳細運行記錄")
        print("  - 查看 Issues 標籤為 'daily-report' 的報告")
        print("="*60)


def main():
    dashboard = AutomationDashboard()
    dashboard.run()


if __name__ == '__main__':
    main()
