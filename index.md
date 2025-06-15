---
layout: default
title: Welcome
---

# 👋 Welcome to My Idea Hub

這是一個收集與探索各種創意點子的網站。

## 🧠 最新點子列表

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <small>({{ post.date | date: "%Y-%m-%d" }})</small>
    </li>
  {% endfor %}
</ul>

👉 查看[關於本站](about.html)了解更多。
