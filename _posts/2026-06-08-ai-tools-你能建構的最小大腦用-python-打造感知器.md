---
layout: single
title: "你能建構的最小大腦：用 Python 打造感知器"
date: 2026-06-08 01:46:46 +0800
categories:
  - AI工具
tags:
  - AI
  - AI工具
  - 人工智慧
excerpt: "在人工智慧蓬勃發展的今天，深度學習、神經網路這些名詞聽起來既迷人又遙不可及。但你知道嗎？所有複雜的神經網路架構，其實都源自一個極其簡單的概念——感知器（Perceptron）。這個在 1958 年由 Frank Rosenblatt 發明的演算法，可以說是人工智慧領域最基礎的「大腦細胞」。"
---

# 你能建構的最小大腦：用 Python 打造感知器

## 引言：理解 AI 的第一步 🧠

在人工智慧蓬勃發展的今天，深度學習、神經網路這些名詞聽起來既迷人又遙不可及。但你知道嗎？所有複雜的神經網路架構，其實都源自一個極其簡單的概念——感知器（Perceptron）。這個在 1958 年由 Frank Rosenblatt 發明的演算法，可以說是人工智慧領域最基礎的「大腦細胞」。

理解感知器不僅能幫助你掌握機器學習的核心原理，更能讓你親手打造一個真正能「學習」的程式。這不需要昂貴的硬體設備，也不需要複雜的數學背景，只需要一點點好奇心和 Python 基礎知識。讓我們一起探索這個「最小的大腦」，看看它如何從零開始學會做決策。

## 什麼是感知器？從生物神經元說起 🔬

### 生物神經元的啟發

人類大腦中有約 860 億個神經元，每個神經元都在接收訊號、處理資訊，然後決定是否向下一個神經元發送訊號。這個看似簡單的機制，卻造就了人類的智慧。感知器正是模仿這個過程：

- **接收輸入**：就像神經元的樹突接收訊號
- **加權處理**：不同訊號的重要性不同
- **做出決策**：超過某個閾值就「激發」，否則保持沉默

### 感知器的數學本質

從數學角度來看，感知器其實是一個簡單的線性分類器。它的運作可以用以下公式表示：

```
y = f(w₁x₁ + w₂x₂ + ... + wₙxₙ + b)
```

其中：
- **x₁, x₂, ..., xₙ** 是輸入特徵
- **w₁, w₂, ..., wₙ** 是對應的權重
- **b** 是偏差值（bias）
- **f** 是激活函數，通常是階梯函數

這個公式看起來複雜，但本質上就是在做「加權平均」然後「二選一」的決策。

## 從零開始：用 Python 實作感知器 💻

### 基本架構設計

讓我們動手建構一個感知器類別。這個類別需要具備以下核心功能：

```python
import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        """
        初始化感知器
        learning_rate: 學習率，控制每次調整的幅度
        n_iterations: 訓練迭代次數
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
```

### 激活函數：決策的關鍵

激活函數決定了感知器如何做出最終決策。最簡單的激活函數是單位階梯函數：

```python
def activation_function(self, x):
    """
    單位階梯函數：大於等於 0 回傳 1，否則回傳 0
    """
    return np.where(x >= 0, 1, 0)
```

這個函數的美妙之處在於它的簡潔：只要加權和大於等於零，就輸出 1（代表「是」），否則輸出 0（代表「否」）。

### 訓練過程：機器如何學習

訓練是感知器最核心的部分。它透過不斷調整權重來「學習」正確的分類方式：

```python
def fit(self, X, y):
    """
    訓練感知器
    X: 訓練資料 (n_samples, n_features)
    y: 標籤 (n_samples,)
    """
    n_samples, n_features = X.shape
    
    # 初始化權重和偏差
    self.weights = np.zeros(n_features)
    self.bias = 0
    
    # 迭代訓練
    for iteration in range(self.n_iterations):
        for idx, x_i in enumerate(X):
            # 計算線性輸出
            linear_output = np.dot(x_i, self.weights) + self.bias
            # 通過激活函數
            y_predicted = self.activation_function(linear_output)
            
            # 更新權重和偏差
            update = self.learning_rate * (y[idx] - y_predicted)
            self.weights += update * x_i
            self.bias += update
```

這個訓練過程體現了機器學習的核心思想：

1. **預測**：用當前權重做出預測
2. **比較**：將預測結果與實際答案比較
3. **調整**：根據誤差調整權重
4. **重複**：不斷重複直到學會為止

### 預測功能：應用所學

訓練完成後，感知器需要能對新資料做出預測：

```python
def predict(self, X):
    """
    對新資料進行預測
    """
    linear_output = np.dot(X, self.weights) + self.bias
    y_predicted = self.activation_function(linear_output)
    return y_predicted
```

## 實戰演練：解決真實問題 🎯

### 案例一：邏輯閘實作（AND 閘）

讓我們用感知器來實作最基本的邏輯閘——AND 閘。這是一個完美的入門案例：

```python
# AND 閘的訓練資料
X_and = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_and = np.array([0, 0, 0, 1])

# 建立並訓練感知器
perceptron_and = Perceptron(learning_rate=0.1, n_iterations=10)
perceptron_and.fit(X_and, y_and)

# 測試
predictions = perceptron_and.predict(X_and)
print("AND 閘預測結果：", predictions)
# 輸出：[0 0 0 1]
```

成功！感知器完美學會了 AND 閘的邏輯。

### 案例二：簡單的二元分類

讓我們處理一個更實際的問題：根據考試成績和作業完成度預測學生是否及格。

```python
# 訓練資料：[考試成績, 作業完成度]
X_students = np.array([
    [45, 60],   # 不及格
    [55, 70],   # 不及格
    [65, 80],   # 及格
    [75, 85],   # 及格
    [50, 55],   # 不及格
    [80, 90],   # 及格
    [70, 75],   # 及格
    [40, 50]    # 不及格
])

y_students = np.array([0, 0, 1, 1, 0, 1, 1, 0])

# 訓練模型
perceptron_student = Perceptron(learning_rate=0.01, n_iterations=100)
perceptron_student.fit(X_students, y_students)

# 預測新學生
new_student = np.array([[60, 75]])
prediction = perceptron_student.predict(new_student)
print(f"新學生預測結果：{'及格' if prediction[0] == 1 else '不及格'}")
```

### 視覺化理解：決策邊界

感知器本質上是在特徵空間中畫一條線（或超平面）來分隔兩類資料。我們可以視覺化這個過程：

| 特徵空間 | 決策邊界 | 分類結果 |
|---------|---------|---------|
| 二維平面 | 一條直線 | 線的兩側分別是不同類別 |
| 三維空間 | 一個平面 | 平面兩側是不同類別 |
| 高維空間 | 超平面 | 同樣的分隔概念 |

## 感知器的限制與突破 ⚠️

### XOR 問題：經典的困境

感知器有一個著名的限制：無法解決線性不可分的問題。最經典的例子就是 XOR（互斥或）邏輯：

```python
# XOR 閘的資料
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

# 感知器無法學會 XOR
perceptron_xor = Perceptron(learning_rate=0.1, n_iterations=1000)
perceptron_xor.fit(X_xor, y_xor)
predictions = perceptron_xor.predict(X_xor)
# 預測結果會有錯誤
```

為什麼會這樣？因為 XOR 的兩類資料無法用一條直線分開。這個發現在 1969 年幾乎終結了神經網路研究。

### 解決方案：多層感知器

好消息是，只要堆疊多個感知器形成多層網路，就能解決 XOR 等非線性問題。這就是現代深度學習的基礎：

```
輸入層 → 隱藏層（多個感知器）→ 輸出層
```

這個簡單的擴展，開啟了深度學習的大門。

## 實際應用場景 🚀

### 1. 垃圾郵件過濾

感知器可以作為簡單的垃圾郵件分類器：

**輸入特徵：**
- 郵件中「免費」出現次數
- 郵件中「優惠」出現次數
- 郵件中連結數量
- 大寫字母比例

**輸出：**
- 0 = 正常郵件
- 1 = 垃圾郵件

```python
# 實際應用範例
email_features = np.array([
    [0, 0, 1, 0.1],    # 正常郵件
    [5, 3, 10, 0.8],   # 垃圾郵件
    [1, 0, 2, 0.15],   # 正常郵件
    [8, 7, 15, 0.9]    # 垃圾郵件
])

email_labels = np.array([0, 1, 0, 1])

spam_detector = Perceptron(learning_rate=0.01, n_iterations=100)
spam_detector.fit(email_features, email_labels)
```

### 2. 醫療診斷輔助

在醫療領域，感知器可以協助初步診斷：

**應用範例：糖尿病風險評估**
- 輸入：血糖值、BMI、年齡、家族病史
- 輸出：高風險 / 低風險

雖然實際醫療診斷需要更複雜的模型，但感知器可以作為快速篩檢工具。

### 3. 信用評分系統

金融機構可以用感知器進行基本的信用評估：

| 特徵 | 權重影響 |
|-----|---------|
| 收入水平 | 高 |
| 信用歷史長度 | 中 |
| 負債比率 | 高（負向）|
| 逾期記錄 | 高（負向）|

### 4. 工業品質控制

在製造業中，感知器可以快速判斷產品是否合格：

```python
# 產品檢測範例
product_features = np.array([
    [98.5, 2.1, 50],   # [溫度, 厚度誤差, 重量] - 合格
    [95.2, 5.3, 48],   # 不合格
    [99.1, 1.8, 51],   # 合格
])

quality_labels = np.array([1, 0, 1])

quality_checker = Perceptron(learning_rate=0.05, n_iterations=50)
quality_checker.fit(product_features, quality_labels)
```

### 實務建議 💡

在實際應用感知器時，請注意以下幾點：

1. **特徵標準化**：將不同尺度的特徵標準化到相同範圍（如 0-1），可以加快訓練速度
2. **學習率調整**：太大會導致震盪，太小會訓練緩慢，建議從 0.01 開始嘗試
3. **資料平衡**：確保兩類資料數量相近，避免模型偏向多數類
4. **適用性評估**：先確認問題是否線性可分，否則考慮使用多層網路

## 從感知器到深度學習：進階之路 🌟

### 感知器的演化樹

```
感知器（1958）
    ↓
多層感知器 MLP（1986）
    ↓
深度神經網路 DNN（2006+）
    ↓
卷積神經網路 CNN / 循環神經網路 RNN
    ↓
Transformer / GPT 等現代架構
```

### 核心概念的延續

雖然現代深度學習模型極其複雜，但它們都保留了感知器的核心概念：

- ✅ **權重與偏差

---

**參考資料：**
- [The Smallest Brain You Can Build: A Perceptron in Python](https://ranpara.net/posts/perceptron-explained-from-scratch/)
