#!/usr/bin/env python3
"""
文章自動生成器
用於快速生成部落格文章的框架和內容

使用方法：
python article_generator.py --template comparison --title "Claude vs ChatGPT"
"""

import os
import sys
import argparse
from datetime import datetime
import yaml
import re

class ArticleGenerator:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.drafts_dir = os.path.join(os.path.dirname(__file__), '..', '_drafts')

        # 確保目錄存在
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.drafts_dir, exist_ok=True)

    def list_templates(self):
        """列出所有可用的模板"""
        templates = [
            'comparison',      # 對比類文章（如 Claude vs ChatGPT）
            'tool_review',     # 工具評測（如 Notion AI 指南）
            'tutorial',        # 教學類（如創意思維框架）
            'idea_showcase',   # 點子展示（如哈利波特頭像）
            'quick_note',      # 快速筆記（500-800字）
        ]
        return templates

    def generate_filename(self, title):
        """根據標題生成檔案名稱"""
        # 移除特殊字符，轉換為小寫
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)

        # 添加日期
        today = datetime.now().strftime('%Y-%m-%d')
        return f"{today}-{filename}.md"

    def generate_comparison_article(self, config):
        """生成對比類文章"""
        title = config.get('title', '未命名文章')
        item_a = config.get('item_a', 'A')
        item_b = config.get('item_b', 'B')
        categories = config.get('categories', ['未分類'])
        tags = config.get('tags', [])

        template = f"""---
layout: single
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories:
{self._format_yaml_list(categories)}
tags:
{self._format_yaml_list(tags)}
excerpt: "深度對比 {item_a} 與 {item_b}，基於實際使用經驗的全面分析，幫助你找到最適合的工具。"
---

在 AI 工具快速發展的今天，{item_a} 和 {item_b} 都是市場上的熱門選擇。但究竟哪一個更適合你？本文將基於實際使用經驗，進行全面深度的對比分析。

<!--more-->

## 🎯 為什麼要對比 {item_a} 和 {item_b}？

### 對比的意義
- 兩者都是市場領導者
- 功能有重疊但各有特色
- 選擇困難需要客觀分析

### 本文的價值
- 基於 3+ 個月實際使用經驗
- 包含真實測試數據
- 提供具體選擇建議

---

## 📊 第一部分：基礎認識

### 1.1 {item_a} 簡介

**核心特色：**
- [ ] TODO: 填寫主要特色 1
- [ ] TODO: 填寫主要特色 2
- [ ] TODO: 填寫主要特色 3

**價格方案：**
- 免費版：[ ] TODO
- 付費版：[ ] TODO

### 1.2 {item_b} 簡介

**核心特色：**
- [ ] TODO: 填寫主要特色 1
- [ ] TODO: 填寫主要特色 2
- [ ] TODO: 填寫主要特色 3

**價格方案：**
- 免費版：[ ] TODO
- 付費版：[ ] TODO

---

## 🔍 第二部分：核心能力對比

### 2.1 功能對比

| 功能指標 | {item_a} | {item_b} | 優勢方 |
|---------|---------|---------|--------|
| 功能 1 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | [ ] TODO |
| 功能 2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | [ ] TODO |
| 功能 3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | [ ] TODO |

### 2.2 實測案例

**測試場景 1：**
- [ ] TODO: 描述測試場景
- {item_a} 表現：[ ] TODO
- {item_b} 表現：[ ] TODO
- 結論：[ ] TODO

**測試場景 2：**
- [ ] TODO: 描述測試場景
- {item_a} 表現：[ ] TODO
- {item_b} 表現：[ ] TODO
- 結論：[ ] TODO

---

## 💡 第三部分：使用場景建議

### 3.1 適合使用 {item_a} 的場景

**場景 1：**
- [ ] TODO: 描述場景
- 為什麼選 {item_a}：[ ] TODO
- 實際案例：[ ] TODO

### 3.2 適合使用 {item_b} 的場景

**場景 1：**
- [ ] TODO: 描述場景
- 為什麼選 {item_b}：[ ] TODO
- 實際案例：[ ] TODO

---

## ⚖️ 第四部分：優劣勢總結

### {item_a} 的優勢與劣勢

**✅ 主要優勢：**
1. [ ] TODO: 優勢 1
2. [ ] TODO: 優勢 2
3. [ ] TODO: 優勢 3

**❌ 主要劣勢：**
1. [ ] TODO: 劣勢 1
2. [ ] TODO: 劣勢 2
3. [ ] TODO: 劣勢 3

### {item_b} 的優勢與劣勢

**✅ 主要優勢：**
1. [ ] TODO: 優勢 1
2. [ ] TODO: 優勢 2
3. [ ] TODO: 優勢 3

**❌ 主要劣勢：**
1. [ ] TODO: 劣勢 1
2. [ ] TODO: 劣勢 2
3. [ ] TODO: 劣勢 3

---

## 🎯 第五部分：選擇建議

### 快速決策指南

**選擇 {item_a} 如果你：**
- [ ] TODO: 條件 1
- [ ] TODO: 條件 2
- [ ] TODO: 條件 3

**選擇 {item_b} 如果你：**
- [ ] TODO: 條件 1
- [ ] TODO: 條件 2
- [ ] TODO: 條件 3

### 我的個人建議

[ ] TODO: 基於你的實際使用經驗，給出誠實的建議

---

## 📈 實測數據總結

### 測試項目對比

| 測試項目 | {item_a} | {item_b} | 勝出方 |
|---------|---------|---------|--------|
| 測試 1 | [ ] TODO | [ ] TODO | [ ] TODO |
| 測試 2 | [ ] TODO | [ ] TODO | [ ] TODO |
| 測試 3 | [ ] TODO | [ ] TODO | [ ] TODO |

---

## 🚀 結語與行動建議

### 核心結論
- [ ] TODO: 一句話總結你的觀點

### 立即行動
1. [ ] TODO: 具體行動建議 1
2. [ ] TODO: 具體行動建議 2
3. [ ] TODO: 具體行動建議 3

---

*你使用過 {item_a} 或 {item_b} 嗎？歡迎在留言區分享你的使用經驗！*

**相關文章推薦：**
- [2025 年必知的 10 個 AI 生產力工具](/ai-productivity-tools-2025)
- [Notion AI 完整指南](/notion-ai-complete-guide)
"""
        return template

    def generate_tool_review_article(self, config):
        """生成工具評測類文章"""
        title = config.get('title', '未命名文章')
        tool_name = config.get('tool_name', '工具')
        categories = config.get('categories', ['AI工具'])
        tags = config.get('tags', [])

        template = f"""---
layout: single
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories:
{self._format_yaml_list(categories)}
tags:
{self._format_yaml_list(tags)}
excerpt: "深度評測 {tool_name}，從基礎操作到高級技巧，幫你充分發揮工具潛力。"
---

{tool_name} 是一個強大的工具，本文將深入介紹其核心功能與實戰應用。

<!--more-->

## 🎯 為什麼選擇 {tool_name}？

### 核心優勢
- [ ] TODO: 優勢 1
- [ ] TODO: 優勢 2
- [ ] TODO: 優勢 3

---

## 🚀 核心功能深度解析

### 1. 功能一

**使用場景：**
- [ ] TODO: 場景描述

**操作步驟：**
1. [ ] TODO: 步驟 1
2. [ ] TODO: 步驟 2
3. [ ] TODO: 步驟 3

### 2. 功能二

**使用場景：**
- [ ] TODO: 場景描述

**操作步驟：**
1. [ ] TODO: 步驟 1
2. [ ] TODO: 步驟 2
3. [ ] TODO: 步驟 3

---

## 💡 實戰應用場景

### 場景一：[ ] TODO

**步驟：**
1. [ ] TODO
2. [ ] TODO
3. [ ] TODO

**效果：**
- [ ] TODO: 描述實際效果

---

## 🔧 進階技巧與最佳實踐

### 技巧 1：[ ] TODO

### 技巧 2：[ ] TODO

---

## ⚠️ 使用注意事項

1. [ ] TODO: 注意事項 1
2. [ ] TODO: 注意事項 2
3. [ ] TODO: 注意事項 3

---

## 🎯 總結與建議

[ ] TODO: 總結你的使用心得

---

*如果這篇文章對你有幫助，歡迎分享！*
"""
        return template

    def generate_quick_note(self, config):
        """生成快速筆記（500-800字）"""
        title = config.get('title', '未命名筆記')
        categories = config.get('categories', ['技術筆記'])
        tags = config.get('tags', [])

        template = f"""---
layout: single
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories:
{self._format_yaml_list(categories)}
tags:
{self._format_yaml_list(tags)}
excerpt: "[ ] TODO: 一句話總結這篇筆記的核心內容"
---

## 💡 核心觀點

[ ] TODO: 用 2-3 句話說明這篇筆記的核心內容

---

## 📝 詳細說明

### 重點 1
[ ] TODO: 展開說明

### 重點 2
[ ] TODO: 展開說明

### 重點 3
[ ] TODO: 展開說明

---

## 🚀 實際應用

**範例：**
```
[ ] TODO: 加入代碼或實例
```

---

## 🎯 關鍵要點

- [ ] TODO: 要點 1
- [ ] TODO: 要點 2
- [ ] TODO: 要點 3

---

## 🔗 相關資源

- [ ] TODO: 相關連結或文章

---

*這是一篇快速筆記，歡迎留言討論！*
"""
        return template

    def _format_yaml_list(self, items):
        """格式化 YAML 列表"""
        if not items:
            return "  - 未分類"
        return '\n'.join([f"  - {item}" for item in items])

    def create_article(self, template_type, config):
        """創建文章"""
        if template_type == 'comparison':
            content = self.generate_comparison_article(config)
        elif template_type == 'tool_review':
            content = self.generate_tool_review_article(config)
        elif template_type == 'quick_note':
            content = self.generate_quick_note(config)
        else:
            raise ValueError(f"未知的模板類型: {template_type}")

        # 生成檔案名稱
        filename = self.generate_filename(config.get('title', '未命名'))
        filepath = os.path.join(self.drafts_dir, filename)

        # 寫入檔案
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

def main():
    parser = argparse.ArgumentParser(description='文章自動生成器')
    parser.add_argument('--template', '-t',
                       choices=['comparison', 'tool_review', 'quick_note'],
                       required=True,
                       help='文章模板類型')
    parser.add_argument('--title', required=True, help='文章標題')
    parser.add_argument('--item-a', help='對比項目 A（僅用於 comparison）')
    parser.add_argument('--item-b', help='對比項目 B（僅用於 comparison）')
    parser.add_argument('--tool', help='工具名稱（僅用於 tool_review）')
    parser.add_argument('--categories', nargs='+', default=['AI工具'], help='分類')
    parser.add_argument('--tags', nargs='+', default=[], help='標籤')

    args = parser.parse_args()

    # 構建配置
    config = {
        'title': args.title,
        'categories': args.categories,
        'tags': args.tags,
    }

    if args.template == 'comparison':
        if not args.item_a or not args.item_b:
            print("錯誤：comparison 模板需要 --item-a 和 --item-b 參數")
            sys.exit(1)
        config['item_a'] = args.item_a
        config['item_b'] = args.item_b
    elif args.template == 'tool_review':
        if not args.tool:
            print("錯誤：tool_review 模板需要 --tool 參數")
            sys.exit(1)
        config['tool_name'] = args.tool

    # 生成文章
    generator = ArticleGenerator()
    filepath = generator.create_article(args.template, config)

    print(f"✅ 文章框架已生成：{filepath}")
    print(f"\n接下來你可以：")
    print(f"1. 使用編輯器打開文件")
    print(f"2. 填寫 [ ] TODO 標記的部分")
    print(f"3. 使用 AI 輔助填充內容")
    print(f"4. 完成後移到 _posts 目錄發布")

if __name__ == '__main__':
    main()
