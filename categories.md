---
layout: page
title: 文章分類
permalink: /categories/
---

<div class="post-content">

## 📂 文章分類

透過分類快速找到你感興趣的內容：

{% assign categories = site.categories | sort %}
{% for category in categories %}
  <div class="post-card">
    <h3>{{ category[0] | capitalize }}</h3>
    <p>共 {{ category[1].size }} 篇文章</p>
    
    <ul style="list-style: none; padding: 0;">
      {% for post in category[1] limit:5 %}
        <li style="margin-bottom: 0.5rem;">
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          <small style="color: #7f8c8d; margin-left: 1rem;">{{ post.date | date: "%Y-%m-%d" }}</small>
        </li>
      {% endfor %}
      {% if category[1].size > 5 %}
        <li><em>還有 {{ category[1].size | minus: 5 }} 篇文章...</em></li>
      {% endif %}
    </ul>
  </div>
{% endfor %}

{% if site.categories.size == 0 %}
  <div class="post-card">
    <h3>🚀 即將推出</h3>
    <p>文章分類功能已準備就緒，等待精彩內容的加入！</p>
    <p>預計分類包括：</p>
    <ul>
      <li>🤖 <strong>AI工具</strong> - 人工智慧工具評測與應用</li>
      <li>💡 <strong>創意思維</strong> - 創新方法論與實踐</li>
      <li>🚀 <strong>創業洞察</strong> - 商業趨勢與創業經驗</li>
      <li>🔧 <strong>生產力工具</strong> - 效率提升與工具推薦</li>
      <li>📚 <strong>學習筆記</strong> - 知識整理與心得分享</li>
    </ul>
  </div>
{% endif %}

</div> 