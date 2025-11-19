# 🚀 快速入門：修復 GitHub Actions PR 權限問題

## ⚡ 只需一步即可解決！

### 📋 您需要做的事情（5 分鐘內完成）

前往 Repository Settings 並啟用 PR 創建權限：

```
1. 打開 https://github.com/justin2061/idea-hub/settings/actions

2. 滾動到 "Workflow permissions" 區塊

3. 選擇：
   ● Read and write permissions

4. 勾選：
   ☑ Allow GitHub Actions to create and approve pull requests

5. 點擊 [Save] 按鈕
```

### ✅ 完成後會發生什麼？

所有自動化工作流將立即恢復正常工作：

| 工作流 | 行為 | 說明 |
|--------|------|------|
| 🤖 `fully-auto-content.yml` | ✅ 直接 Push | 自動生成內容並直接發布（最快） |
| 🔧 `auto-fix.yml` | 📝 創建 PR → 自動合併 | 修復問題後自動測試並合併 |
| 📝 `auto-content.yml` | 📋 創建 PR → 等待審查 | 生成內容後等待人工檢查 |

---

## 🧪 測試驗證

完成設置後，測試一下：

```bash
# 測試自動修復工作流
gh workflow run auto-fix.yml

# 或測試自動內容生成
gh workflow run auto-content.yml --raw-field categories=tech --raw-field count=1
```

然後查看：
- Actions 頁面確認運行成功
- Pull Requests 頁面確認 PR 已創建（針對 auto-fix 和 auto-content）

---

## 📚 詳細文檔

更多信息請查看：
- 📖 [完整解決方案文檔](./PR_CREATION_SOLUTION.md)
- 🏗️ [CI/CD 設計文檔](./CI_CD_DESIGN.md)

---

## 🆘 需要幫助？

### 常見問題

**Q: 我沒有 Repository Admin 權限怎麼辦？**
A: 請聯繫 repository 管理員協助設定，或使用替代方案（Personal Access Token）

**Q: 這是組織 (Organization) 的 repository**
A: 可能需要組織管理員權限，請聯繫組織管理員

**Q: 完成設置後仍然失敗**
A: 等待 2-3 分鐘讓設置生效，然後重新運行工作流

---

## 🎯 當前狀態

✅ 所有工作流配置已優化並準備就緒
⏳ 等待您完成 Repository Settings 修改
🚀 完成後立即可用！

---

*創建時間: 2025-11-19*
*估計修復時間: < 5 分鐘*
