---
layout: single
title: "如何撰寫一份優秀的 Claude.md：提升 AI 協作效率的關鍵指南"
date: 2025-12-01 01:32:54 +0800
categories:
  - AI工具
tags:
  - AI
  - AI工具
  - 人工智慧
excerpt: "在 AI 輔助開發的時代，我們與 AI 的互動方式正在經歷革命性的轉變。Claude、ChatGPT 等大型語言模型已成為開發者的得力助手，但你是否發現，同樣的問題，有些人能讓 AI 產出近乎完美的程式碼，而有些人卻得到模糊不清的回應？關鍵差異往往在於「上下文」的提供方式。"
---

# 如何撰寫一份優秀的 Claude.md：提升 AI 協作效率的關鍵指南

## 引言

在 AI 輔助開發的時代，我們與 AI 的互動方式正在經歷革命性的轉變。Claude、ChatGPT 等大型語言模型已成為開發者的得力助手，但你是否發現，同樣的問題，有些人能讓 AI 產出近乎完美的程式碼，而有些人卻得到模糊不清的回應？關鍵差異往往在於「上下文」的提供方式。

`Claude.md` 正是為了解決這個問題而生的實踐方法——一份專為 AI 助手準備的專案說明文件。透過結構化的資訊提供，你可以讓 AI 更深入理解你的專案架構、編碼風格和業務邏輯，從而獲得更精準、更符合需求的協助。這不僅能節省大量來回溝通的時間，更能顯著提升程式碼品質和開發效率。讓我們深入探討如何撰寫一份真正有效的 `Claude.md`。

## 核心內容

### 📋 什麼是 Claude.md？

`Claude.md` 是一份放置在專案根目錄的 Markdown 文件，專門用來向 AI 助手（如 Claude、ChatGPT 等）說明專案的各項重要資訊。它就像是專案的「使用說明書」，但受眾不是人類開發者，而是 AI 協作夥伴。

這份文件的核心價值在於：

- **減少重複解釋**：將專案背景、架構、慣例一次說明清楚
- **提升回應品質**：AI 能基於完整上下文給出更準確的建議
- **保持一致性**：確保 AI 產出的程式碼符合專案規範
- **加速開發流程**：減少來回確認，直接獲得可用的解決方案

### 🏗️ Claude.md 的核心結構

一份優秀的 `Claude.md` 應該包含以下關鍵區塊：

#### 1. 專案概述（Project Overview）

這是 AI 理解你專案的第一步。應該簡潔但全面地說明：

```markdown
## 專案概述

本專案是一個基於 TypeScript 的 SaaS 平台，提供企業級的資料分析服務。
主要技術棧：
- 前端：Next.js 14 (App Router)、TailwindCSS、shadcn/ui
- 後端：Node.js、Express、PostgreSQL
- 部署：Vercel + Supabase
```

**實用建議**：
- 用 2-3 句話說明專案的核心價值
- 列出主要技術棧（版本號很重要！）
- 說明專案規模（小型工具 vs 企業級應用）

#### 2. 架構說明（Architecture）

這部分幫助 AI 理解程式碼的組織方式：

```markdown
## 專案架構

/app                 # Next.js App Router 頁面
/components          # React 元件
  /ui               # 基礎 UI 元件（shadcn/ui）
  /features         # 功能性元件
/lib                # 共用工具函式
/services           # API 呼叫層
/types              # TypeScript 型別定義
```

**關鍵要點**：
- 使用樹狀圖或清晰的目錄結構
- 解釋每個資料夾的職責
- 說明資料流向（如：UI → Service → API）

#### 3. 編碼規範（Coding Conventions）

這是最容易被忽略但極其重要的部分：

```markdown
## 編碼規範

### 命名慣例
- 元件：PascalCase（例：UserProfile.tsx）
- 函式：camelCase（例：fetchUserData）
- 常數：UPPER_SNAKE_CASE（例：API_BASE_URL）

### 程式碼風格
- 使用函式元件（Function Components），不使用類別元件
- 優先使用 TypeScript 的嚴格模式
- 所有 API 呼叫必須包含錯誤處理
- 使用 Zod 進行資料驗證

### 範例
```typescript
// ✅ 正確
async function fetchUserData(userId: string): Promise<User> {
  try {
    const response = await api.get(`/users/${userId}`);
    return userSchema.parse(response.data);
  } catch (error) {
    logger.error('Failed to fetch user', { userId, error });
    throw new ApiError('User fetch failed');
  }
}

// ❌ 避免
function getUser(id) {
  return fetch('/users/' + id).then(r => r.json());
}
```
```

**實戰技巧**：
- 提供具體的「做」與「不做」範例
- 說明例外情況（什麼時候可以打破規則）
- 包含常見的錯誤模式

#### 4. 關鍵決策與脈絡（Key Decisions & Context）

記錄重要的技術決策，避免 AI 提出已被否決的方案：

```markdown
## 技術決策記錄

### 為什麼使用 Supabase 而非自建後端？
- 團隊規模小（3 人），需要快速迭代
- Supabase 提供即時訂閱功能，符合產品需求
- 成本考量：初期用戶量預估在 10k 以下

### 為什麼不使用 Redux？
- 專案狀態管理需求簡單
- 使用 React Context + Zustand 已足夠
- 避免過度工程化
```

**為什麼這很重要**：
- AI 不會建議你「改用 Redux」（因為你已說明原因）
- 新成員（或未來的你）也能理解決策背景
- 避免重複討論已解決的問題

#### 5. 常見任務指南（Common Tasks）

提供具體的操作範例，讓 AI 知道如何協助你：

```markdown
## 常見開發任務

### 新增一個 API 端點
1. 在 `/app/api/[endpoint]/route.ts` 建立檔案
2. 使用 Zod schema 驗證輸入
3. 在 `/services` 建立對應的服務函式
4. 更新 `/types/api.ts` 的型別定義
5. 撰寫單元測試

### 新增一個頁面
1. 在 `/app/[route]/page.tsx` 建立檔案
2. 使用 Server Component（除非需要客戶端互動）
3. 在 `/components/features` 建立功能元件
4. 更新導航選單（如適用）
```

### 📊 實際案例分析

讓我們看一個真實的對比案例：

**沒有 Claude.md 的情況**：

```
開發者：幫我寫一個使用者登入的功能
AI：好的，這裡是一個基本的登入表單...
[產出使用 class component 的 React 程式碼]

開發者：我們用的是函式元件
AI：抱歉，這是修改後的版本...
[產出沒有 TypeScript 的程式碼]

開發者：需要加上 TypeScript 型別
AI：這是加上型別的版本...
[產出沒有錯誤處理的程式碼]
```

**有 Claude.md 的情況**：

```
開發者：幫我實作使用者登入功能
AI：基於你的專案規範，我會：
- 使用 Next.js App Router 的 Server Actions
- 套用 Zod schema 驗證
- 使用 Supabase Auth
- 遵循你的錯誤處理模式

[直接產出符合專案規範的完整程式碼]
```

時間節省：**從 5 次來回降到 1 次**，品質提升：**首次產出即可使用**。

### 🎯 進階技巧

#### 使用「情境模板」

針對不同類型的任務，提供標準化的模板：

```markdown
## 元件開發模板

當建立新元件時，請遵循以下結構：

```typescript
'use client'; // 僅在需要客戶端互動時使用

import { ComponentProps } from '@/types';
import { cn } from '@/lib/utils';

interface [ComponentName]Props {
  // 明確定義 props
}

export function [ComponentName]({ 
  ...props 
}: [ComponentName]Props) {
  // 1. Hooks（useState, useEffect 等）
  // 2. 事件處理函式
  // 3. 渲染邏輯
  
  return (
    <div className={cn("base-classes", props.className)}>
      {/* 內容 */}
    </div>
  );
}
```
```

#### 記錄已知限制

誠實地說明專案的限制，避免 AI 提出不可行的建議：

```markdown
## 已知限制與約束

- **效能**：目前不支援超過 10MB 的檔案上傳（基礎設施限制）
- **瀏覽器**：不支援 IE11（已明確放棄）
- **API**：第三方 API 有每分鐘 100 次的請求限制
- **資料庫**：PostgreSQL 版本為 14，不支援某些 15+ 的新特性
```

### 📈 維護與更新

`Claude.md` 不是一次性文件，應該隨專案演進：

| 時機 | 更新內容 | 範例 |
|------|---------|------|
| 技術棧變更 | 更新架構說明 | 從 Pages Router 遷移到 App Router |
| 新增編碼規範 | 補充規範章節 | 團隊決定統一使用 Prettier |
| 重大重構 | 更新架構圖 | 引入微服務架構 |
| 踩坑經驗 | 加入「避免」清單 | 某個套件的已知問題 |

**實用建議**：
- 在 PR 審查時檢查是否需要更新 `Claude.md`
- 每季度進行一次完整檢視
- 將更新 `Claude.md` 納入 Definition of Done

## 實際應用

### 🚀 如何開始撰寫你的第一份 Claude.md

**步驟一：建立基本骨架（15 分鐘）**

在專案根目錄建立 `Claude.md`，使用以下模板：

```markdown
# [專案名稱] - AI 協作指南

## 專案概述
[2-3 句話說明專案]

## 技術棧
- 前端：
- 後端：
- 資料庫：
- 部署：

## 專案結構
[貼上主要資料夾結構]

## 編碼規範
[列出 3-5 個最重要的規則]
```

**步驟二：逐步豐富內容（持續進行）**

不要試圖一次寫完所有內容。每次遇到以下情況時更新：
- AI 給出不符合預期的回應 → 補充相關規範
- 新成員問了重複的問題 → 加入常見任務指南
- 做出重要技術決策 → 記錄在決策章節

**步驟三：實戰測試（每週）**

選擇一個實際任務，在與 AI 對話時先分享 `Claude.md`：

```
我需要新增一個使用者設定頁面。
請先閱讀專案根目錄的 Claude.md，
然後根據我們的規範提供實作建議。
```

觀察 AI 的回應品質，調整文件內容。

### 💡 團隊協作場景

**場景一：新成員 Onboarding**

新成員可以透過 `Claude.md` 快速了解專案規範，並使用 AI 輔助學習：

```
新成員 → AI：根據 Claude.md，我應該如何實作一個新的 API 端點？
AI：根據專案規範，你需要...
```

**場景二：程式碼審查**

在 PR 中，可以請 AI 根據 `Claude.md` 檢查程式碼：

```
審查者 → AI：請根據 Claude.md 的編碼規範，
檢查這個 PR 是否符合專案標準。
```

**場景三：重構任務**

大型重構時，AI 可以基於規範提供一致性的修改：

```
開發者 → AI：我們要將所有 API 呼叫改為使用新的錯誤處理模式，
請根據 Claude.md 的規範重構這個檔案。
```

### 🔧 工具整合

將 `Claude.md` 整合到開發流程：

1. **VS Code 擴充功能**：設定快捷鍵快速開啟 `Claude.md`
2. **Git Hooks**：提交前檢查是否需要更新文件
3. **CI/CD**：在部署流程中驗證文件的完整性
4. **文件連結**：在 `README.md` 中明確指向 `Claude.md`

## 總結與展望

### 🎯 關鍵要點回顧

撰寫優秀的 `Claude.md` 的核心原則：

1. **具體勝於抽象**：

---

**參考資料：**
- [Writing a good Claude.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
