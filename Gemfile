source "https://rubygems.org"

# Jekyll 核心
gem "jekyll", "~> 4.3"

# 本地開發用
gem "webrick", "~> 1.8"

# Jekyll 插件
group :jekyll_plugins do
  gem "jekyll-remote-theme"
  gem "jekyll-sitemap"
  gem "jekyll-feed"
  gem "jekyll-include-cache"
  gem "jekyll-paginate"
  gem "jekyll-seo-tag"
  gem "jekyll-gist"
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
