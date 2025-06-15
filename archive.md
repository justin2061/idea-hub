---
layout: page
title: 文章歸檔
permalink: /archive/
---

<div class="post-content">

## 📅 文章歸檔

按時間順序瀏覽所有文章：

{% if site.posts.size > 0 %}
  {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
  
  {% for year in posts_by_year %}
    <div class="post-card">
      <h3>{{ year.name }} 年</h3>
      <p>共發布 {{ year.items.size }} 篇文章</p>
      
      {% assign posts_by_month = year.items | group_by_exp: "post", "post.date | date: '%m'" %}
      
      {% for month in posts_by_month %}
        <h4 style="margin-top: 2rem; margin-bottom: 1rem; color: #3498db;">
          {{ month.items.first.date | date: "%m月" }} ({{ month.items.size }} 篇)
        </h4>
        
        <ul style="list-style: none; padding: 0;">
          {% for post in month.items %}
            <li style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                  <a href="{{ post.url | relative_url }}" style="font-weight: 500; color: #2c3e50; text-decoration: none;">
                    {{ post.title }}
                  </a>
                  {% if post.excerpt %}
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem;">
                      {{ post.excerpt | strip_html | truncatewords: 15 }}
                    </p>
                  {% endif %}
                </div>
                <div style="color: #95a5a6; font-size: 0.9rem; white-space: nowrap; margin-left: 1rem;">
                  {{ post.date | date: "%m月%d日" }}
                </div>
              </div>
              
              {% if post.categories.size > 0 or post.tags.size > 0 %}
                <div style="margin-top: 0.5rem;">
                  {% for category in post.categories %}
                    <span style="background: #3498db; color: white; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem; margin-right: 0.5rem;">
                      {{ category }}
                    </span>
                  {% endfor %}
                  {% for tag in post.tags limit:3 %}
                    <span style="background: #95a5a6; color: white; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem; margin-right: 0.5rem;">
                      #{{ tag }}
                    </span>
                  {% endfor %}
                </div>
              {% endif %}
            </li>
          {% endfor %}
        </ul>
      {% endfor %}
    </div>
  {% endfor %}
  
{% else %}
  <div class="post-card">
    <h3>🚀 準備開始</h3>
    <p>文章歸檔功能已準備就緒，等待第一篇文章的發布！</p>
    <p>這裡將會按年份和月份整理所有文章，方便你回顧過往的內容。</p>
  </div>
{% endif %}

## 📊 統計資訊

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem;">
  <div style="background: #3498db; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
    <h4 style="margin: 0; color: white;">總文章數</h4>
    <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0 0 0;">{{ site.posts.size }}</p>
  </div>
  
  <div style="background: #2ecc71; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
    <h4 style="margin: 0; color: white;">分類數量</h4>
    <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0 0 0;">{{ site.categories.size }}</p>
  </div>
  
  <div style="background: #e74c3c; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
    <h4 style="margin: 0; color: white;">最新更新</h4>
    <p style="font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0 0 0;">
      {% if site.posts.size > 0 %}
        {{ site.posts.first.date | date: "%Y-%m-%d" }}
      {% else %}
        即將開始
      {% endif %}
    </p>
  </div>
</div>

</div> 