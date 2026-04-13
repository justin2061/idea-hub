# Jekyll 檔案封存

## 封存日期
2025-06-26

## 封存原因
專案從 Jekyll + Hugo 雙系統改為純 Hugo 系統，將 Jekyll 相關檔案封存備份。

## 封存內容
- `_config.yml` - Jekyll 主設定檔
- `_data/` - Jekyll 資料檔案
- `_drafts/` - Jekyll 草稿檔案
- `_pages/` - Jekyll 頁面檔案  
- `_posts/` - Jekyll 文章檔案（已轉移到 Hugo content/posts/）
- `_sass/` - Jekyll 樣式檔案
- `_site/` - Jekyll 建置輸出
- `Gemfile` / `Gemfile.lock` - Ruby 依賴管理
- `.jekyll-cache/` - Jekyll 快取
- `404.html` - Jekyll 404 頁面

## 目前狀態
- ✅ Netlify 設定：已改為使用 Hugo (`hugo --gc --minify`)
- ✅ 主要內容：已轉移到 `content/posts/` 
- ✅ 主題：使用 Hugo Paper 主題
- ✅ 設定檔：`hugo.toml`

## 復原方式
如需復原 Jekyll 系統：
1. 將此資料夾內容移回專案根目錄
2. 修改 `netlify.toml` 建置命令為 Jekyll
3. 安裝 Ruby 依賴：`bundle install` 