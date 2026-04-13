# 點子實驗室 - Hugo 工作流程

## 🎯 現在的流程（已優化）

```
寫文章 → 放到 content/posts/ → git add → git commit → git push → 喝咖啡 ☕ → 網站自動更新！
```

## 🛠️ 系統架構

- **靜態網站生成器**: Hugo (已移除 Jekyll)
- **主題**: Paper 
- **部署**: Netlify (自動部署)
- **編輯**: 自製編輯器 + Hugo 本地預覽

## 📝 寫文章方式

### 方式 1: 使用內建編輯器 (推薦新手)
```bash
# 啟動編輯器 + Hugo 預覽
start.bat
# 選擇選項 2
```

**特色**:
- ✨ 即時 Markdown 預覽
- 📋 Front-matter 助手
- 💾 一鍵下載 .md 檔案
- 🎨 美觀的介面

### 方式 2: Typora + Hugo (推薦進階用戶)
```bash
# 1. 安裝 Typora (付費但值得)
# 2. 啟動 Hugo 預覽
hugo server -D --navigateToChanged

# 3. 用 Typora 編輯 content/posts/ 中的檔案
# 4. 瀏覽器會自動重新整理
```

### 方式 3: VS Code + Hugo
```bash
# 1. 啟動 Hugo 預覽  
hugo server -D

# 2. 用 VS Code 編輯，安裝這些套件：
# - Markdown All in One
# - Hugo Language and Syntax Support
# - Front Matter CMS (可選)
```

## 📁 文章檔案結構

```
content/posts/
├── 2025-06-15-gemini-grounding-vs-rag-interactive.html (互動式內容)
├── 2025-06-14-harry-potter-avatar.md                   (一般文章)
└── _index.md                                           (列表頁設定)
```

### Front-matter 範本

```yaml
---
title: "文章標題"
date: 2025-06-26
draft: false
categories: ["AI工具", "技術解析"]
tags: ["Hugo", "Markdown", "編輯器"]
author: "Justin Lee"
description: "文章簡短描述，用於 SEO 和社群分享"
---
```

## 🚀 部署流程

### 自動部署 (Netlify)
```bash
git add .
git commit -m "新增文章: 標題"
git push origin main
# Netlify 自動偵測並部署，約 2-3 分鐘完成
```

### 本地測試
```bash
# 方式 1: 使用腳本
start.bat

# 方式 2: 直接指令
hugo server -D
```

## 📋 檔案命名規則

```
YYYY-MM-DD-article-title.md
```

**範例**:
- `2025-06-26-hugo-workflow-guide.md`
- `2025-06-26-ai-tools-comparison.md`

## 🎨 特殊內容支援

### 1. 互動式內容 (.html)
- 支援 JavaScript、CSS
- 適合：圖表、互動式範例、工具
- 範例：`2025-06-15-gemini-grounding-vs-rag-interactive.html`

### 2. 一般文章 (.md)
- 標準 Markdown
- 支援：程式碼區塊、數學公式、表格
- 適合：技術文章、觀點分享

## 🗂️ 專案結構 (清理後)

```
idea-hub/
├── content/posts/          # 📝 文章內容 (主要工作區)
├── themes/paper/           # 🎨 Hugo 主題
├── assets/                 # 🖼️ 靜態資源
├── hugo.toml              # ⚙️ Hugo 設定
├── netlify.toml           # 🚀 部署設定  
├── editor.html            # ✏️ 文章編輯器
├── start.bat              # 🔧 啟動腳本
└── archive/jekyll-backup/ # 📦 Jekyll 檔案封存
```

## ☕ 快速開始

1. **寫新文章**:
   ```bash
   start.bat  # 選擇模式 2
   ```

2. **預覽現有文章**:
   ```bash
   hugo server -D
   # 開啟 http://localhost:1313
   ```

3. **發布文章**:
   ```bash
   # 將編輯器下載的 .md 檔案放到 content/posts/
   git add .
   git commit -m "新增: 文章標題"
   git push
   ```

## 🛠️ 故障排除

### Hugo 指令找不到
```bash
# Windows (Chocolatey)
choco install hugo-extended

# 或下載安裝包
# https://github.com/gohugoio/hugo/releases
```

### 編輯器開啟失敗
- 直接雙擊 `editor.html`
- 或用瀏覽器開啟

### Netlify 部署失敗
- 檢查 `hugo.toml` 語法
- 確認 `content/posts/` 中檔案格式正確

---

**現在的工作流程更乾淨、更快速！** 🎉 