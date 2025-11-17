# 🔄 永動機機制完整說明文檔

## 📋 文檔目的

本文檔詳細說明「永動機系統」的運作機制，包括各個組件的職責、相互關係、觸發條件和失敗恢復流程。

---

## 🎯 永動機核心概念

### 什麼是永動機？

永動機是一個**自動化、自我修復、持續運作**的閉環系統，具備以下特性：

1. **自動執行** - 定時自動觸發，無需人工介入
2. **自我診斷** - 自動檢測系統健康狀態
3. **自我修復** - 發現問題後自動修復
4. **自動驗證** - 修復後自動測試確認
5. **自動重試** - 失敗後自動重新嘗試
6. **閉環運作** - 形成完整的自動化循環

### 設計理念

```
傳統系統：人工 → 操作 → 檢查 → 失敗 → 人工修復 → 重試
永動機：  自動 → 執行 → 監控 → 失敗 → 自動修復 → 自動重試 → 循環
```

---

## 🏗️ 系統架構

### 系統組件層級結構

```
┌─────────────────────────────────────────────────────────┐
│                     永動機系統架構                        │
└─────────────────────────────────────────────────────────┘

第一層：核心功能層
├─ 🤖 fully-auto-content.yml    (內容生成引擎)
└─ 🚀 deploy.yml                (構建測試引擎)

第二層：自我修復層
├─ 🔄 self-healing.yml          (系統總控)
├─ 🔧 auto-fix.yml              (問題修復)
└─ 🤝 auto-merge-pr.yml         (PR 自動處理)

第三層：支援工具層
├─ 📊 system_monitor.py         (系統監控)
├─ 🤖 auto_content_generator.py (內容生成)
├─ 🔧 auto_fixer.py             (問題掃描修復)
└─ 🧪 test_*.py                 (測試套件)
```

---

## 🔄 完整運作流程

### 階段 1：正常運作循環

```
┌──────────────────────────────────────────────┐
│           ⏰ 定時觸發 (週一/三/五 9:00)        │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   🤖 fully-auto-content.yml 自動執行          │
│                                               │
│   步驟:                                       │
│   1. 從 Hacker News/Reddit/News API 搜索話題 │
│   2. 使用 Claude AI 生成 6 篇文章            │
│   3. 驗證品質 (字數、格式、結構)             │
│   4. 自動 commit 並 push                     │
└──────────────────────────────────────────────┘
                    ↓
         ┌──────────┴───────────┐
         │   是否生成成功？      │
         └──────────┬───────────┘
              YES  │   NO
                   │    │
                   │    └──────→ 觸發 self-healing.yml
                   │             (進入階段 2：失敗恢復)
                   ↓
┌──────────────────────────────────────────────┐
│   🚀 deploy.yml 自動觸發 (push 到 main)       │
│                                               │
│   步驟:                                       │
│   1. 構建 Jekyll 網站                        │
│   2. 運行完整測試套件                        │
│      - HTML 驗證                             │
│      - 連結檢查                              │
│      - 內容品質                              │
│      - SEO 驗證                              │
│      - 效能測試                              │
│   3. 上傳 artifacts                          │
└──────────────────────────────────────────────┘
                    ↓
         ┌──────────┴───────────┐
         │   測試是否通過？      │
         └──────────┬───────────┘
              YES  │   NO
                   │    │
                   │    └──────→ 觸發 self-healing.yml
                   │             (進入階段 2：失敗恢復)
                   ↓
┌──────────────────────────────────────────────┐
│   🌐 自動部署到 GitHub Pages                 │
│                                               │
│   - Jekyll workflow 自動觸發                 │
│   - 網站自動更新                             │
│   - 2-5 分鐘後可訪問                         │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   📊 創建每日報告 Issue                       │
│                                               │
│   包含:                                       │
│   - 生成的文章列表                           │
│   - 品質驗證結果                             │
│   - 快速連結                                 │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   ⏰ 等待下次觸發 (持續監控中)               │
│                                               │
│   - 每小時健康檢查                           │
│   - 每天凌晨 2:00 自動修復掃描               │
└──────────────────────────────────────────────┘
                    ↓
            回到步驟 1 (循環)
```

### 階段 2：失敗恢復循環

```
┌──────────────────────────────────────────────┐
│   ❌ 檢測到失敗                               │
│                                               │
│   觸發來源:                                   │
│   - fully-auto-content.yml 失敗              │
│   - deploy.yml 失敗                          │
│   - 每小時健康檢查發現問題                   │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   🔄 self-healing.yml 自動啟動               │
│                                               │
│   Job 1: 健康檢查                            │
│   - 檢查最近 workflow runs                   │
│   - 統計失敗次數                             │
│   - 識別失敗的 workflow                      │
│   - 判斷是否需要修復                         │
└──────────────────────────────────────────────┘
                    ↓
         ┌──────────┴───────────┐
         │   是否需要修復？      │
         └──────────┬───────────┘
              YES  │   NO
                   │    │
                   │    └──────→ 創建健康報告
                   │             結束
                   ↓
┌──────────────────────────────────────────────┐
│   Job 2: 自動診斷和修復                      │
│                                               │
│   步驟 1: 診斷問題                           │
│   - 運行 auto_fixer.py scan                  │
│   - 識別所有潛在問題                         │
│   - 分類問題類型                             │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   步驟 2: 應用修復                           │
│   - 運行 auto_fixer.py fix                   │
│   - 修復可處理的問題:                        │
│     • 死連結修復                             │
│     • 格式錯誤修正                           │
│     • 缺少 front matter                      │
│     • 圖片路徑修正                           │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   步驟 3: 驗證修復                           │
│   - 重新構建 Jekyll                          │
│   - 運行測試確認修復有效                     │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   步驟 4: 提交修復                           │
│   - Git add 所有變更                         │
│   - Git commit 詳細說明                      │
│   - Git push 到當前分支                      │
└──────────────────────────────────────────────┘
                    ↓
         ┌──────────┴───────────┐
         │   修復是否成功？      │
         └──────────┬───────────┘
              YES  │   NO
                   │    │
                   │    └──────→ 創建 Issue 通知人工
                   │             (needs-attention 標籤)
                   ↓
┌──────────────────────────────────────────────┐
│   Job 3: 自動重試失敗任務                    │
│                                               │
│   步驟 1: 等待變更傳播 (5 分鐘)             │
│   步驟 2: 識別原失敗的 workflow              │
│   步驟 3: 使用 gh CLI 重新觸發:              │
│      - 如果是內容生成失敗 → 重新生成         │
│      - 如果是部署失敗 → 重新部署             │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   Job 4: 監控和報告                          │
│                                               │
│   - 創建詳細的修復報告 Issue                 │
│   - 包含修復步驟和結果                       │
│   - 標記 self-healing, fixed 標籤            │
└──────────────────────────────────────────────┘
                    ↓
         回到階段 1 (正常運作循環)
```

### 階段 3：PR 自動處理流程

```
┌──────────────────────────────────────────────┐
│   📝 PR 創建                                  │
│                                               │
│   來源:                                       │
│   - 🔧 auto-fix.yml 創建修復 PR              │
│   - 其他自動化工具創建的 PR                  │
│                                               │
│   條件:                                       │
│   - PR 必須有 'automated' 標籤               │
│   - 或由 github-actions[bot] 創建            │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   🤝 auto-merge-pr.yml 自動觸發              │
│                                               │
│   步驟 1: Checkout PR 代碼                   │
│   步驟 2: 安裝依賴 (Ruby, Python, Node)      │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   步驟 3: 構建網站                           │
│   - bundle exec jekyll build                 │
│   - 確認構建成功                             │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   步驟 4: 運行完整測試套件                   │
│                                               │
│   測試項目:                                   │
│   1. test_links.py - 連結驗證                │
│   2. test_content.py - 內容品質              │
│   3. test_seo.py - SEO 檢查                  │
│                                               │
│   結果: 記錄失敗測試數量                     │
└──────────────────────────────────────────────┘
                    ↓
         ┌──────────┴───────────┐
         │   所有測試通過？      │
         └──────────┬───────────┘
              YES  │   NO
                   │    │
                   ↓    └──────→ 創建失敗評論
┌──────────────────┐             觸發 self-healing
│  步驟 5: 自動審核 │             (回到階段 2)
│  - 創建 APPROVE   │
│  - 添加通過評論   │
└─────────┬─────────┘
          ↓
┌──────────────────────────────────────────────┐
│   步驟 6: 自動合併                           │
│                                               │
│   - 使用 squash 合併方式                     │
│   - 生成合併 commit 訊息                     │
│   - 合併到 main 分支                         │
│   - 添加成功評論                             │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   🚀 觸發部署                                 │
│                                               │
│   - Push 到 main 觸發 deploy.yml             │
│   - 執行構建和測試                           │
│   - 部署到 GitHub Pages                      │
└──────────────────────────────────────────────┘
                    ↓
         回到階段 1 (正常運作循環)
```

---

## 📊 各 Workflow 詳細說明

### 1. fully-auto-content.yml - 內容生成引擎

**職責**: 自動生成高質量文章內容

**觸發條件**:
- **定時**: 每週一、三、五早上 9:00 (台灣時間)
- **手動**: workflow_dispatch

**執行流程**:

```yaml
1. Setup 環境
   - Checkout 代碼
   - 配置 Git
   - 安裝 Python 3.11
   - 安裝依賴: anthropic, requests, pyyaml, beautifulsoup4

2. 統計當前文章數 (before_stats)
   - 計算 _posts/ 中現有文章數量

3. 生成文章 (generate)
   - 讀取參數: categories (預設 all), count (預設 1)
   - 運行 auto_content_generator.py
   - 對每個分類:
     a. 搜索熱門話題 (Hacker News, Reddit, News API)
     b. 選擇最相關的話題
     c. 使用 Claude 3.5 Sonnet 生成文章 (2000-3000 字)
     d. 生成 front matter (title, date, categories, excerpt)
     e. 保存為 _posts/YYYY-MM-DD-title.md
   - 計算生成的文章數量
   - 如果數量為 0，退出並報錯

4. 品質驗證 (validate)
   - 對每篇新文章:
     a. 檢查 front matter 是否存在
     b. 檢查必要欄位: title, date
     c. 檢查字數 (最少 1500 字)
     d. 檢查內容結構 (是否有章節標題 ##)
   - 記錄失敗數和警告數
   - 如果有失敗，退出並回滾

5. 生成文章列表 (article_list)
   - 提取每篇文章的:
     • 標題
     • 分類
     • 字數
   - 格式化為 Markdown 列表

6. 自動提交和推送 (commit)
   - git add 所有新文章
   - 生成詳細 commit 訊息 (使用 heredoc)
   - git commit -F commit_message.txt
   - git push origin 當前分支

7. 生成統計資訊 (stats)
   - 計算總文章數
   - 計算總字數
   - 計算平均字數
   - 輸出到 GITHUB_STEP_SUMMARY

8. 創建每日報告 Issue (create_issue)
   - 使用 github-script
   - 提取所有 GitHub 表達式為變量 (避免模板字串衝突)
   - 構建報告內容:
     • 生成時間
     • 文章數量
     • 文章列表
     • 詳細統計
     • 快速連結
   - 創建 Issue with 標籤: auto-generated, daily-report

9. Slack 通知 (optional)
   - 如果配置了 SLACK_WEBHOOK
   - 發送成功或失敗通知

10. 失敗清理 (cleanup)
    - 如果任何步驟失敗
    - git reset --hard HEAD
    - 回滾所有更改
    - 觸發 self-healing (透過 workflow_run)
```

**輸出**:
- 6 篇新文章 (預設，可調整)
- Git commit 到當前分支
- 每日報告 Issue

**失敗處理**:
- 自動回滾所有更改
- 觸發 self-healing.yml (透過 workflow_run)

---

### 2. self-healing.yml - 系統總控和自我修復

**職責**: 系統健康監控、自動診斷、自動修復、自動重試

**觸發條件**:
- **workflow_run**: fully-auto-content.yml 或 deploy.yml 完成時
- **定時**: 每小時一次
- **手動**: workflow_dispatch

**執行流程**:

```yaml
Job 1: health-check (系統健康檢查)
  1. Checkout 代碼
  2. 安裝 Python
  3. 檢查系統健康:
     - 使用 gh CLI 獲取最近 10 次 workflow runs
     - 統計失敗次數
     - 識別失敗的 workflow 名稱
     - 判斷是否需要修復:
       • 如果有失敗 → needs_healing=true
       • 否則 → needs_healing=false
  4. 生成健康報告
  5. 輸出:
     - needs_healing (true/false)
     - failed_workflow (失敗的 workflow 名稱)
     - failed_runs (失敗次數)

Job 2: auto-fix (自動診斷和修復)
  條件: needs_healing == 'true'

  1. Checkout 代碼
  2. 安裝 Ruby + Python
  3. 安裝所有依賴

  4. 診斷問題 (diagnose):
     - 運行 auto_fixer.py scan
     - 生成 diagnosis.json
     - 包含所有發現的問題:
       • 死連結
       • 格式錯誤
       • 缺少 front matter
       • 圖片路徑問題
     - 輸出問題數量

  5. 應用修復 (fix):
     - 運行 auto_fixer.py fix
     - 自動修復可處理的問題
     - 生成 fix_result.json
     - 輸出修復數量

  6. 驗證修復 (verify):
     - bundle exec jekyll build
     - 運行測試套件
     - 確認修復有效

  7. 提交修復 (commit):
     - git config user.name "Self-Healing Bot"
     - git add -A
     - 生成詳細 commit 訊息 (heredoc)
     - git commit -F commit_msg.txt
     - git push origin 當前分支

  8. 輸出:
     - fix_applied (true/false)
     - fixed_count (修復數量)

Job 3: auto-retry (自動重試)
  條件: fix_applied == 'true'

  1. 等待變更傳播 (5 分鐘)
     - sleep 300

  2. 重新觸發失敗的 workflow:
     - 識別 failed_workflow 名稱
     - 如果包含 "Auto Generate":
       • gh workflow run fully-auto-content.yml
     - 如果包含 "Deploy":
       • gh workflow run deploy.yml

  3. 記錄重試操作

Job 4: monitor-and-report (監控和報告)
  條件: always() (總是執行)

  1. 生成綜合報告:
     - 收集所有 job 的結果
     - 判斷整體狀態

  2. 創建報告 Issue:
     - 如果修復成功:
       • 標題: "✅ 自我修復成功 - DATE"
       • 內容: 修復流程、結果統計
       • 標籤: self-healing, fixed

     - 如果修復失敗:
       • 標題: "⚠️ 需要人工介入 - DATE"
       • 內容: 問題描述、建議檢查項目
       • 標籤: self-healing, needs-attention

  3. 更新 dashboard:
     - 輸出執行結果表格
     - 顯示系統狀態
```

**核心邏輯**:
```
檢測失敗 → 診斷問題 → 應用修復 → 驗證修復 →
提交修復 → 等待 5 分鐘 → 重新觸發原任務 → 創建報告
```

**失敗處理**:
- 如果自動修復失敗，創建 Issue 通知人工
- 不會無限重試，避免資源浪費

---

### 3. auto-merge-pr.yml - PR 自動處理

**職責**: 自動測試、審核、合併 Bot 創建的 PR

**觸發條件**:
- **pull_request**: opened, synchronize, reopened
- **條件**:
  - PR 由 github-actions[bot] 創建
  - 或 PR 標題包含 "🔧 自動修復" 或 "🤖 自動生成"
  - 或 PR 有標籤: auto-fix, automated

**執行流程**:

```yaml
1. Checkout PR 代碼
   - 使用 PR 的 head ref
   - fetch-depth: 0 (完整歷史)

2. Setup 環境
   - Ruby 3.1 with bundler cache
   - Python 3.11
   - 安裝所有依賴

3. 構建網站 (build)
   - bundle exec jekyll build --verbose
   - JEKYLL_ENV=production
   - 輸出 build_status

4. 運行所有測試 (test)
   - 初始化失敗計數器: FAILED=0

   測試 1: 連結檢查
   - python _tests/test_links.py
   - 失敗則 FAILED++

   測試 2: 內容品質
   - python _tests/test_content.py
   - 失敗則 FAILED++

   測試 3: SEO 檢查
   - python _tests/test_seo.py
   - 失敗則 FAILED++

   - 輸出 failed_tests 數量
   - 輸出 test_status (success/failed)

5. 測試摘要 (summary)
   - 輸出到 GITHUB_STEP_SUMMARY
   - 顯示構建和測試狀態

6. 自動審核 (approve)
   條件: test_status == 'success'

   - 使用 github-script
   - 創建 PR review:
     • event: 'APPROVE'
     • body: "✅ 自動審核通過..."

7. 自動合併 (merge)
   條件: test_status == 'success'

   - 使用 github.rest.pulls.merge
   - 參數:
     • merge_method: 'squash'
     • commit_title: '🤖 Auto-merge: ...'
     • commit_message: 'Automatically merged...'

   - 添加成功評論

   - 如果合併失敗:
     • 添加失敗評論
     • 拋出錯誤

8. 測試失敗處理 (on failure)
   條件: test_status == 'failed'

   - 添加失敗評論:
     • 說明有多少測試失敗
     • 提供檢查項目清單

   - 觸發 self-healing:
     • gh workflow run self-healing.yml
     • --field force_fix=true
```

**核心邏輯**:
```
PR 創建 → 檢查條件 → 構建 → 測試 →
測試通過 → 審核 → 合併 → 觸發部署
測試失敗 → 評論 → 觸發 self-healing
```

**安全機制**:
- 只處理有特定標籤或特定 actor 的 PR
- 所有測試必須通過才能合併
- 失敗時不會強制合併

---

### 4. auto-fix.yml - 自動問題修復

**職責**: 定期掃描和修復常見問題

**觸發條件**:
- **定時**: 每天凌晨 2:00
- **workflow_run**: deploy.yml 失敗後
- **手動**: workflow_dispatch

**執行流程**:

```yaml
Job 1: detect-and-fix (檢測和修復)
  條件: 上游 workflow 失敗或定時觸發

  1. Checkout 代碼
  2. Setup Ruby + Python
  3. 安裝依賴

  4. 構建網站:
     - bundle exec jekyll build
     - JEKYLL_ENV=production

  5. 掃描問題 (scan):
     - python _tests/auto_fixer.py scan > scan_report.json
     - 使用 jq 提取 total_issues
     - 輸出 issues_count

  6. 自動修復 (fix):
     條件: issues_count > 0

     - python _tests/auto_fixer.py fix > fix_report.json
     - 提取 fixed_count
     - 輸出 fixed_count

  7. 驗證修復 (verify):
     條件: fixed_count > 0

     - bundle exec jekyll build
     - python _tests/test_runner.py

  8. 創建 PR (create_pr):
     條件: fixed_count > 0

     使用 peter-evans/create-pull-request@v6:
     - branch: auto-fix/issues-{run_number}
     - delete-branch: true
     - title: "🔧 自動修復：{count} 個問題"
     - body: 詳細修復報告
     - labels: auto-fix, automated, auto-merge

     ⭐ auto-merge 標籤會觸發 auto-merge-pr.yml

  9. PR 創建摘要:
     - 顯示 PR 號碼
     - 顯示修復數量
     - 說明將自動合併

  10. 創建無法修復問題的 Issue:
      條件: issues_count > fixed_count

      - 使用 github-script
      - 讀取 scan_report.json 和 fix_report.json
      - 找出無法修復的問題
      - 構建 Issue 內容 (使用字串拼接避免模板字串問題)
      - 創建 Issue with 標籤: bug, needs-review, automated

  11. 摘要:
      - 總問題數
      - 自動修復數
      - 需要人工處理數

Job 2: performance-optimization (效能優化)
  平行執行

  1. Checkout 代碼

  2. 優化圖片:
     - 安裝 optipng, jpegoptim
     - 壓縮所有 PNG (optipng -o2)
     - 壓縮所有 JPG (jpegoptim --max=85)

  3. 檢查大文件:
     - find . -type f -size +1M
     - 列出所有 > 1MB 的文件

  4. 創建優化 PR:
     - 如果有變更
     - 創建 PR with 標籤: performance, automated
```

**可修復的問題類型**:
1. 死連結 (404 links)
2. 圖片路徑錯誤
3. 缺少 front matter
4. Markdown 格式錯誤
5. 過多空白行
6. 行尾空白

**創建的 PR 流程**:
```
auto-fix 創建 PR →
auto-merge-pr 檢測到 'auto-merge' 標籤 →
運行測試 → 自動合併 → 觸發部署
```

---

### 5. deploy.yml - 構建測試部署

**職責**: 構建 Jekyll 網站、運行測試、部署到 GitHub Pages

**觸發條件**:
- **push**: main 或 master 分支
- **pull_request**: main 或 master 分支
- **手動**: workflow_dispatch

**執行流程**:

```yaml
Job 1: build-and-test (構建和測試)

  1. Checkout 代碼
  2. Setup Ruby 3.1 with bundler cache
  3. Setup Node.js 18

  4. 安裝依賴:
     - gem install bundler
     - bundle install
     - npm install -g htmlhint html-validator-cli broken-link-checker

  5. 構建 Jekyll:
     - bundle exec jekyll build --verbose
     - JEKYLL_ENV=production

  6. 生成構建報告:
     - 計算總文件數
     - 計算總大小
     - 計算 HTML 頁面數
     - 輸出到 GITHUB_STEP_SUMMARY

  7. HTML 驗證 (continue-on-error):
     - htmlhint _site/**/*.html
     - 生成報告

  8. 連結檢查 (continue-on-error):
     - pip install -r _tests/requirements.txt
     - python _tests/test_links.py

  9. 內容品質檢查 (continue-on-error):
     - python _tests/test_content.py

  10. SEO 驗證 (continue-on-error):
      - python _tests/test_seo.py

  11. 效能測試 (continue-on-error):
      - python _tests/test_performance.py

  12. 上傳測試報告:
      - actions/upload-artifact@v4
      - 名稱: test-reports

  13. 上傳網站 artifact:
      - actions/upload-artifact@v4
      - 名稱: site-build
      - 路徑: _site/
      - 保留 7 天

Job 2: deploy (部署到 VM)
  ⚠️ 目前已停用 (全部註釋)

  原因: 在 if 條件中無法訪問 secrets
  替代: 使用 GitHub Pages 自動部署

Job 3: post-deployment-test (部署後測試)
  ⚠️ 目前已停用 (因為 VM 部署已停用)

Job 4: notify (通知)
  條件: always()
  依賴: build-and-test

  1. 創建摘要:
     - 顯示 Build & Test 結果
     - 說明 VM Deploy 已停用
     - 說明使用 GitHub Pages

  2. Slack 通知 (optional):
     - 如果配置了 SLACK_WEBHOOK
     - 發送構建和測試結果
```

**重要**:
- VM 部署已完全停用
- 使用 GitHub Pages 進行部署 (jekyll.yml)
- 所有測試使用 continue-on-error，不會阻止部署

---

## 🔗 組件間的觸發關係

### 觸發關係圖

```
┌─────────────────────────────────────────────────────────┐
│                   觸發關係完整圖                          │
└─────────────────────────────────────────────────────────┘

定時觸發 (Cron)
├─ 週一/三/五 9:00 → fully-auto-content.yml
├─ 每小時 → self-healing.yml (健康檢查)
└─ 每天 2:00 → auto-fix.yml

Push 觸發
└─ push to main → deploy.yml

Workflow Run 觸發
├─ fully-auto-content.yml 完成 → self-healing.yml
└─ deploy.yml 完成 → auto-fix.yml (如果失敗)

Pull Request 觸發
└─ PR 創建/更新 (有 automated 標籤) → auto-merge-pr.yml

手動觸發 (Workflow Dispatch)
├─ self-healing.yml (強制修復)
├─ fully-auto-content.yml (手動生成)
├─ auto-fix.yml (手動修復)
└─ deploy.yml (手動部署)

連鎖反應
fully-auto-content.yml 成功
    → push to main
        → deploy.yml
            → jekyll.yml (GitHub Pages 部署)

fully-auto-content.yml 失敗
    → self-healing.yml
        → auto-fix.yml (診斷修復)
            → 創建 PR
                → auto-merge-pr.yml
                    → 測試通過
                        → 合併 PR
                            → push to main
                                → deploy.yml
                                    → 回到正常流程

auto-fix.yml 發現問題
    → 創建 PR (with auto-merge 標籤)
        → auto-merge-pr.yml
            → 自動合併
                → push to main
                    → deploy.yml

deploy.yml 失敗
    → self-healing.yml
        → 修復並重試
```

### 關鍵觸發點說明

1. **fully-auto-content.yml → self-healing.yml**
   ```yaml
   # self-healing.yml
   on:
     workflow_run:
       workflows: ["🤖 Fully Auto Generate & Publish"]
       types: [completed]
   ```
   只要 fully-auto-content.yml 完成（無論成功或失敗），都會觸發 self-healing

2. **auto-fix.yml → auto-merge-pr.yml**
   ```yaml
   # auto-fix.yml 創建 PR 時添加標籤
   labels: |
     auto-fix
     automated
     auto-merge

   # auto-merge-pr.yml 檢測標籤
   if: |
     contains(github.event.pull_request.labels.*.name, 'auto-merge') ||
     contains(github.event.pull_request.labels.*.name, 'automated')
   ```

3. **self-healing.yml 重新觸發原失敗任務**
   ```bash
   # 修復完成後
   if [[ "$FAILED_WORKFLOW" == *"Auto Generate"* ]]; then
     gh workflow run fully-auto-content.yml
   elif [[ "$FAILED_WORKFLOW" == *"Deploy"* ]]; then
     gh workflow run deploy.yml
   fi
   ```

---

## 🛡️ 失敗恢復機制

### 多層防護策略

```
第一層：預防性檢查
├─ fully-auto-content.yml
│  ├─ 品質驗證（字數、格式、結構）
│  └─ 驗證失敗 → 自動回滾

第二層：自動修復
├─ self-healing.yml
│  ├─ 健康檢查（每小時）
│  ├─ 自動診斷
│  ├─ 自動修復
│  └─ 自動重試

第三層：人工介入
├─ 創建 Issue (needs-attention 標籤)
└─ 詳細錯誤報告
```

### 具體失敗場景處理

#### 場景 1: 文章生成失敗

```
問題: API 速率限制、網路錯誤、內容品質不合格

處理流程:
1. fully-auto-content.yml 檢測失敗
2. 執行回滾: git reset --hard HEAD
3. 觸發 self-healing.yml (workflow_run)
4. self-healing 診斷問題:
   - 檢查 API key 是否有效
   - 檢查網路連接
   - 檢查生成日誌
5. 如果可修復:
   - 調整重試邏輯
   - 添加錯誤處理
   - 提交修復
   - 等待 5 分鐘
   - 重新觸發 fully-auto-content.yml
6. 如果無法修復:
   - 創建 Issue: "⚠️ 需要人工介入"
   - 包含詳細錯誤訊息
   - 等待人工處理
```

#### 場景 2: 構建測試失敗

```
問題: Jekyll 構建錯誤、測試失敗

處理流程:
1. deploy.yml 檢測失敗
2. 觸發 self-healing.yml
3. self-healing 診斷:
   - 檢查 _config.yml
   - 檢查 front matter 格式
   - 檢查 Markdown 語法
4. auto_fixer.py 掃描並修復:
   - 修正 front matter
   - 修正 Markdown 格式
   - 修正連結
5. 創建 PR with 修復
6. auto-merge-pr.yml 自動處理:
   - 測試修復
   - 通過則合併
   - 重新觸發構建
```

#### 場景 3: 自動修復失敗

```
問題: 無法自動診斷或修復

處理流程:
1. self-healing.yml 嘗試修復
2. 修復失敗
3. 創建詳細 Issue:
   標題: "⚠️ 需要人工介入 - DATE"
   內容:
   - 失敗的 workflow
   - 診斷結果
   - 嘗試的修復
   - 建議檢查項目
   標籤: self-healing, needs-attention
4. 系統繼續監控
5. 下次定時觸發時會重試
```

#### 場景 4: PR 自動合併失敗

```
問題: 測試失敗、合併衝突

處理流程:
1. auto-merge-pr.yml 檢測測試失敗
2. 添加失敗評論到 PR
3. 觸發 self-healing.yml --field force_fix=true
4. self-healing 分析 PR 代碼
5. 如果可以修復:
   - 在 PR 分支上提交修復
   - PR 更新會重新觸發 auto-merge-pr.yml
   - 重新測試
6. 如果無法修復:
   - 創建 Issue
   - 保留 PR 供人工審核
```

---

## 📊 監控和維護

### 系統監控工具

#### 1. system_monitor.py

**用途**: 實時監控系統健康狀態

**功能**:
```python
class SystemMonitor:
    def check_workflow_status():
        # 使用 gh CLI 獲取 workflow 狀態
        # 統計成功/失敗率
        # 識別問題 workflow

    def check_content_generation():
        # 統計文章數量
        # 分析生成頻率
        # 檢查最近 7 天產出

    def check_system_health():
        # 綜合健康評估
        # 生成問題和警告列表
        # 輸出狀態: healthy/warning/unhealthy

    def generate_report():
        # 生成完整報告
        # 包含所有統計和建議

    def export_metrics():
        # 導出 JSON 格式指標
        # 供外部監控系統使用
```

**使用方式**:
```bash
# 本地運行監控
cd _tools
python system_monitor.py

# 輸出示例:
# ============================================================
# 🔄 永動機系統監控報告
# ============================================================
#
# ## ✅ 系統狀態: HEALTHY
# 檢查時間: 2024-11-17T10:30:00
#
# ## 📊 Workflow 運行狀態
#
# ### 🤖 Fully Auto Generate & Publish
#   - 總運行: 15 次
#   - 成功: 14 次 (93.3%)
#   - 失敗: 1 次
#   - 進行中: 0 次
#   - 最後運行: 2024-11-17T09:00:00
#
# ### 🔄 Self-Healing System
#   - 總運行: 3 次
#   - 成功: 3 次 (100.0%)
#   - 失敗: 0 次
#
# ## 📝 內容生成狀態
#   - 總文章數: 42
#   - 最近 7 天: 18 篇
#
# ## 🔄 永動機循環狀態
#   循環組件:
#     ✅ ✅ 自動生成
#     ✅ ✅ 自動修復
#     ✅ ✅ 自我修復
#     ✅ ✅ 自動合併
#     ✅ ✅ 自動部署
#
#   🎉 所有組件就緒，永動機正常運作！
```

### 監控指標

#### 關鍵績效指標 (KPIs)

1. **內容生成成功率**
   - 目標: > 95%
   - 計算: 成功運行 / 總運行
   - 監控: system_monitor.py

2. **Self-healing 成功率**
   - 目標: > 80%
   - 計算: 成功修復 / 總失敗
   - 監控: GitHub Issues (self-healing 標籤)

3. **平均修復時間 (MTTR)**
   - 目標: < 10 分鐘
   - 計算: 失敗時間 → 修復完成時間
   - 監控: Workflow 執行時間

4. **系統可用時間**
   - 目標: > 99%
   - 計算: 正常運行時間 / 總時間
   - 監控: 每小時健康檢查

5. **人工介入頻率**
   - 目標: < 1 次/週
   - 計算: needs-attention Issues / 週
   - 監控: GitHub Issues

### 每週維護檢查清單

```
□ 檢查 needs-attention Issues (處理人工介入請求)
□ 審查最近 7 天生成的文章品質（抽樣 2-3 篇）
□ 檢查 Anthropic API 使用量和成本
□ 運行 system_monitor.py 查看系統健康
□ 檢查 self-healing 成功率
□ 審查任何異常的 workflow 失敗
□ 確認 GitHub Actions 配額充足
```

### 月度維護檢查清單

```
□ 全面審查生成的內容品質
□ 分析內容生成趨勢（話題分佈、字數）
□ 檢查和優化 API 使用成本
□ 審查 self-healing 效果（修復成功率、常見問題）
□ 更新依賴版本（Python packages, Ruby gems）
□ 備份重要數據（可選，GitHub 已自動備份）
□ 評估是否需要調整生成頻率或數量
```

---

## 🔧 配置和調整

### 調整生成頻率

**文件**: `.github/workflows/fully-auto-content.yml`

```yaml
# 當前配置: 週一、三、五 9:00
schedule:
  - cron: '0 1 * * 1,3,5'  # UTC 1:00 = 台灣 9:00

# 調整為每天
schedule:
  - cron: '0 1 * * *'

# 調整為只有週一
schedule:
  - cron: '0 1 * * 1'

# 調整為一週兩次（週二、週五）
schedule:
  - cron: '0 1 * * 2,5'
```

### 調整文章數量

**文件**: `.github/workflows/fully-auto-content.yml`

```yaml
# 方法 1: 修改預設值
inputs:
  count:
    default: '1'  # 改為 2 則每次生成 12 篇（6分類×2）

# 方法 2: 修改環境變數
env:
  DEFAULT_ARTICLE_COUNT: 2
```

### 調整品質標準

**文件**: `.github/workflows/fully-auto-content.yml`

```yaml
env:
  MIN_WORDS: 1500  # 最少字數，可調整為 2000
  MIN_QUALITY_SCORE: 7  # 品質分數 0-10
```

**文件**: `_tools/auto_content_generator.py`

```python
# 調整文章長度
ARTICLE_MIN_WORDS = 2000  # 最少字數
ARTICLE_TARGET_WORDS = 3000  # 目標字數
ARTICLE_MAX_WORDS = 4000  # 最多字數

# 調整提示詞以控制品質
GENERATION_PROMPT = f"""
請生成一篇關於「{topic}」的專業文章。

要求：
- 字數: {ARTICLE_TARGET_WORDS} 字
- 深度: 深入分析，不要淺嘗輒止
- 結構: 清楚的章節劃分
- 風格: 專業但易讀
- 實例: 包含實際案例
"""
```

### 添加新的內容分類

**文件**: `_tools/auto_content_generator.py`

```python
self.categories = {
    # 現有分類...

    # 新增分類
    'new-category': {
        'name': '新分類名稱',
        'description': '分類描述',
        'keywords': ['關鍵字1', '關鍵字2', '關鍵字3'],
        'search_queries': [
            '搜索詞1',
            '搜索詞2',
            '搜索詞3'
        ],
        'generation_prompt_template': """
        專門為這個分類設計的提示詞模板...
        """
    }
}
```

### 配置 Slack 通知

**步驟**:
1. 在 Slack 創建 Incoming Webhook
2. 在 GitHub Secrets 添加:
   ```
   Name: SLACK_WEBHOOK
   Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```
3. Workflows 會自動檢測並發送通知

---

## 🎓 最佳實踐

### 1. 定期審查生成內容

```
頻率: 每週一次
方法:
1. 隨機抽取 2-3 篇文章
2. 檢查:
   - 內容準確性
   - 語言流暢度
   - 結構完整性
   - SEO 優化
3. 如有問題:
   - 調整提示詞
   - 修改品質標準
   - 更新生成邏輯
```

### 2. 監控 API 使用

```
頻率: 每月初
檢查:
1. 前往 https://console.anthropic.com/
2. 查看 API 使用量
3. 計算成本:
   - 每篇文章 ~$0.05
   - 每月 72 篇 = ~$3.6
4. 確保在預算內
5. 必要時調整生成頻率
```

### 3. 處理 needs-attention Issues

```
頻率: 每週或當收到通知時
步驟:
1. 查看 Issue 詳細內容
2. 了解無法自動修復的原因
3. 手動修復問題
4. 觀察系統是否恢復正常
5. 關閉 Issue 並添加解決方案註釋
6. 考慮是否需要改進自動修復邏輯
```

### 4. 備份重要數據

```
頻率: 每月或重大變更前
方法:
1. GitHub 已自動備份所有內容
2. 可選擇額外備份:
   git clone --mirror https://github.com/YOUR_USERNAME/YOUR_REPO
   tar -czf backup-$(date +%Y%m%d).tar.gz YOUR_REPO.git
3. 備份配置和 secrets（線下安全存儲）
```

### 5. 保持依賴更新

```
頻率: 每季度
檢查:
1. Python packages:
   pip list --outdated
   # 更新 _tools/requirements.txt

2. Ruby gems:
   bundle outdated
   # 更新 Gemfile

3. GitHub Actions:
   # 檢查 .github/workflows/*.yml
   # 更新 actions 版本
   # 例如: actions/checkout@v4 → actions/checkout@v5

4. 測試所有更新
5. 逐步部署
```

---

## 🚨 故障排除

### 常見問題和解決方案

#### 問題 1: Workflow 持續失敗

**症狀**:
- fully-auto-content.yml 每次都失敗
- self-healing 無法修復

**排查步驟**:
```bash
1. 檢查 API Key
   - GitHub → Settings → Secrets
   - 確認 ANTHROPIC_API_KEY 存在且正確

2. 檢查 API 配額
   - 前往 https://console.anthropic.com/
   - 查看是否達到限額

3. 查看詳細日誌
   - GitHub → Actions → 失敗的 workflow
   - 展開每個步驟查看錯誤

4. 本地測試
   cd _tools
   export ANTHROPIC_API_KEY="your-key"
   python auto_content_generator.py --categories ai-tools --count 1
```

**解決方案**:
- 更新 API Key
- 增加 API 配額
- 修復代碼錯誤
- 調整重試邏輯

#### 問題 2: Self-healing 無法啟動

**症狀**:
- Workflow 失敗但 self-healing 沒有觸發

**排查步驟**:
```yaml
1. 檢查 workflow_run 配置
   # self-healing.yml
   on:
     workflow_run:
       workflows: ["🤖 Fully Auto Generate & Publish"]  # 名稱必須完全匹配
       types: [completed]

2. 檢查是否在正確的分支
   # self-healing 只在 main 分支觸發

3. 手動觸發測試
   gh workflow run self-healing.yml --field force_fix=true
```

**解決方案**:
- 確認 workflow 名稱匹配
- 確認在 main 分支
- 手動觸發一次觀察

#### 問題 3: PR 沒有自動合併

**症狀**:
- auto-fix 創建了 PR
- 但 PR 沒有被自動合併

**排查步驟**:
```bash
1. 檢查 PR 標籤
   # 必須有: automated, auto-merge, 或 auto-fix

2. 檢查測試結果
   # 前往 PR 頁面查看 Checks
   # 必須所有測試都通過

3. 查看 auto-merge-pr.yml 日誌
   # GitHub → Actions → Auto Merge PR
```

**解決方案**:
```bash
# 如果標籤缺失
gh pr edit PR_NUMBER --add-label auto-merge

# 如果測試失敗
# 修復問題後推送更新，會重新觸發

# 手動合併
gh pr merge PR_NUMBER --squash
```

#### 問題 4: 生成的文章品質不佳

**症狀**:
- 文章太短
- 內容不相關
- 語言不通順

**排查步驟**:
```python
1. 檢查搜索到的話題
   # 運行生成器並查看選擇的話題
   python auto_content_generator.py --categories ai-tools --count 1

2. 檢查提示詞
   # 打開 auto_content_generator.py
   # 查看 generate_article_with_ai() 方法

3. 測試不同的提示詞
   # 修改提示詞並重新生成
```

**解決方案**:
```python
# 調整提示詞
GENERATION_PROMPT = f"""
你是一位專業的科技作家。請撰寫一篇關於「{topic['title']}」的深度文章。

要求：
1. 字數：2000-3000 字
2. 結構：
   - 引言（說明背景和重要性）
   - 主體（3-4 個主要章節，每章節 500-700 字）
   - 實例（包含 2-3 個實際案例）
   - 結論（總結和展望）
3. 風格：
   - 專業但平易近人
   - 使用具體數據和例子
   - 避免空洞的陳述
4. SEO：
   - 自然使用關鍵字
   - 清楚的標題層級
"""

# 調整溫度和其他參數
response = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8000,
    temperature=0.7,  # 調整為 0.7 獲得更有創意的內容
    messages=[...]
)
```

---

## 📈 效果評估

### 預期效果

#### 第一個月

```
內容產出:
- 總文章數: 72 篇
- 總字數: ~180,000 字
- 平均品質: 良好（AI 生成 + 自動驗證）

系統穩定性:
- 自動生成成功率: > 90%
- Self-healing 成功率: > 75%
- 人工介入次數: 2-3 次

成本:
- API 費用: ~NT$144
- GitHub Actions: 免費（在免費額度內）
- 時間投入: 1-2 小時（監控和調整）
```

#### 第三個月

```
內容產出:
- 總文章數: 216 篇
- 總字數: ~540,000 字
- 品質提升（經過調整優化）

系統穩定性:
- 自動生成成功率: > 95%
- Self-healing 成功率: > 85%
- 人工介入次數: < 1 次/週

優化效果:
- 提示詞優化 3 次
- 新增 2 個內容分類
- 修復邏輯改進 5 次
```

#### 一年後

```
內容產出:
- 總文章數: 864 篇
- 總字數: ~2,160,000 字
- 建立專業內容庫

系統穩定性:
- 完全自動化運行
- 極少需要人工介入
- 系統自我學習和改進

業務效果:
- 網站流量提升
- SEO 排名改善
- 建立專業品牌
- 潛在商業機會

ROI:
- 投入: ~NT$1,728 (API) + 20 小時（監控）
- 價值: ~NT$1,296,000（以人工撰寫計算）
- ROI: 74,900%
```

---

## 🎉 總結

### 永動機系統的核心優勢

1. **完全自動化**
   - 定時觸發，無需人工操作
   - 24/7 持續運行

2. **自我修復**
   - 自動檢測問題
   - 自動診斷和修復
   - 自動重試失敗任務

3. **高度可靠**
   - 多層防護機制
   - 品質驗證
   - 自動回滾

4. **持續改進**
   - 從失敗中學習
   - 自動優化
   - 易於調整配置

5. **成本效益**
   - 極低的運行成本
   - 極高的產出價值
   - 驚人的 ROI

### 關鍵成功因素

1. ✅ **完整的自動化鏈**
   - 從生成到部署全自動
   - 無斷點，無需人工介入

2. ✅ **智能的錯誤處理**
   - 多層次的失敗恢復
   - 從簡單到複雜的修復策略

3. ✅ **閉環的系統設計**
   - 每個環節相互連接
   - 形成自我維持的循環

4. ✅ **可觀測性**
   - 詳細的日誌和報告
   - 實時監控和告警

5. ✅ **靈活的配置**
   - 易於調整參數
   - 易於擴展功能

### 最後的話

這個永動機系統代表了自動化運維的最佳實踐：

- 🤖 **自動執行** - 讓機器做機器擅長的事
- 🔄 **自我修復** - 系統能自己解決大部分問題
- 📊 **持續監控** - 隨時了解系統狀態
- 👨‍💻 **人機協作** - 人類只在必要時介入

通過這個系統，您可以：
- 專注於更有價值的工作
- 建立穩定的內容輸出
- 獲得驚人的時間和成本效益
- 享受真正的「躺平式」內容創作

**永動機已就緒，讓它為您持續創造價值！** 🚀✨

---

*文檔版本: 1.0*
*最後更新: 2024-11-17*
*作者: Claude Code*
