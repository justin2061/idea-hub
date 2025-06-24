---
layout: home
title: 首頁
---

<div class="hero-section">
  <h1>點子實驗室</h1>
  <p class="hero-description">探索 AI、創意、創業與未來工具的專業內容平台<br>每天分享新穎觀點與深度思考</p>
</div>

## 🚀 最新文章

<div class="post-list">
  {% for post in site.posts limit:3 %}
  <article class="post-card">
    <h2 class="post-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <div class="post-meta">
      <span class="post-date">{{ post.date | date: "%Y年%m月%d日" }}</span>
      <span class="post-author">{{ post.author | default: site.author }}</span>
      {% if post.categories.size > 0 %}
        <span class="post-category">{{ post.categories.first }}</span>
      {% endif %}
    </div>
    <div class="post-excerpt">
      {{ post.excerpt | strip_html | truncatewords: 30 }}
    </div>
    <a href="{{ post.url | relative_url }}" class="read-more">閱讀全文</a>
  </article>
  {% endfor %}
</div>

## 🎯 熱門主題

<div class="features-section">
  <div class="feature-card">
    <span class="feature-icon">🤖</span>
    <h3>AI 工具探索</h3>
    <p>深入研究最新的 AI 工具與應用，分享實用的使用技巧與心得。</p>
  </div>
  
  <div class="feature-card">
    <span class="feature-icon">💡</span>
    <h3>創意思維</h3>
    <p>探討創意發想的方法論，分享靈感來源與創意實踐的經驗。</p>
  </div>
  
  <div class="feature-card">
    <span class="feature-icon">🚀</span>
    <h3>創業洞察</h3>
    <p>分析創業趨勢，分享創業路上的思考與實戰經驗。</p>
  </div>
</div>

## 📊 網站統計

<div class="stats-section">
  <div class="stat-card">
    <div>{{ site.posts.size }}</div>
    <div>篇文章</div>
  </div>
  
  <div class="stat-card">
    <div>{{ site.categories.size }}</div>
    <div>個分類</div>
  </div>
  
  <div class="stat-card">
    <div>2025</div>
    <div>年創立</div>
  </div>
</div>

## 👋 關於作者

<div class="author-section">
  <div style="display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 300px;">
      <h3 style="margin-top: 0;">Justin Lee</h3>
      <p>我是一個對 AI、創意與創業充滿熱情的探索者。在這個快速變化的時代，我致力於發現和分享那些能夠啟發思考、推動創新的想法與工具。</p>
      <p>這個網站是我記錄思考軌跡、分享學習心得的地方。希望這些內容能為你帶來新的視角與靈感。</p>
      <a href="{{ '/about/' | relative_url }}" class="btn-primary">了解更多</a>
    </div>
    <div style="text-align: center;">
      <div style="width: 120px; height: 120px; background: linear-gradient(135deg, var(--tech-blue), var(--tech-purple)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem; color: white; margin: 0 auto; box-shadow: var(--glow-shadow);">👨‍💻</div>
    </div>
  </div>
</div>

## 🔗 快速導航

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
  <a href="{{ '/categories/' | relative_url }}" class="nav-card">
    <div>📂</div>
    <h4>文章分類</h4>
    <p>按主題瀏覽所有文章</p>
  </a>
  
  <a href="{{ '/archive/' | relative_url }}" class="nav-card">
    <div>📅</div>
    <h4>文章歸檔</h4>
    <p>按時間順序查看文章</p>
  </a>
  
  <a href="{{ '/about/' | relative_url }}" class="nav-card">
    <div>ℹ️</div>
    <h4>關於本站</h4>
    <p>了解網站理念與作者</p>
  </a>
</div>

<style>
.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
</style>
