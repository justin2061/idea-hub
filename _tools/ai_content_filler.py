#!/usr/bin/env python3
"""
AI 內容填充工具
使用 Claude API 自動填充文章中的 TODO 部分

使用方法：
python ai_content_filler.py --file path/to/article.md --api-key YOUR_API_KEY
"""

import os
import re
import argparse
import anthropic
from pathlib import Path
import json
import hashlib
from functools import lru_cache

class AIContentFiller:
    def __init__(self, api_key=None, use_cache=True):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            print("⚠️  未設定 API Key，將使用互動模式")

        # 性能優化：添加緩存支持
        self.use_cache = use_cache
        self.cache_dir = Path('_tests/.cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / 'ai_content_cache.json'
        self.cache = self._load_cache()

    def _load_cache(self):
        """載入緩存（性能優化）"""
        if self.use_cache and self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        """保存緩存（性能優化）"""
        if self.use_cache:
            try:
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(self.cache, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"⚠️  保存緩存失敗: {e}")

    def _get_cache_key(self, prompt: str) -> str:
        """生成緩存鍵（性能優化）"""
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()

    def extract_todos(self, content):
        """提取文章中的所有 TODO 項目"""
        # 匹配 [ ] TODO: ... 格式
        pattern = r'\[ \] TODO:?\s*(.+?)(?:\n|$)'
        todos = re.findall(pattern, content)
        return todos

    def extract_context(self, content, todo_position):
        """提取 TODO 周圍的上下文"""
        lines = content.split('\n')
        todo_line = -1

        for i, line in enumerate(lines):
            if '[ ] TODO' in line and todo_position in line:
                todo_line = i
                break

        if todo_line == -1:
            return ""

        # 提取前後 5 行作為上下文
        start = max(0, todo_line - 5)
        end = min(len(lines), todo_line + 5)
        context_lines = lines[start:end]

        return '\n'.join(context_lines)

    def generate_content_with_ai(self, todo_item, context, article_title):
        """使用 AI 生成內容（帶緩存優化）"""
        if not self.client:
            return self.interactive_mode(todo_item, context)

        prompt = f"""你是一個專業的繁體中文技術寫作助手。

文章標題：{article_title}

當前需要填寫的部分：
{todo_item}

上下文：
{context}

請根據上下文，用繁體中文撰寫這個部分的內容。要求：
1. 內容深入且實用
2. 保持專業但易懂的語調
3. 使用具體例子和數據
4. 格式清晰，適合部落格閱讀
5. 長度適中（100-300字）

只輸出內容本身，不要包含其他說明。
"""

        # 性能優化：檢查緩存
        cache_key = self._get_cache_key(prompt)
        if self.use_cache and cache_key in self.cache:
            print("  ⚡ 使用緩存內容")
            return self.cache[cache_key]

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = message.content[0].text

            # 保存到緩存
            if self.use_cache:
                self.cache[cache_key] = content
                self._save_cache()

            return content
        except Exception as e:
            print(f"❌ AI 生成失敗: {e}")
            return self.interactive_mode(todo_item, context)

    def interactive_mode(self, todo_item, context):
        """互動模式：手動輸入內容"""
        print(f"\n📝 需要填寫：{todo_item}")
        print(f"上下文：\n{context}\n")
        print("請輸入內容（輸入 'skip' 跳過）：")

        lines = []
        while True:
            line = input()
            if line.lower() == 'skip':
                return None
            if line.lower() == 'done' or line == '':
                break
            lines.append(line)

        return '\n'.join(lines)

    def fill_article(self, filepath, auto_mode=False):
        """填充文章中的 TODO 項目"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取標題
        title_match = re.search(r'title:\s*"(.+?)"', content)
        article_title = title_match.group(1) if title_match else "未知標題"

        print(f"📄 處理文章：{article_title}")
        print(f"📊 發現 {len(self.extract_todos(content))} 個 TODO 項目\n")

        # 逐個處理 TODO
        todo_pattern = r'(\[ \] TODO:?\s*)(.+?)(?=\n|$)'

        def replace_todo(match):
            todo_marker = match.group(1)
            todo_content = match.group(2)

            print(f"\n🔍 處理：{todo_content[:50]}...")

            if auto_mode and self.client:
                # 自動模式：使用 AI 生成
                context = self.extract_context(content, todo_content)
                generated = self.generate_content_with_ai(todo_content, context, article_title)

                if generated:
                    print(f"✅ 已生成內容")
                    return generated
                else:
                    return match.group(0)  # 保持原樣
            else:
                # 互動模式：詢問用戶
                response = input(f"要填充這個 TODO 嗎？(y/n/auto): ").lower()

                if response == 'y':
                    context = self.extract_context(content, todo_content)
                    generated = self.generate_content_with_ai(todo_content, context, article_title)
                    return generated if generated else match.group(0)
                elif response == 'auto' and self.client:
                    context = self.extract_context(content, todo_content)
                    generated = self.generate_content_with_ai(todo_content, context, article_title)
                    return generated if generated else match.group(0)
                else:
                    return match.group(0)  # 保持原樣

        # 替換所有 TODO
        new_content = re.sub(todo_pattern, replace_todo, content)

        # 保存結果
        output_path = filepath.replace('.md', '_filled.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"\n✅ 處理完成！新文件：{output_path}")
        return output_path

    def analyze_article(self, filepath):
        """分析文章的完成度"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        todos = self.extract_todos(content)
        total_lines = len(content.split('\n'))
        word_count = len(content)

        # 提取標題
        title_match = re.search(r'title:\s*"(.+?)"', content)
        title = title_match.group(1) if title_match else "未知"

        print(f"\n📊 文章分析報告")
        print(f"=" * 50)
        print(f"標題：{title}")
        print(f"總行數：{total_lines}")
        print(f"總字數：{word_count}")
        print(f"待完成項目：{len(todos)}")
        print(f"完成度：{((total_lines - len(todos)) / total_lines * 100):.1f}%")
        print(f"\n待完成項目：")
        for i, todo in enumerate(todos[:10], 1):  # 只顯示前 10 個
            print(f"{i}. {todo[:60]}...")

        if len(todos) > 10:
            print(f"... 還有 {len(todos) - 10} 個項目")

def main():
    parser = argparse.ArgumentParser(description='AI 內容填充工具')
    parser.add_argument('--file', '-f', required=True, help='文章檔案路徑')
    parser.add_argument('--api-key', '-k', help='Anthropic API Key')
    parser.add_argument('--auto', '-a', action='store_true', help='自動模式（不詢問）')
    parser.add_argument('--analyze', action='store_true', help='只分析不填充')

    args = parser.parse_args()

    # 創建填充器
    filler = AIContentFiller(api_key=args.api_key)

    # 檢查文件是否存在
    if not os.path.exists(args.file):
        print(f"❌ 檔案不存在：{args.file}")
        return

    if args.analyze:
        # 只分析
        filler.analyze_article(args.file)
    else:
        # 填充內容
        filler.fill_article(args.file, auto_mode=args.auto)

if __name__ == '__main__':
    main()
