#!/usr/bin/env python3
"""
連結測試腳本
檢查網站中的所有內部和外部連結是否有效
"""

import os
import sys
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from collections import defaultdict

class LinkTester:
    def __init__(self, site_dir="_site"):
        self.site_dir = Path(site_dir)
        self.base_url = "/"
        self.internal_links = set()
        self.external_links = set()
        self.broken_links = []
        self.warnings = []

    def find_all_html_files(self):
        """找到所有 HTML 文件"""
        return list(self.site_dir.rglob("*.html"))

    def extract_links(self, html_file):
        """從 HTML 文件提取所有連結"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            links = []

            # 提取 <a> 標籤的 href
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                if href:
                    links.append(('a', href, tag.get_text(strip=True)[:50]))

            # 提取 <img> 標籤的 src
            for tag in soup.find_all('img', src=True):
                src = tag['src']
                if src:
                    links.append(('img', src, tag.get('alt', '')[:50]))

            # 提取 <link> 標籤的 href（CSS 等）
            for tag in soup.find_all('link', href=True):
                href = tag['href']
                if href:
                    links.append(('link', href, tag.get('rel', [''])[0]))

            # 提取 <script> 標籤的 src
            for tag in soup.find_all('script', src=True):
                src = tag['src']
                if src:
                    links.append(('script', src, ''))

            return links

        except Exception as e:
            self.warnings.append(f"解析 {html_file} 時出錯: {e}")
            return []

    def is_internal_link(self, url):
        """判斷是否為內部連結"""
        parsed = urlparse(url)
        return not parsed.netloc or parsed.netloc in ['localhost', '127.0.0.1']

    def normalize_path(self, url, current_file):
        """標準化路徑"""
        # 移除錨點
        url = url.split('#')[0]

        # 跳過特殊協議
        if url.startswith(('mailto:', 'tel:', 'javascript:')):
            return None

        # 處理絕對路徑
        if url.startswith('/'):
            return self.site_dir / url.lstrip('/')

        # 處理相對路徑
        if not url.startswith(('http://', 'https://')):
            current_dir = current_file.parent
            relative_path = (current_dir / url).resolve()
            return relative_path

        return url

    def check_internal_link(self, link_path):
        """檢查內部連結是否存在"""
        if isinstance(link_path, str):
            # 外部連結，稍後處理
            return True

        # 檢查文件是否存在
        if link_path.exists():
            return True

        # 嘗試添加 .html
        if link_path.with_suffix('.html').exists():
            return True

        # 嘗試 index.html
        if link_path.is_dir():
            index_path = link_path / 'index.html'
            if index_path.exists():
                return True

        return False

    def check_external_link(self, url, timeout=10):
        """檢查外部連結是否可訪問"""
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code < 400
        except requests.RequestException:
            # 如果 HEAD 失敗，嘗試 GET
            try:
                response = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
                return response.status_code < 400
            except:
                return False

    def run_tests(self, check_external=False):
        """運行所有測試"""
        print("🔍 開始檢查連結...")

        html_files = self.find_all_html_files()
        print(f"📄 找到 {len(html_files)} 個 HTML 文件")

        # 收集所有連結
        all_links = defaultdict(list)

        for html_file in html_files:
            links = self.extract_links(html_file)
            relative_path = html_file.relative_to(self.site_dir)

            for link_type, url, text in links:
                normalized = self.normalize_path(url, html_file)

                if normalized is None:
                    continue

                if isinstance(normalized, str):
                    # 外部連結
                    self.external_links.add(normalized)
                    all_links[normalized].append({
                        'file': str(relative_path),
                        'type': link_type,
                        'text': text
                    })
                else:
                    # 內部連結
                    self.internal_links.add(normalized)
                    all_links[normalized].append({
                        'file': str(relative_path),
                        'type': link_type,
                        'text': text
                    })

        # 檢查內部連結
        print(f"\n🔗 檢查 {len(self.internal_links)} 個內部連結...")
        for link in self.internal_links:
            if not self.check_internal_link(link):
                sources = all_links[link]
                self.broken_links.append({
                    'type': 'internal',
                    'url': str(link),
                    'sources': sources
                })

        # 檢查外部連結（可選）
        if check_external:
            print(f"\n🌐 檢查 {len(self.external_links)} 個外部連結...")
            for i, link in enumerate(self.external_links, 1):
                print(f"  [{i}/{len(self.external_links)}] {link[:60]}...")
                if not self.check_external_link(link):
                    sources = all_links[link]
                    self.broken_links.append({
                        'type': 'external',
                        'url': link,
                        'sources': sources
                    })

        # 生成報告
        self.generate_report()

    def generate_report(self):
        """生成測試報告"""
        print("\n" + "="*60)
        print("📊 連結測試報告")
        print("="*60)

        print(f"\n✅ 總計:")
        print(f"  - 內部連結: {len(self.internal_links)}")
        print(f"  - 外部連結: {len(self.external_links)}")
        print(f"  - 損壞連結: {len(self.broken_links)}")

        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.broken_links:
            print(f"\n❌ 損壞的連結 ({len(self.broken_links)}):")
            for i, broken in enumerate(self.broken_links, 1):
                print(f"\n  {i}. [{broken['type']}] {broken['url']}")
                print(f"     出現在以下文件:")
                for source in broken['sources'][:5]:  # 只顯示前 5 個
                    print(f"     - {source['file']} ({source['type']}): {source['text']}")
                if len(broken['sources']) > 5:
                    print(f"     ... 還有 {len(broken['sources']) - 5} 個")

            # 保存詳細報告
            report_dir = Path('_tests/reports')
            report_dir.mkdir(parents=True, exist_ok=True)

            report_file = report_dir / 'broken_links.json'
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'total_internal': len(self.internal_links),
                    'total_external': len(self.external_links),
                    'broken_count': len(self.broken_links),
                    'broken_links': self.broken_links,
                    'warnings': self.warnings
                }, f, indent=2, ensure_ascii=False)

            print(f"\n📄 詳細報告已保存到: {report_file}")

            # 失敗退出
            sys.exit(1)
        else:
            print("\n🎉 所有連結都正常！")
            sys.exit(0)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='檢查網站連結')
    parser.add_argument('--site-dir', default='_site', help='網站目錄')
    parser.add_argument('--check-external', action='store_true', help='檢查外部連結')

    args = parser.parse_args()

    tester = LinkTester(args.site_dir)
    tester.run_tests(check_external=args.check_external)

if __name__ == '__main__':
    main()
