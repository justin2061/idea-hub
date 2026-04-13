# Obsidian + Hugo + Netlify 發布方案

## 🎯 方案 1: Obsidian Git 插件 (推薦)

### 設定步驟

1. **安裝 Obsidian Git 插件**
   - 在 Obsidian 中：設定 → 社群插件 → 瀏覽 → 搜尋 "Obsidian Git"
   - 安裝並啟用

2. **將 content/posts/ 設為 Obsidian Vault**
   ```
   專案結構：
   idea-hub/
   ├── content/posts/  ← 這個資料夾設為 Obsidian Vault
   ├── hugo.toml
   └── netlify.toml
   ```

3. **設定 Obsidian Git**
   - **Backup interval**: 5 分鐘 (自動備份)
   - **Auto pull on startup**: ✅
   - **Auto push**: ✅

4. **工作流程**
   ```
   Obsidian 寫文章 → 自動 Git Push → Netlify 自動部署 → 喝咖啡 ☕
   ```

### 優點
- ✅ 零手動操作
- ✅ 5分鐘內自動發布
- ✅ 離線編輯支援
- ✅ 版本控制自動化

---

## 🎯 方案 2: Obsidian 整合式工作流程 (進階)

### 設定步驟

1. **建立 Obsidian Templates**
   - 安裝 **Templater** 插件
   - 建立文章模板：

   ```javascript
   <%*
   const title = await tp.system.prompt("文章標題:");
   const slug = title.toLowerCase().replace(/\s+/g, '-');
   const today = tp.date.now("YYYY-MM-DD");
   %>---
   title: "<% title %>"
   date: <% today %>
   draft: false
   categories: []
   tags: []
   author: "Justin Lee"
   description: ""
   ---

   ## 開始寫作

   您的內容...
   ```

2. **設定 Front-matter Properties**
   - Obsidian 設定 → Core plugins → Properties → 啟用
   - 可視化編輯 YAML front-matter

3. **調整 Obsidian 設定**
   ```
   Files & Links:
   ├── Use [[Wikilinks]]: ❌ (改用標準 Markdown)
   ├── New link format: Relative path to file
   └── Default location for new attachments: Same folder as current file
   ```

### 優點
- ✅ 更強大的模板系統
- ✅ 視覺化 front-matter 編輯
- ✅ 圖片管理更便利

---

## 🎯 方案 3: 混合式方案 (最佳體驗)

### 同時使用
1. **Obsidian** - 主要寫作環境
2. **內建編輯器** - 快速修改和預覽
3. **Hugo 本地預覽** - 最終檢查

### 工作流程
```bash
# 日常寫作
Obsidian 編輯 → Auto Git Push → 網站更新

# 需要預覽時
start.bat → 選擇模式 1 (Hugo 預覽)
```

---

## 🛠️ 立即設定 Obsidian 方案

### 第一步：將 content/posts 設為 Vault
```bash
# 在 Obsidian 中
File → Open folder as vault → 選擇 D:\GitHub\idea-hub\content\posts
```

### 第二步：安裝關鍵插件
- **Obsidian Git** (自動發布)
- **Templater** (文章模板)
- **Properties** (Front-matter 編輯，Core plugin)

### 第三步：享受無縫寫作體驗！
```
在 Obsidian 寫完文章 → 5分鐘後自動出現在網站 🎉
```

---

## 🎨 額外功能

### 支援的內容類型
- ✅ 標準 Markdown 文章
- ✅ 互動式 HTML 內容 
- ✅ 圖片自動處理
- ✅ 內部連結轉換

### 進階功能 (可選)
- **Quick Switcher** - 快速切換文章
- **Graph View** - 視覺化文章關聯
- **Daily Notes** - 靈感記錄
- **Canvas** - 視覺化規劃

---

## 🚀 結論

**Obsidian + Git + Netlify = 最佳寫作發布體驗**

這個組合讓您可以：
- 📝 專注於寫作，不用考慮技術細節
- ⚡ 自動發布，無需手動操作
- 🔄 版本控制和備份自動化
- 🎨 強大的組織和連結功能

**準備好開始了嗎？** 先設定 Obsidian Git 插件試試看！ 