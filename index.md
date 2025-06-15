---
layout: home
title: 首頁
---

<div class="hero-section">
  <h1>點子實驗室</h1>
  <p class="hero-description">探索 AI、創意、創業與未來工具的專業內容平台<br>每天分享新穎觀點與深度思考</p>
</div>

<div class="wrapper">
  <!-- 最新文章區域 -->
  <section class="latest-posts">
    <h2>🚀 最新文章</h2>
    
    {% if site.posts.size > 0 %}
      {% for post in site.posts limit:6 %}
        <article class="post-card">
          <h3 class="post-title">
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          </h3>
          
          <div class="post-meta">
            <span class="post-date">📅 {{ post.date | date: "%Y年%m月%d日" }}</span>
            {% if post.author %}
              <span class="post-author">👤 {{ post.author }}</span>
            {% endif %}
            {% if post.categories.size > 0 %}
              <span class="post-category">📂 {{ post.categories | first }}</span>
            {% endif %}
          </div>
          
          {% if post.excerpt %}
            <div class="post-excerpt">
              {{ post.excerpt | strip_html | truncatewords: 30 }}
            </div>
          {% endif %}
          
          <a href="{{ post.url | relative_url }}" class="read-more">閱讀全文 →</a>
        </article>
      {% endfor %}
    {% else %}
      <div class="post-card">
        <h3>歡迎來到點子實驗室！</h3>
        <p>這裡即將分享關於 AI、創意、創業與未來工具的精彩內容。敬請期待第一篇文章的發布！</p>
      </div>
    {% endif %}
  </section>

  <!-- 特色內容區域 -->
  <section class="featured-content">
    <h2>🎯 熱門主題</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 3rem;">
      
      <div class="post-card">
        <h3>🤖 AI 工具探索</h3>
        <p>深入研究最新的 AI 工具與應用，分享實用的使用技巧與心得。</p>
      </div>
      
      <div class="post-card">
        <h3>💡 創意思維</h3>
        <p>探討創意發想的方法論，分享靈感來源與創意實踐的經驗。</p>
      </div>
      
      <div class="post-card">
        <h3>🚀 創業洞察</h3>
        <p>分析創業趨勢，分享創業路上的思考與實戰經驗。</p>
      </div>
      
    </div>
  </section>

  <!-- 關於作者 -->
  <section class="about-author">
    <div class="post-card">
      <h2>👋 關於作者</h2>
      <p>我是 Justin Lee，一個對 AI、創意與創業充滿熱情的探索者。在這個快速變化的時代，我致力於發現和分享那些能夠啟發思考、推動創新的想法與工具。</p>
      <p>這個網站是我記錄思考軌跡、分享學習心得的地方。希望這些內容能為你帶來新的視角與靈感。</p>
      <a href="{{ '/about/' | relative_url }}" class="read-more">了解更多 →</a>
    </div>
  </section>

</div>
