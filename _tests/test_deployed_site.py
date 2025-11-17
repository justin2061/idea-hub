#!/usr/bin/env python3
"""
部署後測試腳本
測試已部署的網站是否正常運行
"""

import sys
import requests
from urllib.parse import urljoin

class DeployedSiteTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.errors = []
        self.warnings = []

    def test_homepage(self):
        """測試首頁"""
        print(f"🏠 測試首頁: {self.base_url}/")

        try:
            response = requests.get(self.base_url, timeout=10)

            if response.status_code != 200:
                self.errors.append({
                    'test': 'homepage',
                    'message': f'首頁返回 HTTP {response.status_code}'
                })
            else:
                print(f"  ✅ 首頁正常 (HTTP {response.status_code})")

                # 檢查內容
                if len(response.content) < 1000:
                    self.warnings.append({
                        'test': 'homepage',
                        'message': '首頁內容似乎太少'
                    })

        except requests.RequestException as e:
            self.errors.append({
                'test': 'homepage',
                'message': f'無法訪問首頁: {e}'
            })

    def test_response_time(self):
        """測試響應時間"""
        print(f"⏱️  測試響應時間...")

        try:
            response = requests.get(self.base_url, timeout=10)
            response_time = response.elapsed.total_seconds()

            print(f"  ⏱️  響應時間: {response_time:.2f} 秒")

            if response_time > 3:
                self.warnings.append({
                    'test': 'response_time',
                    'message': f'響應時間過長: {response_time:.2f} 秒'
                })
            else:
                print(f"  ✅ 響應時間正常")

        except requests.RequestException as e:
            self.errors.append({
                'test': 'response_time',
                'message': f'無法測試響應時間: {e}'
            })

    def test_https(self):
        """測試 HTTPS"""
        if self.base_url.startswith('https'):
            print(f"🔒 測試 HTTPS...")

            try:
                response = requests.get(self.base_url, timeout=10, verify=True)
                print(f"  ✅ HTTPS 證書有效")
            except requests.exceptions.SSLError:
                self.errors.append({
                    'test': 'https',
                    'message': 'SSL 證書無效'
                })
            except requests.RequestException as e:
                self.warnings.append({
                    'test': 'https',
                    'message': f'HTTPS 測試失敗: {e}'
                })
        else:
            self.warnings.append({
                'test': 'https',
                'message': '網站未啟用 HTTPS'
            })

    def test_common_pages(self):
        """測試常見頁面"""
        print(f"📄 測試常見頁面...")

        pages = [
            '/about/',
            '/posts/',
            '/404.html',
        ]

        for page in pages:
            url = urljoin(self.base_url, page)

            try:
                response = requests.get(url, timeout=10)

                # 404 頁面應該返回 404
                if page == '/404.html' and response.status_code != 404:
                    print(f"  ⚠️  {page}: HTTP {response.status_code} (預期 404)")
                elif page != '/404.html' and response.status_code >= 400:
                    print(f"  ❌ {page}: HTTP {response.status_code}")
                    self.warnings.append({
                        'test': 'common_pages',
                        'message': f'{page} 返回 {response.status_code}'
                    })
                else:
                    print(f"  ✅ {page}: HTTP {response.status_code}")

            except requests.RequestException:
                # 某些頁面可能不存在，這是正常的
                print(f"  ℹ️  {page}: 不存在")

    def test_security_headers(self):
        """測試安全標頭"""
        print(f"🔐 測試安全標頭...")

        try:
            response = requests.get(self.base_url, timeout=10)
            headers = response.headers

            recommended_headers = {
                'X-Frame-Options': 'SAMEORIGIN or DENY',
                'X-Content-Type-Options': 'nosniff',
                'X-XSS-Protection': '1; mode=block',
            }

            for header, expected in recommended_headers.items():
                if header in headers:
                    print(f"  ✅ {header}: {headers[header]}")
                else:
                    print(f"  ⚠️  缺少 {header}")
                    self.warnings.append({
                        'test': 'security_headers',
                        'message': f'缺少安全標頭: {header}'
                    })

        except requests.RequestException as e:
            self.warnings.append({
                'test': 'security_headers',
                'message': f'無法測試安全標頭: {e}'
            })

    def run_tests(self):
        """運行所有測試"""
        print(f"\n{'='*60}")
        print(f"🧪 測試部署的網站: {self.base_url}")
        print(f"{'='*60}\n")

        self.test_homepage()
        self.test_response_time()
        self.test_https()
        self.test_common_pages()
        self.test_security_headers()

        self.generate_report()

    def generate_report(self):
        """生成測試報告"""
        print(f"\n{'='*60}")
        print("📊 部署測試報告")
        print(f"{'='*60}\n")

        print(f"❌ 錯誤: {len(self.errors)}")
        print(f"⚠️  警告: {len(self.warnings)}")

        if self.errors:
            print(f"\n❌ 錯誤列表:")
            for error in self.errors:
                print(f"  - [{error['test']}] {error['message']}")

        if self.warnings:
            print(f"\n⚠️  警告列表:")
            for warning in self.warnings:
                print(f"  - [{warning['test']}] {warning['message']}")

        if not self.errors and not self.warnings:
            print(f"\n🎉 所有測試都通過！網站運行正常。")
            sys.exit(0)
        elif self.errors:
            print(f"\n❌ 發現嚴重錯誤，部署可能有問題！")
            sys.exit(1)
        else:
            print(f"\n⚠️  有一些警告，但網站基本正常。")
            sys.exit(0)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='測試已部署的網站')
    parser.add_argument('url', help='網站 URL (如: http://example.com)')

    args = parser.parse_args()

    tester = DeployedSiteTester(args.url)
    tester.run_tests()

if __name__ == '__main__':
    main()
