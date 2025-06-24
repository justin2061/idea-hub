source "https://rubygems.org"

# 使用 GitHub Pages gem，這會自動包含正確的 Jekyll 版本
gem "github-pages", "~> 232", group: :jekyll_plugins

# 本地開發用的額外 gems
gem "webrick", "~> 1.8"

# Windows 和 JRuby 不包含 zoneinfo 文件，所以將 tzinfo-data gem 打包
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Windows 性能提升
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# JRuby 的 HTTP 解析器
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby] 