# 點子實驗室 | Idea Hub

> 探索 AI、創意、創業與未來工具的專業內容平台

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://justin2061.github.io)
[![Jekyll](https://img.shields.io/badge/Jekyll-4.3-red)](https://jekyllrb.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🎯 專案簡介

點子實驗室是一個基於 Jekyll 的專業內容網站，專注於分享 AI 工具、創意思維、創業洞察與未來科技趨勢。網站採用現代化的響應式設計，提供優質的閱讀體驗。

### ✨ 主要特色

- 🎨 **現代化設計** - 專業的視覺風格與用戶體驗
- 📱 **響應式佈局** - 完美適配各種設備
- 🚀 **高效能** - 靜態網站，載入速度快
- 🔍 **SEO 優化** - 完整的搜尋引擎優化
- 📊 **內容管理** - 分類、標籤、歸檔功能
- 🎯 **專業內容** - 深度的技術與商業分析

## 🛠 技術架構

### 核心技術
- **Jekyll 4.3** - 靜態網站生成器
- **GitHub Pages** - 免費託管服務
- **Liquid** - 模板語言
- **Sass/SCSS** - CSS 預處理器
- **Markdown** - 內容撰寫格式

### 插件與功能
- `jekyll-feed` - RSS 訂閱
- `jekyll-seo-tag` - SEO 優化
- `jekyll-sitemap` - 網站地圖
- `jekyll-paginate` - 分頁功能

## 🚀 快速開始

### 環境需求
- Ruby 2.7 或更高版本
- Bundler
- Git

### 本地開發

1. **克隆專案**
   ```bash
   git clone https://github.com/justin2061/idea-hub.git
   cd idea-hub
   ```

2. **安裝依賴**
   ```bash
   bundle install
   ```

3. **啟動開發伺服器**
   ```bash
   bundle exec jekyll serve
   ```

4. **瀏覽網站**
   開啟瀏覽器訪問 `http://localhost:4000`

### 部署到 GitHub Pages

1. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "Update content"
   git push origin main
   ```

2. **啟用 GitHub Pages**
   - 進入 GitHub 專案設定
   - 找到 "Pages" 選項
   - 選擇 "Deploy from a branch"
   - 選擇 "main" 分支

## 📝 內容管理

### 撰寫新文章

1. **建立文章檔案**
   在 `_posts/` 目錄下建立新檔案，格式：`YYYY-MM-DD-title.md`

2. **文章前置資料**
   ```yaml
   ---
   layout: post
   title: "文章標題"
   date: 2025-01-15
   categories: [分類1, 分類2]
   tags: [標籤1, 標籤2, 標籤3]
   author: Justin Lee
   excerpt: "文章摘要，會顯示在首頁和搜尋結果中"
   ---
   ```

3. **內容撰寫**
   ```markdown
   文章開頭內容...
   
   <!--more-->
   
   詳細內容...
   ```

### 內容分類

**主要分類：**
- `AI工具` - AI 工具評測與應用
- `創意思維` - 創新方法論與實踐
- `創業洞察` - 商業趨勢與創業經驗
- `生產力工具` - 效率提升與工具推薦
- `學習筆記` - 知識整理與心得分享

**標籤使用：**
- 技術相關：`人工智慧`、`機器學習`、`程式開發`
- 商業相關：`商業模式`、`市場分析`、`創業`
- 工具相關：`工具推薦`、`效率提升`、`自動化`

## 🎨 自訂設計

### 修改樣式

主要樣式檔案位於 `assets/css/style.scss`，包含：

- **顏色變數** - 統一的色彩系統
- **響應式設計** - 適配不同螢幕尺寸
- **動畫效果** - 提升用戶體驗
- **組件樣式** - 文章卡片、按鈕等

### 自訂配置

在 `_config.yml` 中可以修改：

```yaml
# 網站基本資訊
title: 你的網站標題
description: 網站描述
author: 作者名稱
email: 聯絡信箱

# 社交媒體連結
social_links:
  github: 你的GitHub用戶名
  twitter: 你的Twitter用戶名
  linkedin: 你的LinkedIn用戶名

# 導航選單
header_pages:
  - about.md
  - categories.md
  - archive.md
```

## 📊 網站結構

```
idea-hub/
├── _posts/              # 文章目錄
├── _layouts/            # 頁面模板（由主題提供）
├── _includes/           # 可重用組件（由主題提供）
├── _sass/               # Sass 樣式檔案（由主題提供）
├── assets/              # 靜態資源
│   └── css/
│       └── style.scss   # 自訂樣式
├── _config.yml          # Jekyll 配置檔案
├── index.md             # 首頁
├── about.md             # 關於頁面
├── categories.md        # 分類頁面
├── archive.md           # 歸檔頁面
├── Gemfile              # Ruby 依賴管理
└── README.md            # 專案說明
```

## 🔧 進階功能

### SEO 優化

網站已整合完整的 SEO 功能：

- **自動生成** meta 標籤
- **結構化資料** 支援
- **Open Graph** 社群分享優化
- **XML Sitemap** 自動生成
- **RSS Feed** 訂閱功能

### 分析與追蹤

在 `_config.yml` 中設定：

```yaml
# Google Analytics
google_analytics: GA_TRACKING_ID

# Google Search Console
google_site_verification: VERIFICATION_CODE
```

### 評論系統

可以整合第三方評論系統：
- Disqus
- Gitalk
- Utterances

## 📈 效能優化

### 圖片優化
- 使用適當的圖片格式（WebP、JPEG、PNG）
- 壓縮圖片檔案大小
- 使用響應式圖片

### 載入速度
- 最小化 CSS 和 JavaScript
- 使用 CDN 加速
- 啟用瀏覽器快取

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 提交 Issue
- 清楚描述問題或建議
- 提供重現步驟（如果是 bug）
- 包含螢幕截圖（如果適用）

### 提交 Pull Request
1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 建立 Pull Request

## 📄 授權條款

本專案採用 [MIT License](LICENSE) 授權條款。

## 📞 聯絡資訊

- **作者：** Justin Lee
- **Email：** [your@email.com](mailto:your@email.com)
- **GitHub：** [@justin2061](https://github.com/justin2061)
- **網站：** [https://justin2061.github.io](https://justin2061.github.io)

## 🙏 致謝

感謝以下開源專案：
- [Jekyll](https://jekyllrb.com/) - 靜態網站生成器
- [Minima](https://github.com/jekyll/minima) - Jekyll 主題
- [GitHub Pages](https://pages.github.com/) - 免費託管服務

---

⭐ 如果這個專案對你有幫助，請給個 Star 支持一下！
