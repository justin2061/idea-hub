#!/usr/bin/env python3
"""
性能監控工具
監控網站性能指標，包括頁面大小、加載時間等

使用方法：
python performance_monitor.py --url https://justin2061.github.io/idea-hub
"""

import argparse
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json


class PerformanceMonitor:
    def __init__(self, url: str):
        self.url = url
        self.results = {}

    def measure_page_load(self) -> Dict:
        """測量頁面加載性能"""
        print(f"🔍 測量頁面加載性能: {self.url}")

        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=30)
            end_time = time.time()

            load_time = end_time - start_time
            content_size = len(response.content)
            status_code = response.status_code

            result = {
                'url': self.url,
                'status_code': status_code,
                'load_time': round(load_time, 3),
                'content_size': content_size,
                'content_size_kb': round(content_size / 1024, 2),
                'timestamp': datetime.now().isoformat(),
                'headers': dict(response.headers)
            }

            print(f"  ✅ 狀態碼: {status_code}")
            print(f"  ⏱️  加載時間: {load_time:.3f} 秒")
            print(f"  📦 內容大小: {content_size} bytes ({content_size/1024:.2f} KB)")

            return result

        except Exception as e:
            print(f"  ❌ 測量失敗: {e}")
            return {
                'url': self.url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def analyze_cache_headers(self, headers: Dict) -> Dict:
        """分析緩存頭"""
        cache_info = {
            'cache_control': headers.get('Cache-Control', 'Not set'),
            'etag': headers.get('ETag', 'Not set'),
            'last_modified': headers.get('Last-Modified', 'Not set'),
            'expires': headers.get('Expires', 'Not set'),
            'content_encoding': headers.get('Content-Encoding', 'Not set')
        }

        print("\n📋 緩存頭分析:")
        for key, value in cache_info.items():
            print(f"  - {key}: {value}")

        return cache_info

    def generate_report(self, output_file: str = None):
        """生成性能報告"""
        result = self.measure_page_load()

        if 'error' not in result:
            cache_analysis = self.analyze_cache_headers(result['headers'])
            result['cache_analysis'] = cache_analysis

        # 保存報告
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"\n💾 報告已保存: {output_path}")

        return result

    def compare_with_baseline(self, baseline_file: str):
        """與基準性能比較"""
        print("\n📊 與基準性能比較...")

        baseline_path = Path(baseline_file)
        if not baseline_path.exists():
            print(f"  ⚠️  基準文件不存在: {baseline_file}")
            return

        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)

        current = self.measure_page_load()

        if 'error' in baseline or 'error' in current:
            print("  ❌ 無法比較（存在錯誤）")
            return

        # 比較指標
        load_time_diff = current['load_time'] - baseline['load_time']
        size_diff = current['content_size'] - baseline['content_size']

        print(f"\n⏱️  加載時間:")
        print(f"  - 基準: {baseline['load_time']:.3f} 秒")
        print(f"  - 當前: {current['load_time']:.3f} 秒")
        print(f"  - 差異: {load_time_diff:+.3f} 秒 ({load_time_diff/baseline['load_time']*100:+.1f}%)")

        print(f"\n📦 內容大小:")
        print(f"  - 基準: {baseline['content_size_kb']} KB")
        print(f"  - 當前: {current['content_size_kb']} KB")
        print(f"  - 差異: {size_diff/1024:+.2f} KB ({size_diff/baseline['content_size']*100:+.1f}%)")


def main():
    parser = argparse.ArgumentParser(description='性能監控工具')
    parser.add_argument('--url', required=True, help='要測量的網站 URL')
    parser.add_argument('--output', help='輸出報告文件路徑')
    parser.add_argument('--baseline', help='基準性能文件路徑（用於比較）')

    args = parser.parse_args()

    monitor = PerformanceMonitor(args.url)

    if args.baseline:
        monitor.compare_with_baseline(args.baseline)
    else:
        monitor.generate_report(args.output)


if __name__ == '__main__':
    main()
