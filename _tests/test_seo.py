#!/usr/bin/env python3
"""
SEO 測試腳本
檢查網站的 SEO 優化情況
"""

import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup

class SEOTester:
    def __init__(self, site_dir="_site"):
        self.site_dir = Path(site_dir)
        self.issues = []
        self.warnings = []

    def test_html_file(self, html_file):
        """測試單個 HTML 文件的 SEO"""
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        relative_path = html_file.relative_to(self.site_dir)

        # 檢查 title 標籤
        title = soup.find('title')
        if not title:
            self.issues.append({
                'file': str(relative_path),
                'type': 'missing_title',
                'message': '缺少 <title> 標籤'
            })
        elif len(title.text) < 10:
            self.warnings.append({
                'file': str(relative_path),
                'type': 'short_title',
                'message': f'標題太短: {len(title.text)} 字'
            })
        elif len(title.text) > 60:
            self.warnings.append({
                'file': str(relative_path),
                'type': 'long_title',
                'message': f'標題太長: {len(title.text)} 字'
            })

        # 檢查 meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            self.warnings.append({
                'file': str(relative_path),
                'type': 'missing_description',
                'message': '缺少 meta description'
            })
        elif meta_desc.get('content'):
            desc_length = len(meta_desc['content'])
            if desc_length < 50:
                self.warnings.append({
                    'file': str(relative_path),
                    'type': 'short_description',
                    'message': f'描述太短: {desc_length} 字'
                })
            elif desc_length > 160:
                self.warnings.append({
                    'file': str(relative_path),
                    'type': 'long_description',
                    'message': f'描述太長: {desc_length} 字'
                })

        # 檢查 H1 標籤
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            self.warnings.append({
                'file': str(relative_path),
                'type': 'missing_h1',
                'message': '缺少 H1 標籤'
            })
        elif len(h1_tags) > 1:
            self.warnings.append({
                'file': str(relative_path),
                'type': 'multiple_h1',
                'message': f'有 {len(h1_tags)} 個 H1 標籤（建議只有 1 個）'
            })

        # 檢查圖片 alt 屬性
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                self.warnings.append({
                    'file': str(relative_path),
                    'type': 'missing_alt',
                    'message': f'圖片缺少 alt 屬性: {img.get("src", "unknown")}'
                })

    def run_tests(self):
        """運行所有 SEO 測試"""
        print("🔍 開始 SEO 檢查...")

        html_files = list(self.site_dir.rglob("*.html"))
        print(f"📄 找到 {len(html_files)} 個 HTML 文件")

        for html_file in html_files:
            self.test_html_file(html_file)

        self.generate_report()

    def generate_report(self):
        """生成 SEO 報告"""
        print("\n" + "="*60)
        print("📊 SEO 測試報告")
        print("="*60)

        print(f"\n❌ 錯誤: {len(self.issues)}")
        print(f"⚠️  警告: {len(self.warnings)}")

        if self.issues:
            print(f"\n❌ 嚴重問題:")
            for issue in self.issues[:10]:
                print(f"  - [{issue['file']}] {issue['message']}")

        if self.warnings:
            print(f"\n⚠️  建議改進:")
            for warning in self.warnings[:20]:
                print(f"  - [{warning['file']}] {warning['message']}")

        # 保存報告
        report_dir = Path('_tests/reports')
        report_dir.mkdir(parents=True, exist_ok=True)

        with open(report_dir / 'seo_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'issues': self.issues,
                'warnings': self.warnings
            }, f, indent=2, ensure_ascii=False)

        if self.issues:
            sys.exit(1)
        else:
            print("\n✅ SEO 檢查完成（只有建議，無嚴重問題）")
            sys.exit(0)

def main():
    tester = SEOTester()
    tester.run_tests()

if __name__ == '__main__':
    main()
