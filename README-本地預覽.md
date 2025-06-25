# 🚀 本地預覽方法

由於 Jekyll + Docker 在 Windows 環境中有相容性問題，我為您提供了多種簡單的本地預覽方案：

## 方法 1: VS Code Live Server（推薦）⭐

### 📋 步驟：
1. **安裝 VS Code 擴充功能**：
   - 開啟 VS Code
   - 安裝 "Live Server" 擴充功能（作者：Ritwick Dey）

2. **開啟預覽**：
   - 在 VS Code 中開啟 `index-preview.html`
   - 右鍵點選檔案 → "Open with Live Server"
   - 或按 `Alt+L Alt+O`

3. **自動開啟瀏覽器**：
   - 網址：`http://127.0.0.1:5500/index-preview.html`
   - 支援即時重載，修改後自動重新整理

### ✅ 優點：
- ✅ 快速啟動，無需安裝複雜環境
- ✅ 即時重載，修改即時看到效果
- ✅ 完全沒有相容性問題
- ✅ 適合快速預覽和調整設計

---

## 方法 2: 直接開啟 HTML 檔案

### 📋 步驟：
1. 直接雙擊 `index-preview.html`
2. 使用瀏覽器開啟

### ⚠️ 注意：
- 不支援即時重載
- 修改後需要手動重新整理瀏覽器

---

## 方法 3: Python 簡易伺服器

### 📋 步驟：
1. 開啟 PowerShell 或命令提示字元
2. 切換到專案目錄：`cd D:\GitHub\idea-hub`
3. 執行：`python -m http.server 8000`
4. 開啟瀏覽器：`http://localhost:8000/index-preview.html`

### ✅ 優點：
- ✅ 簡單易用
- ✅ 支援本地伺服器環境

---

## 🎨 客製化預覽檔案

`index-preview.html` 是專門為本地預覽設計的檔案：

### 📝 如何修改：
1. **更新內容**：直接編輯 HTML 中的文字
2. **調整樣式**：修改 `<style>` 標籤中的 CSS
3. **新增文章**：複製 `.post-card` 區塊並修改內容

### 🎯 設計特色：
- 📱 響應式設計，支援各種螢幕尺寸
- 🎨 現代化漸層設計，良好的視覺對比
- ⚡ 快速載入，無外部依賴
- 🔧 易於客製化和修改

---

## 🚀 部署到正式環境

當您滿意本地預覽效果後，可以：

1. **提交變更**：
   ```bash
   git add -A
   git commit -m "Update design and content"
   git push origin main
   ```

2. **GitHub Actions 自動部署**：
   - 推送後自動觸發建置
   - 部署到 GitHub Pages
   - 網址：`https://justin2061.github.io/idea-hub`

---

## 🛠️ 故障排除

### Q: VS Code Live Server 無法啟動？
**A:** 檢查是否正確安裝擴充功能，重新載入 VS Code

### Q: 瀏覽器顯示空白頁面？
**A:** 確認檔案路徑正確，檢查瀏覽器控制台是否有錯誤

### Q: 修改沒有即時顯示？
**A:** 使用 VS Code Live Server 或手動重新整理瀏覽器

### Q: 想要使用 Jekyll 主題效果？
**A:** 等正式部署到 GitHub Pages 後，主題效果會自動套用

---

## 📞 需要協助？

如果遇到任何問題，請：
1. 檢查上述故障排除步驟
2. 確認所有檔案都已正確建立
3. 聯絡我進行進一步協助 