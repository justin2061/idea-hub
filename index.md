---
layout: default # Assumes a 'default' layout from your theme (e.g., minima)
title: Welcome
---

# Welcome to My Idea Hub!

This is a place to capture and explore new ideas.

## Latest Ideas

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a> - {{ post.date | date: "%Y-%m-%d" }}
    </li>
  {% endfor %}
</ul>

Check out the [About page](about.html) to learn more.
