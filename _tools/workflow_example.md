# 📝 完整工作流程範例

這是一個從零到發布的完整示範，展示如何使用自動化工具快速創建一篇文章。

---

## 🎯 場景：撰寫「Cursor vs GitHub Copilot」對比文章

### 目標
- 文章類型：工具對比
- 預估字數：4000+ 字
- 完成時間：40 分鐘（而非 4 小時）

---

## 📅 工作流程

### 階段 1：規劃（5 分鐘）

**1. 確定主題與受眾**
- 主題：Cursor vs GitHub Copilot 對比
- 目標讀者：程式開發者
- 核心價值：幫助選擇適合的 AI 編程工具

**2. 列出關鍵點**
- [ ] 兩個工具的基本介紹
- [ ] 功能對比表格
- [ ] 實測案例
- [ ] 價格分析
- [ ] 選擇建議

---

### 階段 2：生成框架（1 分鐘）

**執行命令：**

```bash
cd /home/user/idea-hub/_tools

python article_generator.py \
  --template comparison \
  --title "Cursor vs GitHub Copilot：2025 年 AI 編程助手終極對比" \
  --item-a "Cursor" \
  --item-b "GitHub Copilot" \
  --categories "AI工具" "程式開發" \
  --tags "Cursor" "GitHub Copilot" "AI編程" "開發工具"
```

**輸出：**
```
✅ 文章框架已生成：/home/user/idea-hub/_drafts/2025-11-14-cursor-vs-github-copilot.md

接下來你可以：
1. 使用編輯器打開文件
2. 填寫 [ ] TODO 標記的部分
3. 使用 AI 輔助填充內容
4. 完成後移到 _posts 目錄發布
```

---

### 階段 3：分析文章（30 秒）

**檢查需要完成的工作：**

```bash
python ai_content_filler.py \
  --file ../\_drafts/2025-11-14-cursor-vs-github-copilot.md \
  --analyze
```

**輸出範例：**
```
📊 文章分析報告
==================================================
標題：Cursor vs GitHub Copilot：2025 年 AI 編程助手終極對比
總行數：280
總字數：1850
待完成項目：18
完成度：35.7%

待完成項目：
1. 填寫 Cursor 主要特色 1
2. 填寫 Cursor 主要特色 2
3. 填寫 Cursor 主要特色 3
4. 填寫 Cursor 價格方案 - 免費版
5. 填寫 Cursor 價格方案 - 付費版
...（還有 13 個）
```

---

### 階段 4：AI 自動填充（5 分鐘）

**選項 A：全自動模式（快速）**

```bash
# 需要設定 API Key
export ANTHROPIC_API_KEY="your-api-key"

python ai_content_filler.py \
  --file ../_drafts/2025-11-14-cursor-vs-github-copilot.md \
  --auto
```

這會自動填充所有 TODO 項目，5 分鐘內完成！

**選項 B：互動模式（可控）**

```bash
python ai_content_filler.py \
  --file ../_drafts/2025-11-14-cursor-vs-github-copilot.md
```

對每個 TODO 項目，你可以選擇：
- `y` - 使用 AI 生成
- `n` - 跳過（稍後手動填寫）
- `auto` - 從這個開始全部自動

**選項 C：完全手動（不使用 AI）**

直接用編輯器打開文件，手動填寫所有 `[ ] TODO` 部分。

---

### 階段 5：手動優化（30 分鐘）

**這是最重要的步驟！** AI 生成的內容需要加入你的個人經驗。

打開生成的文件：
```bash
code ../_drafts/2025-11-14-cursor-vs-github-copilot_filled.md
```

**優化清單：**

1. **加入個人經驗**
   ```markdown
   ❌ AI生成：Cursor 的代碼補全速度很快
   ✅ 優化後：根據我實際使用 3 個月的經驗，Cursor 的代碼補全速度
              比 Copilot 快約 30%，特別是在大型項目中優勢明顯。
   ```

2. **添加實測數據**
   ```markdown
   ### 實測對比：開發 React 組件

   測試任務：建立一個完整的 TodoList 組件

   | 指標 | Cursor | GitHub Copilot |
   |------|--------|----------------|
   | 完成時間 | 12 分鐘 | 18 分鐘 |
   | 代碼行數 | 85 行 | 92 行 |
   | 錯誤數 | 1 個 | 3 個 |
   | 代碼品質 | A+ | B+ |
   ```

3. **插入截圖**
   ```markdown
   **Cursor 的智能補全界面：**

   ![Cursor 截圖](../assets/images/cursor-screenshot.png)
   ```

4. **加入真實案例**
   ```markdown
   ### 真實案例：重構遺留代碼

   上週我用 Cursor 重構了一個 2000 行的舊專案：

   1. 自動識別出 15 個潛在 bug
   2. 建議了 8 個性能優化點
   3. 自動生成了單元測試
   4. 總共節省了 6 小時工作時間

   相同任務用 Copilot 我估計需要 8-10 小時。
   ```

5. **調整語氣與風格**
   - AI 生成的內容可能太正式
   - 加入一些口語化的表達
   - 使用「我」、「你」等人稱讓文章更親切

6. **檢查事實準確性**
   - 驗證價格資訊
   - 確認功能描述
   - 更新最新版本資訊

---

### 階段 6：最終檢查（3 分鐘）

**檢查清單：**

```bash
# 1. 檢查是否還有 TODO
grep "\[ \] TODO" ../_drafts/2025-11-14-cursor-vs-github-copilot_filled.md

# 2. 檢查字數
wc -w ../_drafts/2025-11-14-cursor-vs-github-copilot_filled.md

# 3. 檢查格式
# 確認 front matter 正確
# 確認所有表格正確顯示
# 確認 emoji 使用適當
```

**內容檢查：**
- [ ] 標題吸引人
- [ ] 摘要清晰（150-200 字）
- [ ] 有明確的目錄結構
- [ ] 包含實用的對比表格
- [ ] 有具體的行動建議
- [ ] 相關文章連結正確
- [ ] SEO 關鍵字自然融入
- [ ] 沒有錯別字

---

### 階段 7：發布（1 分鐘）

**一鍵發布：**

```bash
bash quick_publish.sh \
  ../_drafts/2025-11-14-cursor-vs-github-copilot_filled.md \
  "新增文章：Cursor vs GitHub Copilot 深度對比"
```

**腳本會自動：**
1. ✅ 移動文件到 `_posts` 目錄
2. ✅ 移除檔名中的 `_filled` 後綴
3. ✅ 檢查是否還有 TODO（如有會警告）
4. ✅ Git add + commit
5. ✅ Push 到遠端分支
6. ✅ 顯示發布摘要

**輸出：**
```
📄 處理文章：2025-11-14-cursor-vs-github-copilot_filled.md
📁 移動文章到 _posts 目錄...
✅ 已移動到：../_posts/2025-11-14-cursor-vs-github-copilot_filled.md
📝 重新命名文件...
✅ 新檔名：2025-11-14-cursor-vs-github-copilot.md
🔄 執行 Git 操作...
✅ 已添加文件到 Git
✅ 已提交：新增文章：Cursor vs GitHub Copilot 深度對比
🚀 推送到分支：claude/content-strategy-planning-01Tp2dNyRt6wNderS8VDoL6o
✅ 發布成功！

📊 發布摘要
====================
文章：2025-11-14-cursor-vs-github-copilot.md
分支：claude/content-strategy-planning-01Tp2dNyRt6wNderS8VDoL6o
訊息：新增文章：Cursor vs GitHub Copilot 深度對比
====================

📄 文章資訊
字數：4523
行數：342
標題：Cursor vs GitHub Copilot：2025 年 AI 編程助手終極對比
日期：2025-11-14 09:00:00 +0800

🎉 完成！你的文章已成功發布！
```

---

## ⏱️ 時間統計

| 階段 | 時間 | 傳統方式 | 節省 |
|------|------|----------|------|
| 規劃 | 5 分鐘 | 30 分鐘 | -83% |
| 生成框架 | 1 分鐘 | 30 分鐘 | -97% |
| 分析 | 0.5 分鐘 | - | - |
| AI 填充 | 5 分鐘 | 120 分鐘 | -96% |
| 手動優化 | 30 分鐘 | 60 分鐘 | -50% |
| 檢查 | 3 分鐘 | 15 分鐘 | -80% |
| 發布 | 1 分鐘 | 10 分鐘 | -90% |
| **總計** | **45.5 分鐘** | **265 分鐘** | **-83%** |

---

## 💰 成本分析

### AI API 使用成本

**假設：**
- 18 個 TODO 項目
- 每個平均生成 200 tokens
- Claude API 價格（Sonnet 3.5）:
  - Input: $3 / 1M tokens
  - Output: $15 / 1M tokens

**計算：**
```
Input tokens: 500 × 18 = 9,000
Output tokens: 200 × 18 = 3,600

成本 = (9,000 × $3 + 3,600 × $15) / 1,000,000
    = ($27 + $54) / 1,000,000
    = $0.081 ≈ NT$2.5
```

**結論：** 每篇文章成本約 NT$2.5，超級划算！

### ROI 分析

**假設你的時薪價值：** NT$500

**節省時間：** 265 - 45.5 = 219.5 分鐘 = 3.66 小時

**節省金額：** 3.66 × NT$500 = **NT$1,830**

**投資回報率：** (1830 - 2.5) / 2.5 = **73,120%** 🤯

---

## 🎯 後續行動

### 發布後要做的事

**1. 社群分享（10 分鐘）**
- [ ] 分享到 Twitter
- [ ] 分享到 LinkedIn
- [ ] 分享到相關 Discord/Slack 群組
- [ ] 分享到 PTT 或其他論壇

**2. SEO 優化（15 分鐘）**
- [ ] 提交到 Google Search Console
- [ ] 生成 sitemap
- [ ] 建立內部連結
- [ ] 檢查 meta tags

**3. 互動與更新（持續）**
- [ ] 回覆留言
- [ ] 收集讀者反饋
- [ ] 更新過時資訊
- [ ] 追蹤流量數據

---

## 📊 效果追蹤

### 建議追蹤的指標

**7 天內：**
- 瀏覽量
- 平均停留時間
- 跳出率
- 社群分享次數

**30 天內：**
- 搜尋引擎排名
- 反向連結數量
- 轉換率（如有聯盟連結）
- 讀者互動（留言、分享）

---

## 💡 進階技巧

### 技巧 1：批量生成相關文章

當你完成一篇對比文章後，可以快速衍生出相關文章：

```bash
# 主文：Cursor vs Copilot（已完成）

# 衍生文章 1：Cursor 深度評測
python article_generator.py -t tool_review \
  --title "Cursor 完整使用指南：AI 編程的未來" \
  --tool "Cursor"

# 衍生文章 2：Copilot 最佳實踐
python article_generator.py -t tool_review \
  --title "GitHub Copilot 進階技巧：10 倍提升編程效率" \
  --tool "GitHub Copilot"

# 衍生文章 3：AI 編程工具總覽
python article_generator.py -t comparison \
  --title "2025 年 5 大 AI 編程工具橫向評比" \
  --item-a "AI編程工具" --item-b "傳統IDE"
```

這樣你就有了一個**完整的內容系列**！

### 技巧 2：建立內容日曆

```bash
# Week 1: Cursor vs Copilot（對比）
# Week 2: Cursor 深度評測（單一工具）
# Week 3: AI 編程最佳實踐（教學）
# Week 4: 讀者案例分享（快速筆記）
```

### 技巧 3：重複使用內容

從長文章中提取：
- 社群媒體貼文（Twitter、LinkedIn）
- Email 電子報
- YouTube 影片腳本
- Podcast 大綱

---

## 🎉 恭喜！

你現在已經掌握了高效能的內容創作工作流程！

**記住核心原則：**
1. 🤖 讓 AI 處理重複性工作
2. 👨‍💻 你專注在個人經驗和見解
3. ⚡ 快速迭代，持續優化
4. 📊 用數據驗證效果

**開始你的下一篇文章吧！** 🚀
