source "https://rubygems.org"

# Jekyll 核心
gem "jekyll", "~> 4.3"

# 本地開發用
gem "webrick", "~> 1.8"

# Chirpy 主題所需插件
group :jekyll_plugins do
  gem "jekyll-remote-theme"
  gem "jekyll-paginate"
  gem "jekyll-redirect-from"
  gem "jekyll-seo-tag"
  gem "jekyll-archives"
  gem "jekyll-sitemap"
  gem "jekyll-feed"
  gem "jekyll-include-cache"
  gem "jemoji"
end

# Windows 和 JRuby 支援
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Windows 性能提升
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# JRuby 的 HTTP 解析器
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
