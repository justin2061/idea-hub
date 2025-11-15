#!/usr/bin/env python3
"""
內容質量測試腳本
檢查文章的 front matter、格式、必要欄位等
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import yaml

class ContentTester:
    def __init__(self, posts_dir="_posts"):
        self.posts_dir = Path(posts_dir)
        self.errors = []
        self.warnings = []
        self.stats = {
            'total_posts': 0,
            'total_words': 0,
            'avg_words': 0
        }

    def extract_front_matter(self, content):
        """提取 front matter"""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            try:
                front_matter = yaml.safe_load(match.group(1))
                body = content[match.end():]
                return front_matter, body
            except yaml.YAMLError as e:
                return None, content

        return {}, content

    def validate_front_matter(self, file_path, front_matter):
        """驗證 front matter"""
        required_fields = ['title', 'date', 'categories']
        recommended_fields = ['layout', 'excerpt', 'tags']

        issues = []

        # 檢查必要欄位
        for field in required_fields:
            if field not in front_matter:
                issues.append({
                    'level': 'error',
                    'field': field,
                    'message': f'缺少必要欄位: {field}'
                })

        # 檢查推薦欄位
        for field in recommended_fields:
            if field not in front_matter:
                issues.append({
                    'level': 'warning',
                    'field': field,
                    'message': f'缺少推薦欄位: {field}'
                })

        # 驗證特定欄位
        if 'title' in front_matter:
            title = front_matter['title']
            if len(title) < 10:
                issues.append({
                    'level': 'warning',
                    'field': 'title',
                    'message': f'標題太短（{len(title)} 字），建議至少 10 字'
                })
            if len(title) > 100:
                issues.append({
                    'level': 'warning',
                    'field': 'title',
                    'message': f'標題太長（{len(title)} 字），建議不超過 100 字'
                })

        if 'excerpt' in front_matter:
            excerpt = front_matter['excerpt']
            if len(excerpt) < 50:
                issues.append({
                    'level': 'warning',
                    'field': 'excerpt',
                    'message': f'摘要太短（{len(excerpt)} 字），建議 50-200 字'
                })
            if len(excerpt) > 200:
                issues.append({
                    'level': 'warning',
                    'field': 'excerpt',
                    'message': f'摘要太長（{len(excerpt)} 字），建議 50-200 字'
                })

        if 'date' in front_matter:
            try:
                # 驗證日期格式
                date_str = str(front_matter['date'])
                datetime.strptime(date_str.split()[0], '%Y-%m-%d')
            except ValueError:
                issues.append({
                    'level': 'error',
                    'field': 'date',
                    'message': f'日期格式錯誤: {front_matter["date"]}'
                })

        if 'categories' in front_matter:
            categories = front_matter['categories']
            if not isinstance(categories, list) or len(categories) == 0:
                issues.append({
                    'level': 'warning',
                    'field': 'categories',
                    'message': '分類應該是非空列表'
                })

        return issues

    def validate_content(self, file_path, body):
        """驗證文章內容"""
        issues = []

        # 計算字數
        word_count = len(body)

        if word_count < 500:
            issues.append({
                'level': 'warning',
                'field': 'content',
                'message': f'內容太短（{word_count} 字），建議至少 500 字'
            })

        # 檢查圖片
        img_pattern = r'!\[.*?\]\((.*?)\)'
        images = re.findall(img_pattern, body)

        for img in images:
            if img.startswith('http'):
                # 外部圖片，建議本地化
                issues.append({
                    'level': 'warning',
                    'field': 'images',
                    'message': f'使用外部圖片: {img}，建議使用本地圖片'
                })

        # 檢查連結
        link_pattern = r'\[.*?\]\((.*?)\)'
        links = re.findall(link_pattern, body)

        # 排除圖片
        links = [l for l in links if not any(l.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg'])]

        if len(links) < 2:
            issues.append({
                'level': 'warning',
                'field': 'links',
                'message': '文章中連結太少，建議添加相關文章連結'
            })

        # 檢查標題層級
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        headings = re.findall(heading_pattern, body, re.MULTILINE)

        if len(headings) == 0:
            issues.append({
                'level': 'warning',
                'field': 'structure',
                'message': '文章缺少標題結構'
            })
        else:
            # 檢查標題層級是否合理（應該從 ## 開始，不要跳級）
            levels = [len(h[0]) for h in headings]
            if levels[0] == 1:
                issues.append({
                    'level': 'warning',
                    'field': 'structure',
                    'message': '文章標題應從 ## 開始（# 保留給文章標題）'
                })

        # 檢查代碼塊
        code_blocks = re.findall(r'```(\w*)\n(.*?)\n```', body, re.DOTALL)

        for lang, code in code_blocks:
            if not lang:
                issues.append({
                    'level': 'warning',
                    'field': 'code',
                    'message': '代碼塊缺少語言標識'
                })

        return issues, word_count

    def run_tests(self):
        """運行所有測試"""
        print("🔍 開始檢查文章內容...")

        if not self.posts_dir.exists():
            print(f"❌ 找不到文章目錄: {self.posts_dir}")
            sys.exit(1)

        post_files = list(self.posts_dir.glob("*.md"))
        self.stats['total_posts'] = len(post_files)

        print(f"📄 找到 {len(post_files)} 篇文章")

        total_words = 0

        for post_file in post_files:
            relative_path = post_file.relative_to(Path.cwd())

            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                front_matter, body = self.extract_front_matter(content)

                # 驗證 front matter
                fm_issues = self.validate_front_matter(post_file, front_matter)

                # 驗證內容
                content_issues, word_count = self.validate_content(post_file, body)

                total_words += word_count

                # 收集問題
                all_issues = fm_issues + content_issues

                for issue in all_issues:
                    issue['file'] = str(relative_path)

                    if issue['level'] == 'error':
                        self.errors.append(issue)
                    else:
                        self.warnings.append(issue)

            except Exception as e:
                self.errors.append({
                    'file': str(relative_path),
                    'level': 'error',
                    'field': 'file',
                    'message': f'讀取文件失敗: {e}'
                })

        # 計算統計
        if self.stats['total_posts'] > 0:
            self.stats['total_words'] = total_words
            self.stats['avg_words'] = total_words // self.stats['total_posts']

        # 生成報告
        self.generate_report()

    def generate_report(self):
        """生成測試報告"""
        print("\n" + "="*60)
        print("📊 內容質量報告")
        print("="*60)

        print(f"\n📈 統計:")
        print(f"  - 總文章數: {self.stats['total_posts']}")
        print(f"  - 總字數: {self.stats['total_words']:,}")
        print(f"  - 平均字數: {self.stats['avg_words']:,}")

        print(f"\n📋 檢查結果:")
        print(f"  - 錯誤: {len(self.errors)}")
        print(f"  - 警告: {len(self.warnings)}")

        if self.errors:
            print(f"\n❌ 錯誤 ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - [{error['file']}] {error['field']}: {error['message']}")

        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)}):")
            # 只顯示前 20 個警告
            for warning in self.warnings[:20]:
                print(f"  - [{warning['file']}] {warning['field']}: {warning['message']}")
            if len(self.warnings) > 20:
                print(f"  ... 還有 {len(self.warnings) - 20} 個警告")

        # 保存詳細報告
        report_dir = Path('_tests/reports')
        report_dir.mkdir(parents=True, exist_ok=True)

        report_file = report_dir / 'content_quality.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'stats': self.stats,
                'errors': self.errors,
                'warnings': self.warnings
            }, f, indent=2, ensure_ascii=False)

        print(f"\n📄 詳細報告已保存到: {report_file}")

        # 如果有錯誤，失敗退出
        if self.errors:
            print("\n❌ 發現錯誤，測試失敗")
            sys.exit(1)
        elif self.warnings:
            print("\n⚠️  發現警告，但測試通過")
            sys.exit(0)
        else:
            print("\n🎉 所有檢查都通過！")
            sys.exit(0)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='檢查文章內容質量')
    parser.add_argument('--posts-dir', default='_posts', help='文章目錄')

    args = parser.parse_args()

    tester = ContentTester(args.posts_dir)
    tester.run_tests()

if __name__ == '__main__':
    main()
