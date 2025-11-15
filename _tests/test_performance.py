#!/usr/bin/env python3
"""
性能測試腳本
檢查網站的性能指標
"""

import sys
import json
from pathlib import Path

class PerformanceTester:
    def __init__(self, site_dir="_site"):
        self.site_dir = Path(site_dir)
        self.issues = []
        self.stats = {
            'total_size': 0,
            'file_count': 0,
            'large_files': []
        }

    def check_file_sizes(self):
        """檢查文件大小"""
        print("📊 檢查文件大小...")

        for file_path in self.site_dir.rglob('*'):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                self.stats['total_size'] += size_mb
                self.stats['file_count'] += 1

                # 檢查大文件（> 1MB）
                if size_mb > 1:
                    self.stats['large_files'].append({
                        'file': str(file_path.relative_to(self.site_dir)),
                        'size_mb': round(size_mb, 2)
                    })

                    self.issues.append({
                        'type': 'large_file',
                        'file': str(file_path.relative_to(self.site_dir)),
                        'size_mb': round(size_mb, 2),
                        'message': f'文件過大: {round(size_mb, 2)} MB'
                    })

    def check_image_optimization(self):
        """檢查圖片優化"""
        print("🖼️  檢查圖片優化...")

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
        images_dir = self.site_dir / 'assets' / 'images'

        if images_dir.exists():
            for img_file in images_dir.rglob('*'):
                if img_file.suffix.lower() in image_extensions:
                    size_kb = img_file.stat().st_size / 1024

                    if size_kb > 500:  # 大於 500KB
                        self.issues.append({
                            'type': 'large_image',
                            'file': str(img_file.relative_to(self.site_dir)),
                            'size_kb': round(size_kb, 2),
                            'message': f'圖片過大: {round(size_kb, 2)} KB，建議壓縮'
                        })

    def run_tests(self):
        """運行性能測試"""
        print("⚡ 開始性能檢查...")

        self.check_file_sizes()
        self.check_image_optimization()

        self.generate_report()

    def generate_report(self):
        """生成性能報告"""
        print("\n" + "="*60)
        print("📊 性能測試報告")
        print("="*60)

        print(f"\n📈 統計:")
        print(f"  - 總文件數: {self.stats['file_count']}")
        print(f"  - 總大小: {round(self.stats['total_size'], 2)} MB")
        print(f"  - 大文件數: {len(self.stats['large_files'])}")

        if self.stats['large_files']:
            print(f"\n📦 大文件列表:")
            for file_info in self.stats['large_files'][:10]:
                print(f"  - {file_info['file']}: {file_info['size_mb']} MB")

        if self.issues:
            print(f"\n⚠️  性能問題 ({len(self.issues)}):")
            for issue in self.issues[:20]:
                print(f"  - [{issue['type']}] {issue['message']}")

        # 保存報告
        report_dir = Path('_tests/reports')
        report_dir.mkdir(parents=True, exist_ok=True)

        with open(report_dir / 'performance_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'stats': self.stats,
                'issues': self.issues
            }, f, indent=2, ensure_ascii=False)

        print(f"\n📄 詳細報告已保存")

        if len(self.issues) > 10:
            print(f"\n⚠️  發現較多性能問題，建議優化")
        else:
            print(f"\n✅ 性能檢查完成")

        sys.exit(0)  # 性能問題不阻止部署，只是警告

def main():
    tester = PerformanceTester()
    tester.run_tests()

if __name__ == '__main__':
    main()
