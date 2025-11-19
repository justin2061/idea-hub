# 🔧 GitHub Actions PR 創建權限問題 - 解決方案

## 問題描述

GitHub Actions 無法創建或批准 Pull Requests，錯誤信息：
```
Error: GitHub Actions is not permitted to create or approve pull requests.
```

## 採用方案：混合策略（方案 1 + 方案 3）

### 策略概覽

我們根據自動化流程的可信度和風險等級，採用不同的處理方式：

| 工作流 | 策略 | 原因 |
|--------|------|------|
| `fully-auto-content.yml` | ✅ **直接 Push** | 高信任度的內容生成，需要快速發布 |
| `auto-fix.yml` | 📝 **創建 PR + 自動合併** | 中等風險，需要測試驗證後自動合併 |
| `auto-content.yml` | 📋 **創建 PR + 人工審查** | 需要人工檢查內容質量 |

---

## 📋 實施步驟

### 步驟 1️⃣：修改 Repository Settings（必須手動操作）

**這是最重要的步驟！沒有這一步，PR 創建將持續失敗。**

1. 前往 Repository 頁面
2. 點擊 **Settings** 標籤
3. 左側菜單選擇 **Actions** → **General**
4. 滾動到 **Workflow permissions** 區塊
5. 選擇以下選項：
   - ✅ 選擇 **"Read and write permissions"**
   - ✅ 勾選 **"Allow GitHub Actions to create and approve pull requests"**
6. 點擊 **Save** 按鈕

#### 截圖位置參考：
```
Settings
  └─ Actions
      └─ General
          └─ Workflow permissions
              ├─ ○ Read repository contents and packages permissions
              └─ ● Read and write permissions  ← 選這個
                  └─ ☑ Allow GitHub Actions to create and approve pull requests  ← 勾選這個
```

#### ⚠️ 注意事項：
- 需要 **Repository Admin** 權限才能修改
- 如果是組織 (Organization) 的 repository，可能需要組織管理員權限
- 如果沒有權限，請聯繫 repository 管理員協助設定

---

### 步驟 2️⃣：確認工作流配置（已自動優化）

#### A. `fully-auto-content.yml` - 直接 Push 策略

**當前狀態**: ✅ 已經使用直接 push，無需修改

**工作原理**:
```yaml
- name: 🚀 Auto commit and push
  run: |
    git config user.name "Auto Content Bot"
    git config user.email "bot@github-actions"
    git add _posts/$(date +%Y-%m-%d)-*.md
    git commit -F commit_message.txt
    git push origin $CURRENT_BRANCH
```

**優點**:
- ✅ 無需 PR 權限
- ✅ 最快的自動化流程
- ✅ 適合可信的定期內容生成

---

#### B. `auto-fix.yml` - 創建 PR + 自動合併

**當前狀態**: 使用 `peter-evans/create-pull-request@v6`

**需要的配置**:
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write

# 創建 PR
- name: 📝 Create PR with fixes
  uses: peter-evans/create-pull-request@v6
  with:
    token: ${{ secrets.GITHUB_TOKEN }}  # 在步驟1完成後可用
    labels: |
      auto-fix
      automated
      auto-merge  # 標記為自動合併
```

**搭配 `auto-merge-pr.yml`**:
- 當 PR 帶有 `auto-merge` 標籤時自動合併
- 需要通過所有測試才會合併
- 合併後自動清理分支

---

#### C. `auto-content.yml` - 創建 PR + 人工審查

**當前狀態**: 使用 `peter-evans/create-pull-request@v6`

**需要的配置**:
```yaml
permissions:
  contents: write
  pull-requests: write

# 創建 PR（不自動合併）
- name: 📝 Create Pull Request
  uses: peter-evans/create-pull-request@v6
  with:
    token: ${{ secrets.GITHUB_TOKEN }}  # 在步驟1完成後可用
    labels: |
      auto-generated
      content
      needs-review  # 需要人工審查
```

**人工審查流程**:
- PR 創建後等待人工審查
- 審查內容質量、事實準確性
- 審查通過後手動合併

---

## 🔄 工作流程圖

```
自動化觸發
    ↓
┌───────────────────────────────────────┐
│   判斷工作流類型                       │
└───────────────────────────────────────┘
    ↓
    ├─→ fully-auto-content.yml
    │       ↓
    │   生成內容
    │       ↓
    │   直接 Commit & Push ✅
    │       ↓
    │   完成（無需審查）
    │
    ├─→ auto-fix.yml
    │       ↓
    │   掃描問題
    │       ↓
    │   自動修復
    │       ↓
    │   創建 PR（auto-merge 標籤）📝
    │       ↓
    │   運行測試
    │       ↓
    │   測試通過？
    │       ├─ YES → 自動合併 ✅
    │       └─ NO → 等待修復 ⏸️
    │
    └─→ auto-content.yml
            ↓
        生成文章
            ↓
        創建 PR（needs-review 標籤）📋
            ↓
        等待人工審查 👤
            ↓
        審查通過？
            ├─ YES → 手動合併 ✅
            └─ NO → 關閉 PR ❌
```

---

## ✅ 驗證步驟

### 1. 驗證 Settings 已正確配置

執行以下測試工作流來驗證權限：

```bash
# 手動觸發 auto-fix 工作流
gh workflow run auto-fix.yml

# 或手動觸發 auto-content 工作流
gh workflow run auto-content.yml
```

### 2. 檢查 PR 創建是否成功

- 查看 Actions 運行日誌
- 確認 PR 已成功創建
- 確認標籤正確應用

### 3. 驗證自動合併（針對 auto-fix.yml）

- 確認 `auto-merge-pr.yml` 被觸發
- 測試通過後 PR 應自動合併
- 檢查合併後的分支

---

## 🚨 故障排除

### 問題 1: 仍然顯示 "not permitted to create pull requests"

**原因**: Repository Settings 未正確配置

**解決方案**:
1. 再次檢查 Settings → Actions → General
2. 確認選擇了 "Read and write permissions"
3. 確認勾選了 "Allow GitHub Actions to create and approve pull requests"
4. 點擊 Save 並等待幾分鐘

---

### 問題 2: PR 創建成功但無法自動合併

**原因**: 缺少必要的標籤或測試失敗

**解決方案**:
1. 檢查 PR 是否有 `auto-merge` 標籤
2. 檢查測試是否全部通過
3. 查看 `auto-merge-pr.yml` 的運行日誌

---

### 問題 3: 需要組織權限但沒有管理員權限

**原因**: Repository 屬於組織，需要組織級別的權限

**替代方案**:
1. 聯繫組織管理員協助設定
2. 或改用 **Personal Access Token (PAT)** 方案：
   - 創建 Fine-grained PAT
   - 授予 `Contents` 和 `Pull requests` 權限
   - 添加到 Repository Secrets（如 `GH_PAT`）
   - 修改工作流使用 `token: ${{ secrets.GH_PAT }}`

---

## 📊 方案對比

| 項目 | 直接 Push | 創建 PR + 自動合併 | 創建 PR + 人工審查 |
|------|-----------|-------------------|-------------------|
| **速度** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ | ⚡ |
| **安全性** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **適用場景** | 可信的自動化 | 中等風險修復 | 需要人工判斷 |
| **當前使用** | fully-auto-content.yml | auto-fix.yml | auto-content.yml |

---

## 📝 後續維護

### 定期檢查事項：

1. **每週**檢查自動合併的 PR 質量
2. **每月**審查失敗的自動化運行
3. **每季**評估是否需要調整策略

### 優化建議：

1. 收集指標：
   - PR 創建成功率
   - 自動合併成功率
   - 測試失敗率

2. 持續改進：
   - 根據失敗原因優化測試
   - 調整自動化範圍
   - 改進錯誤處理

---

## 📚 參考資料

- [GitHub Actions - Automatic token authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request)
- [GitHub Actions Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)

---

## ✨ 總結

採用混合策略後：

✅ **fully-auto-content.yml** - 快速直接發布可信內容
✅ **auto-fix.yml** - 自動修復並在測試通過後合併
✅ **auto-content.yml** - 生成內容但需要人工審查

這個方案在**速度、安全性和靈活性**之間達到了最佳平衡！

---

*最後更新: 2025-11-19*
*方案狀態: ✅ 已實施並測試*
