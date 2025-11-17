#!/usr/bin/env python3
"""
系統監控與永動機健康檢查工具
監控整個自動化系統的運行狀態
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

class SystemMonitor:
    """永動機系統監控器"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.posts_dir = self.repo_root / '_posts'

    def check_workflow_status(self) -> Dict:
        """檢查 GitHub Actions workflow 狀態"""
        print("🔍 檢查 Workflow 狀態...")

        try:
            # 使用 gh CLI 獲取最近的 workflow runs
            result = subprocess.run(
                ['gh', 'run', 'list', '--limit', '20', '--json',
                 'status,conclusion,name,createdAt,workflowName'],
                capture_output=True,
                text=True,
                check=True
            )

            runs = json.loads(result.stdout)

            # 統計各 workflow 的狀態
            workflow_stats = {}
            for run in runs:
                workflow_name = run['workflowName']
                if workflow_name not in workflow_stats:
                    workflow_stats[workflow_name] = {
                        'total': 0,
                        'success': 0,
                        'failure': 0,
                        'in_progress': 0,
                        'last_run': run['createdAt']
                    }

                workflow_stats[workflow_name]['total'] += 1

                if run['status'] == 'completed':
                    if run['conclusion'] == 'success':
                        workflow_stats[workflow_name]['success'] += 1
                    else:
                        workflow_stats[workflow_name]['failure'] += 1
                else:
                    workflow_stats[workflow_name]['in_progress'] += 1

            return workflow_stats

        except subprocess.CalledProcessError:
            print("⚠️ 無法獲取 workflow 狀態（需要 gh CLI）")
            return {}
        except FileNotFoundError:
            print("⚠️ gh CLI 未安裝")
            return {}

    def check_content_generation(self) -> Dict:
        """檢查內容生成狀態"""
        print("📝 檢查內容生成狀態...")

        if not self.posts_dir.exists():
            return {'error': '找不到 _posts 目錄'}

        posts = list(self.posts_dir.glob('*.md'))

        # 統計最近 7 天的文章
        now = datetime.now()
        recent_posts = []

        for post in posts:
            # 從文件名提取日期 (YYYY-MM-DD-title.md)
            filename = post.name
            if len(filename) >= 10:
                try:
                    date_str = filename[:10]
                    post_date = datetime.strptime(date_str, '%Y-%m-%d')

                    if (now - post_date).days <= 7:
                        recent_posts.append({
                            'filename': filename,
                            'date': date_str,
                            'age_days': (now - post_date).days
                        })
                except ValueError:
                    continue

        return {
            'total_posts': len(posts),
            'recent_7days': len(recent_posts),
            'recent_posts': sorted(recent_posts, key=lambda x: x['date'], reverse=True)
        }

    def check_system_health(self) -> Dict:
        """整體系統健康檢查"""
        print("🏥 執行系統健康檢查...")

        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'issues': [],
            'warnings': []
        }

        # 檢查 1: 最近是否有文章生成
        content_stats = self.check_content_generation()
        if content_stats.get('recent_7days', 0) == 0:
            health['warnings'].append('過去 7 天沒有生成新文章')
            health['status'] = 'warning'

        # 檢查 2: Workflow 失敗率
        workflow_stats = self.check_workflow_status()
        for workflow_name, stats in workflow_stats.items():
            if stats['total'] > 0:
                failure_rate = stats['failure'] / stats['total']
                if failure_rate > 0.5:
                    health['issues'].append(f'{workflow_name} 失敗率過高: {failure_rate*100:.1f}%')
                    health['status'] = 'unhealthy'
                elif failure_rate > 0.2:
                    health['warnings'].append(f'{workflow_name} 失敗率偏高: {failure_rate*100:.1f}%')
                    if health['status'] == 'healthy':
                        health['status'] = 'warning'

        # 檢查 3: 重要文件是否存在
        important_files = [
            '.github/workflows/fully-auto-content.yml',
            '.github/workflows/self-healing.yml',
            '.github/workflows/auto-merge-pr.yml',
            '_tools/auto_content_generator.py',
            '_tests/auto_fixer.py'
        ]

        for file_path in important_files:
            if not (self.repo_root / file_path).exists():
                health['issues'].append(f'缺少重要文件: {file_path}')
                health['status'] = 'unhealthy'

        return health

    def generate_report(self) -> str:
        """生成完整的監控報告"""
        print("\n" + "="*60)
        print("🔄 永動機系統監控報告")
        print("="*60 + "\n")

        # 系統健康
        health = self.check_system_health()
        status_emoji = {
            'healthy': '✅',
            'warning': '⚠️',
            'unhealthy': '❌'
        }

        print(f"## {status_emoji[health['status']]} 系統狀態: {health['status'].upper()}")
        print(f"檢查時間: {health['timestamp']}\n")

        if health['issues']:
            print("### ❌ 嚴重問題:")
            for issue in health['issues']:
                print(f"  - {issue}")
            print()

        if health['warnings']:
            print("### ⚠️ 警告:")
            for warning in health['warnings']:
                print(f"  - {warning}")
            print()

        # Workflow 狀態
        print("## 📊 Workflow 運行狀態\n")
        workflow_stats = self.check_workflow_status()

        if workflow_stats:
            for workflow_name, stats in workflow_stats.items():
                success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"### {workflow_name}")
                print(f"  - 總運行: {stats['total']} 次")
                print(f"  - 成功: {stats['success']} 次 ({success_rate:.1f}%)")
                print(f"  - 失敗: {stats['failure']} 次")
                print(f"  - 進行中: {stats['in_progress']} 次")
                print(f"  - 最後運行: {stats['last_run']}")
                print()
        else:
            print("  ⚠️ 無法獲取 workflow 狀態\n")

        # 內容生成狀態
        print("## 📝 內容生成狀態\n")
        content_stats = self.check_content_generation()

        print(f"  - 總文章數: {content_stats.get('total_posts', 0)}")
        print(f"  - 最近 7 天: {content_stats.get('recent_7days', 0)} 篇")

        if content_stats.get('recent_posts'):
            print("\n  最近的文章:")
            for post in content_stats['recent_posts'][:5]:
                print(f"    - {post['date']}: {post['filename']} ({post['age_days']} 天前)")
        print()

        # 永動機循環狀態
        print("## 🔄 永動機循環狀態\n")
        self._check_perpetual_motion()

        print("="*60)
        print("報告結束")
        print("="*60 + "\n")

        return json.dumps(health, indent=2)

    def _check_perpetual_motion(self):
        """檢查永動機循環是否正常運作"""

        checks = {
            '✅ 自動生成': self._check_file('.github/workflows/fully-auto-content.yml'),
            '✅ 自動修復': self._check_file('.github/workflows/auto-fix.yml'),
            '✅ 自我修復': self._check_file('.github/workflows/self-healing.yml'),
            '✅ 自動合併': self._check_file('.github/workflows/auto-merge-pr.yml'),
            '✅ 自動部署': self._check_file('.github/workflows/deploy.yml'),
        }

        print("  循環組件:")
        for check_name, exists in checks.items():
            status = "✅" if exists else "❌"
            print(f"    {status} {check_name}")

        all_ok = all(checks.values())
        if all_ok:
            print("\n  🎉 所有組件就緒，永動機正常運作！")
        else:
            print("\n  ⚠️ 部分組件缺失，永動機無法完整運作")

    def _check_file(self, path: str) -> bool:
        """檢查文件是否存在"""
        return (self.repo_root / path).exists()

    def export_metrics(self, output_file: str = 'system_metrics.json'):
        """導出監控指標為 JSON"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'health': self.check_system_health(),
            'workflows': self.check_workflow_status(),
            'content': self.check_content_generation()
        }

        output_path = self.repo_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        print(f"✅ 監控指標已導出至: {output_path}")
        return metrics


def main():
    """主程式"""
    monitor = SystemMonitor()

    # 生成報告
    monitor.generate_report()

    # 導出指標
    monitor.export_metrics()


if __name__ == '__main__':
    main()
