# 🤖 自動內容生成系統完整指南

這是一個完全自動化的內容生成和發布系統，可以：
- 🔍 自動搜尋各分類的熱門話題
- 🤖 使用 AI 生成高質量文章（2000-3000字）
- 📝 自動格式化並保存到 `_posts/`
- 🚀 一鍵發布到 GitHub Pages

---

## 🎯 快速開始（5 分鐘）

### 步驟 1：設置 API Key

```bash
# 設置 Anthropic API Key（必需）
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# 設置 News API Key（可選，提升搜尋質量）
export NEWS_API_KEY="your-news-api-key"

# 或者保存到 .env 文件
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> _tools/.env
echo "NEWS_API_KEY=your-news-api-key" >> _tools/.env
```

### 步驟 2：一鍵生成並發布

```bash
# 進入工具目錄
cd _tools

# 給腳本執行權限
chmod +x one_click_publish.sh

# 運行（生成 5 篇不同分類的文章）
bash one_click_publish.sh 1 all

# 或者單獨測試一個分類
bash one_click_publish.sh 1 ai-tools
```

### 步驟 3：查看生成的文章

```bash
# 列出今天生成的文章
ls -la ../_posts/$(date +%Y-%m-%d)-*.md

# 預覽文章
cat ../_posts/$(date +%Y-%m-%d)-ai-tools-*.md
```

---

## 📚 詳細使用方法

### 方法 1：命令行手動運行

```bash
cd _tools

# 生成所有分類各 1 篇文章
python auto_content_generator.py --categories all --count 1

# 只生成 AI 工具分類的文章
python auto_content_generator.py --categories ai-tools --count 2

# 生成多個特定分類
python auto_content_generator.py \
  --categories ai-tools productivity entrepreneurship \
  --count 1

# 指定 API Key
python auto_content_generator.py \
  --categories all \
  --count 1 \
  --api-key "your-api-key"
```

### 方法 2：一鍵腳本（推薦）

```bash
cd _tools

# 基本用法：生成 1 篇文章，所有分類
bash one_click_publish.sh

# 指定每分類生成 2 篇
bash one_click_publish.sh 2

# 指定分類
bash one_click_publish.sh 1 "ai-tools productivity"
```

### 方法 3：GitHub Actions 自動化

**定期自動生成（每週一早上 9 點）：**
- 系統會自動運行
- 生成文章並創建 PR
- 你只需要審查並合併 PR

**手動觸發：**
1. 進入 GitHub Repository
2. 點擊 `Actions` 標籤
3. 選擇 `🤖 Auto Generate Content`
4. 點擊 `Run workflow`
5. 設置參數：
   - Categories: `all` 或 `ai-tools productivity`
   - Count: `1` 或 `2`
   - Auto Publish: 勾選自動創建 PR
6. 點擊 `Run workflow`

---

## 📂 支援的分類

系統支援 6 個分類，每個分類都有專門的搜尋策略：

### 1. AI 工具 (`ai-tools`)
**關鍵字：** AI, ChatGPT, Claude, 機器學習, AI工具
**搜尋來源：** Hacker News, Reddit (r/OpenAI, r/MachineLearning)
**適合主題：** AI 工具評測、使用教學、最新更新

### 2. 創意思維 (`creativity`)
**關鍵字：** 創意, 設計思維, 創新, SCAMPER
**搜尋來源：** Reddit (r/creativity, r/DesignThinking)
**適合主題：** 創意方法論、設計思維、創新案例

### 3. 生產力 (`productivity`)
**關鍵字：** 生產力, 效率, 時間管理, GTD
**搜尋來源：** Hacker News, Reddit (r/productivity)
**適合主題：** 效率工具、時間管理、工作流程優化

### 4. 創業 (`entrepreneurship`)
**關鍵字：** 創業, startup, 商業模式, 募資
**搜尋來源：** Hacker News, Reddit (r/Entrepreneur, r/startups)
**適合主題：** 創業經驗、商業策略、融資指南

### 5. 技術趨勢 (`tech-trends`)
**關鍵字：** 科技, 技術, 趨勢, Web3, 區塊鏈
**搜尋來源：** Hacker News, Reddit (r/technology, r/Futurology)
**適合主題：** 新興技術、未來趨勢、科技評論

### 6. 個人品牌 (`personal-branding`)
**關鍵字：** 個人品牌, 自媒體, 內容創作
**搜尋來源：** Reddit (r/personalbranding, r/socialmedia)
**適合主題：** 個人品牌建立、內容策略、社群經營

---

## ⚙️ 配置選項

### 搜尋設定

在 `auto_content_generator.py` 中可調整：

```python
# 搜尋天數範圍
days_back = 7  # 搜尋最近 7 天的內容

# 每個分類搜尋的話題數
topics_per_category = 5  # 找出前 5 個熱門話題

# 搜尋來源優先級
sources = ['HackerNews', 'Reddit', 'NewsAPI']
```

### AI 生成設定

```python
# 文章長度
max_tokens = 4000  # 約 2000-3000 字

# 創意程度
temperature = 0.7  # 0.0-1.0，越高越有創意

# 模型選擇
model = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 - 最新最強的模型
```

---

## 🎨 生成的文章結構

AI 會自動生成包含以下部分的文章：

```markdown
---
layout: single
title: "文章標題（AI 自動生成）"
date: 2025-11-14 20:30:00 +0800
categories:
  - AI工具
tags:
  - AI
  - 工具評測
  - ChatGPT
excerpt: "文章摘要（AI 從內容提取）"
---

## 引言（100-200 字）
- 吸引讀者
- 說明主題重要性
- 預告內容

## 核心內容（1500-2000 字）
- 深入分析
- 具體案例
- 數據支撐
- 表格和列表

## 實際應用（300-500 字）
- 如何應用到工作中
- 實用建議
- 行動步驟

## 總結與展望（200-300 字）
- 關鍵要點回顧
- 未來趨勢預測
- 行動呼籲

---

**參考資料：**
- [原始來源連結]
```

---

## 📊 成本估算

### Anthropic API 費用

**假設：**
- 每篇文章：~4000 tokens 輸出
- 每次請求：~500 tokens 輸入
- Claude Sonnet 3.5 價格：
  - Input: $3 / 1M tokens
  - Output: $15 / 1M tokens

**計算：**
```
每篇文章成本 = (500 × $3 + 4000 × $15) / 1,000,000
              = ($1.5 + $60) / 1,000,000
              = $0.0615
              ≈ NT$2
```

**結論：每篇文章成本約 NT$2！**

### 批量生成成本

| 文章數 | API 成本 | 台幣 | 價值 |
|--------|----------|------|------|
| 5 篇 | $0.31 | ~NT$10 | 節省 10+ 小時 |
| 10 篇 | $0.62 | ~NT$20 | 節省 20+ 小時 |
| 30 篇 | $1.85 | ~NT$60 | 節省 60+ 小時 |

**ROI：** 假設你的時薪 NT$500，每篇文章省 2 小時
- 成本：NT$2
- 節省：NT$1000
- **投資回報率：50,000%！** 🤯

### News API（可選）

- 免費版：100 requests/天
- 付費版：$449/月（無限制）
- **建議：** 使用免費版即可

---

## 🔧 進階功能

### 1. 自定義搜尋來源

編輯 `auto_content_generator.py`：

```python
def _search_custom_source(self, category: Dict) -> List[Dict]:
    """添加自定義搜尋來源"""
    topics = []

    # 例如：Product Hunt API
    url = "https://api.producthunt.com/v2/api/graphql"
    # ... 實現搜尋邏輯

    return topics
```

### 2. 自定義文章模板

在 AI prompt 中修改：

```python
prompt = f"""你是一位專業的繁體中文科技部落格作家...

文章結構：
1. 震撼的開場（加入具體數據）
2. 問題分析（為什麼這個主題重要）
3. 深度解析（包含 3-5 個子章節）
4. 實戰案例（真實的應用場景）
5. 未來展望（趨勢預測）
6. 行動建議（讀者可以立即做的 3 件事）

... 你的自定義要求 ...
"""
```

### 3. 添加圖片生成

整合 DALL-E 或 Midjourney API：

```python
def generate_cover_image(self, title: str) -> str:
    """生成文章配圖"""
    # 使用 DALL-E API 生成圖片
    # 保存到 assets/images/
    # 返回圖片路徑
    pass
```

### 4. SEO 優化

自動添加 SEO 相關欄位：

```python
def optimize_seo(self, article: str) -> str:
    """優化 SEO"""
    # 提取關鍵字
    keywords = self._extract_keywords(article)

    # 生成 meta description
    description = self._generate_meta_description(article)

    # 添加到 front matter
    # ...

    return optimized_article
```

---

## 🐛 故障排除

### 問題 1：沒有生成任何文章

**可能原因：**
- API Key 未設定或錯誤
- 搜尋沒有找到相關話題
- 網絡連接問題

**解決方案：**
```bash
# 檢查 API Key
echo $ANTHROPIC_API_KEY

# 測試 API 連接
python -c "import anthropic; client = anthropic.Anthropic(); print('✅ API 連接正常')"

# 查看詳細錯誤
python auto_content_generator.py --categories ai-tools --count 1 2>&1 | tee error.log
```

### 問題 2：生成的文章質量不佳

**可能原因：**
- 搜尋到的話題不夠相關
- AI prompt 需要優化
- 溫度參數設置不當

**解決方案：**
```python
# 調整 temperature（更保守）
temperature = 0.5  # 降低創意度，提高準確性

# 優化 prompt
# 在 prompt 中添加更多具體要求和範例

# 過濾低質量話題
# 提高 relevance 閾值
```

### 問題 3：API 費用太高

**解決方案：**
```python
# 1. 減少文章長度
max_tokens = 3000  # 從 4000 降到 3000

# 2. 使用更便宜的模型
model = "claude-3-haiku-20240307"  # 便宜 10 倍

# 3. 批量生成以分攤成本
# 一次生成 10 篇比分 10 次生成便宜
```

### 問題 4：GitHub Actions 失敗

**常見原因：**
- Secrets 未設定
- 權限不足
- 依賴安裝失敗

**解決方案：**
```bash
# 檢查 Secrets 設定
# Repository → Settings → Secrets → Actions
# 確保有 ANTHROPIC_API_KEY

# 查看 Actions 日誌
# Repository → Actions → 點擊失敗的運行 → 查看詳細日誌
```

---

## 📈 最佳實踐

### 1. 定期生成，保持更新

```bash
# 使用 cron job 定期運行（例如：每週一）
# 添加到 crontab
0 9 * * 1 cd /path/to/idea-hub/_tools && bash one_click_publish.sh 1 all
```

### 2. 人工審查與優化

生成後建議：
- ✅ 檢查事實準確性
- ✅ 添加個人經驗和見解
- ✅ 優化語句流暢度
- ✅ 添加相關圖片
- ✅ 檢查連結有效性

### 3. 混合使用：AI + 人工

```
AI 生成 70% → 人工優化 30% = 完美文章
```

**AI 擅長：**
- 搜尋整理資訊
- 生成文章結構
- 提供多角度觀點
- 保持一致風格

**人類擅長：**
- 加入個人經驗
- 判斷價值和重要性
- 創意和獨特觀點
- 情感共鳴

### 4. 建立內容日曆

```python
# 規劃每週內容
week_plan = {
    'Monday': ['ai-tools'],
    'Wednesday': ['productivity'],
    'Friday': ['creativity']
}
```

### 5. 追蹤效果

```bash
# 使用 Google Analytics 追蹤
# 記錄哪些 AI 生成的文章表現最好
# 持續優化生成策略
```

---

## 🚀 自動化工作流程

### 完整自動化方案

```
週一早上 9:00
  ↓
GitHub Actions 自動觸發
  ↓
搜尋各分類熱門話題
  ↓
AI 生成 5 篇文章
  ↓
自動格式化和驗證
  ↓
創建 Pull Request
  ↓
通知你審查（Email/Slack）
  ↓
你審查並合併（或退回修改）
  ↓
自動部署到 GitHub Pages
  ↓
文章上線！🎉
```

**你的工作：** 只需要 10 分鐘審查和點擊合併！

---

## 💡 創意使用案例

### 案例 1：建立專題系列

```bash
# 連續 4 週生成「AI 工具深度評測」系列
for i in {1..4}; do
  python auto_content_generator.py --categories ai-tools --count 1
  sleep 604800  # 等待一週
done
```

### 案例 2：多語言內容

修改 AI prompt 生成英文版：

```python
prompt = """You are a professional tech blog writer...
Write in English...
"""
```

### 案例 3：整合到其他平台

```bash
# 生成後自動發布到
- Medium（使用 Medium API）
- Dev.to（使用 Dev.to API）
- LinkedIn（使用 LinkedIn API）
```

---

## 📞 獲取幫助

### 文檔
- 📖 [README.md](./README.md) - 工具包總覽
- 🚀 [QUICKSTART.md](./QUICKSTART.md) - 快速開始
- 🔧 本文檔 - 自動內容生成

### 問題排查
1. 查看錯誤日誌
2. 檢查 API Key 設定
3. 測試網絡連接
4. 查看 GitHub Actions 日誌

### 社群
- 提交 Issue 到 GitHub
- 分享你的使用經驗
- 貢獻改進建議

---

## 🎉 開始使用！

現在就試試：

```bash
# 1. 設置 API Key
export ANTHROPIC_API_KEY="your-api-key"

# 2. 運行一鍵腳本
cd _tools
bash one_click_publish.sh 1 ai-tools

# 3. 查看生成的文章
ls -la ../_posts/$(date +%Y-%m-%d)-*.md

# 4. 預覽並發布
git add ../_posts/
git commit -m "🤖 AI 生成新文章"
git push
```

**祝你內容創作愉快！** ✨

---

*最後更新：2025-11-14*
