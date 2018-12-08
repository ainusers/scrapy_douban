from scrapy import cmdline

# 运行scrapy crawl douban_spider
cmdline.execute('scrapy crawl douban_spider'.split())

# 文件导出csv
# cmdline.execute('scrapy crawl douban_spider -o data.csv'.split())
