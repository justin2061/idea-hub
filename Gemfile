source "https://rubygems.org"

# 使用標準 Jekyll 而非 GitHub Pages（避免版本衝突）
gem "jekyll", "~> 4.3"

# 本地開發用的額外 gems
gem "webrick", "~> 1.8"

# Chirpy 主題
gem "jekyll-theme-chirpy", "~> 7.0", ">= 7.0.1"

# Jekyll 插件
group :jekyll_plugins do
  gem "jekyll-sitemap"
  gem "jekyll-gist"
  gem "jekyll-feed"
  gem "jekyll-include-cache"
  gem "jemoji"
  gem "jekyll-archives"
end

# Windows 和 JRuby 不包含 zoneinfo 文件，所以將 tzinfo-data gem 打包
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Windows 性能提升
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# JRuby 的 HTTP 解析器
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby] 