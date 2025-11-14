# ⚡ 5 分鐘快速入門

想立刻開始用工具寫文章？跟著這個指南 5 分鐘就能上手！

---

## 🚀 第一步：安裝依賴（1 分鐘）

```bash
cd /home/user/idea-hub/_tools
pip install anthropic pyyaml
```

---

## ✍️ 第二步：生成你的第一篇文章（30 秒）

### 選項 A：對比類文章（推薦）

```bash
python article_generator.py \
  --template comparison \
  --title "Claude vs ChatGPT：我的使用心得" \
  --item-a "Claude" \
  --item-b "ChatGPT" \
  --categories "AI工具" \
  --tags "AI" "工具評測"
```

### 選項 B：工具評測

```bash
python article_generator.py \
  --template tool_review \
  --title "Notion AI 使用心得" \
  --tool "Notion AI" \
  --categories "AI工具" \
  --tags "Notion" "生產力"
```

### 選項 C：快速筆記

```bash
python article_generator.py \
  --template quick_note \
  --title "今天學到的 Python 技巧" \
  --categories "技術筆記" \
  --tags "Python"
```

---

## 🤖 第三步：AI 自動填充（可選，5 分鐘）

### 如果你有 Claude API Key：

```bash
# 設定 API Key
export ANTHROPIC_API_KEY="your-api-key-here"

# 自動填充內容
python ai_content_filler.py \
  --file ../_drafts/2025-11-14-*.md \
  --auto
```

### 如果沒有 API Key：

**沒問題！** 直接跳到第四步，手動填寫即可。

---

## ✏️ 第四步：手動編輯（30 分鐘）

打開生成的文章（在 `_drafts` 目錄）：

```bash
# 找到你的文章
ls -la ../_drafts/

# 用編輯器打開（選擇你喜歡的）
code ../_drafts/2025-11-14-your-article.md
# 或
vim ../_drafts/2025-11-14-your-article.md
# 或
nano ../_drafts/2025-11-14-your-article.md
```

**填寫所有 `[ ] TODO` 部分**，加入你的經驗和見解。

---

## 📤 第五步：發布（1 分鐘）

```bash
bash quick_publish.sh \
  ../_drafts/2025-11-14-your-article.md \
  "新增文章：你的文章標題"
```

完成！🎉

---

## 🎯 下一步

現在你已經發布了第一篇文章，可以：

1. **查看完整教學**：閱讀 `README.md`
2. **學習完整工作流**：閱讀 `workflow_example.md`
3. **開始定期創作**：每週寫 1-2 篇文章

---

## ❓ 常見問題

### Q1: 我沒有 API Key 可以用嗎？

**可以！** 不用 API Key 也能用工具生成框架，只是需要手動填寫內容。

### Q2: 生成的文章在哪裡？

在 `_drafts` 目錄。使用 `ls ../_drafts/` 查看。

### Q3: 如何修改文章模板？

編輯 `article_generator.py`，找到對應的模板方法。

### Q4: 發布腳本做了什麼？

1. 移動文章到 `_posts`
2. Git add + commit + push
3. 檢查並警告未完成的 TODO

### Q5: 可以不用 Git 發布嗎？

可以，手動移動文件到 `_posts` 目錄即可。

---

## 💡 小技巧

### 快速生成多篇文章

```bash
# 週一：對比文章
python article_generator.py -t comparison --title "A vs B" --item-a "A" --item-b "B"

# 週三：工具評測
python article_generator.py -t tool_review --title "工具評測" --tool "工具名"

# 週五：快速筆記
python article_generator.py -t quick_note --title "本週學習筆記"
```

### 查看文章完成度

```bash
python ai_content_filler.py --file ../_drafts/your-article.md --analyze
```

---

## 🆘 需要幫助？

1. 查看 `README.md` - 完整使用說明
2. 查看 `workflow_example.md` - 實際案例
3. 提交 Issue 到 GitHub

---

**開始創作吧！** ✍️🚀
