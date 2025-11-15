#!/usr/bin/env python3
"""
自動修復腳本
自動修復常見的網站問題
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import yaml

class AutoFixer:
    def __init__(self):
        self.fixes = []
        self.failed_fixes = []

    def scan_issues(self):
        """掃描所有問題"""
        print("🔍 掃描問題...")

        issues = []

        # 掃描文章中的常見問題
        issues.extend(self.scan_markdown_issues())

        # 掃描圖片問題
        issues.extend(self.scan_image_issues())

        # 掃描連結問題
        issues.extend(self.scan_link_issues())

        return issues

    def scan_markdown_issues(self):
        """掃描 Markdown 文件的問題"""
        issues = []
        posts_dir = Path('_posts')

        if not posts_dir.exists():
            return issues

        for md_file in posts_dir.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 檢查 front matter
            if not content.startswith('---'):
                issues.append({
                    'type': 'missing_front_matter',
                    'file': str(md_file),
                    'fixable': True
                })

            # 檢查未完成的 TODO
            todo_count = content.count('[ ] TODO')
            if todo_count > 0:
                issues.append({
                    'type': 'unfinished_todos',
                    'file': str(md_file),
                    'count': todo_count,
                    'fixable': False  # 需要人工處理
                })

            # 檢查重複的空行
            if '\n\n\n' in content:
                issues.append({
                    'type': 'excessive_blank_lines',
                    'file': str(md_file),
                    'fixable': True
                })

            # 檢查行尾空格
            lines_with_trailing_space = sum(1 for line in content.split('\n') if line.endswith(' '))
            if lines_with_trailing_space > 0:
                issues.append({
                    'type': 'trailing_spaces',
                    'file': str(md_file),
                    'count': lines_with_trailing_space,
                    'fixable': True
                })

        return issues

    def scan_image_issues(self):
        """掃描圖片相關問題"""
        issues = []
        posts_dir = Path('_posts')
        images_dir = Path('assets/images')

        if not posts_dir.exists():
            return issues

        for md_file in posts_dir.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找圖片引用
            img_pattern = r'!\[.*?\]\((.*?)\)'
            images = re.findall(img_pattern, content)

            for img_path in images:
                # 跳過外部圖片
                if img_path.startswith(('http://', 'https://')):
                    continue

                # 檢查圖片是否存在
                full_path = Path(img_path.lstrip('/'))
                if not full_path.exists():
                    issues.append({
                        'type': 'missing_image',
                        'file': str(md_file),
                        'image': img_path,
                        'fixable': False  # 圖片真的遺失了，無法自動修復
                    })

                # 檢查圖片大小
                elif full_path.exists():
                    size_mb = full_path.stat().st_size / (1024 * 1024)
                    if size_mb > 1:  # 大於 1MB
                        issues.append({
                            'type': 'large_image',
                            'file': str(md_file),
                            'image': img_path,
                            'size_mb': round(size_mb, 2),
                            'fixable': True  # 可以壓縮
                        })

        return issues

    def scan_link_issues(self):
        """掃描連結問題"""
        issues = []
        posts_dir = Path('_posts')

        if not posts_dir.exists():
            return issues

        for md_file in posts_dir.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找內部連結
            link_pattern = r'\[.*?\]\((.*?)\)'
            links = re.findall(link_pattern, content)

            for link in links:
                # 只檢查內部連結
                if link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    continue

                # 移除錨點
                link_path = link.split('#')[0]
                if not link_path:
                    continue

                # 檢查文件是否存在
                if link_path.startswith('/'):
                    full_path = Path(link_path.lstrip('/'))
                else:
                    full_path = md_file.parent / link_path

                if not full_path.exists():
                    issues.append({
                        'type': 'broken_link',
                        'file': str(md_file),
                        'link': link,
                        'fixable': True  # 可以嘗試修復
                    })

        return issues

    def fix_issues(self, issues):
        """修復問題"""
        print(f"\n🔧 開始修復 {len([i for i in issues if i.get('fixable', False)])} 個可修復的問題...")

        for issue in issues:
            if not issue.get('fixable', False):
                self.failed_fixes.append({
                    'issue': issue,
                    'reason': '需要人工處理'
                })
                continue

            try:
                if issue['type'] == 'excessive_blank_lines':
                    self.fix_excessive_blank_lines(issue)

                elif issue['type'] == 'trailing_spaces':
                    self.fix_trailing_spaces(issue)

                elif issue['type'] == 'missing_front_matter':
                    self.fix_missing_front_matter(issue)

                elif issue['type'] == 'broken_link':
                    self.fix_broken_link(issue)

                elif issue['type'] == 'large_image':
                    self.fix_large_image(issue)

            except Exception as e:
                self.failed_fixes.append({
                    'issue': issue,
                    'reason': str(e)
                })

        return self.fixes

    def fix_excessive_blank_lines(self, issue):
        """修復過多的空行"""
        file_path = Path(issue['file'])

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 將 3+ 個換行替換為 2 個
        new_content = re.sub(r'\n\n\n+', '\n\n', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        self.fixes.append({
            'type': issue['type'],
            'file': str(file_path),
            'action': '移除過多的空行'
        })

    def fix_trailing_spaces(self, issue):
        """修復行尾空格"""
        file_path = Path(issue['file'])

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 移除每行的尾部空格
        new_lines = [line.rstrip() + '\n' if line.endswith('\n') else line.rstrip() for line in lines]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        self.fixes.append({
            'type': issue['type'],
            'file': str(file_path),
            'action': f'移除 {issue["count"]} 行的尾部空格'
        })

    def fix_missing_front_matter(self, issue):
        """修復缺失的 front matter"""
        file_path = Path(issue['file'])

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 從檔名提取日期
        filename = file_path.stem
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')

        # 從內容提取第一個標題作為 title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename.replace('-', ' ').title()

        # 創建基本的 front matter
        front_matter = {
            'layout': 'single',
            'title': title,
            'date': f'{date} 09:00:00 +0800',
            'categories': ['未分類'],
            'tags': []
        }

        # 添加 front matter
        fm_str = '---\n' + yaml.dump(front_matter, allow_unicode=True) + '---\n\n'
        new_content = fm_str + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        self.fixes.append({
            'type': issue['type'],
            'file': str(file_path),
            'action': '添加基本的 front matter'
        })

    def fix_broken_link(self, issue):
        """嘗試修復損壞的連結"""
        file_path = Path(issue['file'])
        broken_link = issue['link']

        # 簡單的修復策略：如果是相對路徑，嘗試添加 .html
        # 這只是一個示例，實際可能需要更複雜的邏輯

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 嘗試幾種可能的修復
        possible_fixes = [
            broken_link + '.html',
            broken_link + '/index.html',
            broken_link.replace(' ', '-'),
        ]

        fixed_link = None
        for fix in possible_fixes:
            if Path(fix.lstrip('/')).exists():
                fixed_link = fix
                break

        if fixed_link:
            new_content = content.replace(f']({broken_link})', f']({fixed_link})')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.fixes.append({
                'type': issue['type'],
                'file': str(file_path),
                'action': f'修復連結: {broken_link} -> {fixed_link}'
            })
        else:
            self.failed_fixes.append({
                'issue': issue,
                'reason': '找不到正確的連結目標'
            })

    def fix_large_image(self, issue):
        """標記需要壓縮的大圖片"""
        # 這裡只是標記，實際壓縮由其他工具處理
        self.failed_fixes.append({
            'issue': issue,
            'reason': '需要使用圖片壓縮工具處理'
        })

def main():
    import argparse

    parser = argparse.ArgumentParser(description='自動修復網站問題')
    parser.add_argument('action', choices=['scan', 'fix'], help='操作: scan 或 fix')

    args = parser.parse_args()

    fixer = AutoFixer()

    if args.action == 'scan':
        # 掃描問題
        issues = fixer.scan_issues()

        result = {
            'total_issues': len(issues),
            'fixable_issues': len([i for i in issues if i.get('fixable', False)]),
            'issues': issues
        }

        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == 'fix':
        # 掃描並修復
        issues = fixer.scan_issues()
        fixes = fixer.fix_issues(issues)

        result = {
            'total_issues': len(issues),
            'fixed_count': len(fixes),
            'failed_count': len(fixer.failed_fixes),
            'fixed_issues': fixes,
            'failed_issues': fixer.failed_fixes
        }

        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
