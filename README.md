# Bookscraper 🕷🕸
## Get started with FreeCode Camp Python Scrapy Course
### ⭐️Sections⭐️
📍 Part 1 - Scrapy & Course Introduction <br>
📍 Part 2 - Setup Virtual Env & Scrapy<br>
📍 Part 3 - Creating a Scrapy Project<br>
📍 Part 4 - Build your First Scrapy Spider<br>
📍 Part 5 - Build Discovery & Extraction Spider<br>
📍 Part 6 - Cleaning Data with Item Pipelines<br>
📍 Part 7 - Saving Data to Files & Databases<br>
📍 Part 8 - Fake User-Agents & Browser Headers<br>
📍 Part 9 - Rotating Proxies & Proxy APIs<br>
📍 Part 10 - Run Spiders in Cloud with Scrapyd<br>
📍 Part 11 - Run Spiders in Cloud with ScrapeOps<br>
📍 Part 12 - Run Spiders in Cloud with Scrapy Cloud<br>
📍 Part 13 - Conclusion & Next Steps

### ⭐️Tech Stack⭐️
- Python 3.11
- Scrapy
- Scrapy Shell
- Supabase
- itemadapter
- [userAgent](https://useragentstring.com/)
- scrapeOps: create Fake User-Agent API 

### ⭐️Course Resources⭐️
- [Scrapy Docs](https://docs.scrapy.org/en/latest/)
- [Course Guide ](https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/)
- Course Cover:
  - Creating your first Scrapy spider
  - Crawling through websites & scraping data from each page
  - Cleaning data with Items & Item Pipelines
  - Saving data to CSV files, Postgres databases
  - Using fake user-agents & headers to avoid getting blocked
  - Using proxies to scale up your web scraping without getting banned
  - Deploying your scraper to the supabase cloud & scheduling it to run periodically
  
### ⭐️Learning Notes⭐️
1. next page until no more pages
```python
next_page = response.css("li.next a::attr(href)").get()

if next_page is not None:
   if 'catalogue/' in next_page:
         next_page_url = 'https://books.toscrape.com/' + next_page
   else:
         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
   yield response.follow(next_page_url, callback=self.parse)
```

2. Understand Xpath

```python
response.xpath("//url[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
```

  If there is no class 
```python
   response.xpath("//div[@class='product_description']/following-sibling::p/text()").get()
```

3. Scrapy attributes
```bash
   response.css('p.star-rating').attrib['class']
   out: 'star-rating Three'
```