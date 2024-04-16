# Amazon Scraper

This is a web scraper built with Scrapy to extract information about wireless headphones from Amazon.in.

## Installation

1. Clone the repository:

    ```
    git clone <repository_url>
    ```

2. Install the required packages using pip:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Navigate to the project directory containing `scrapy.cfg`.
2. Run the spider using the following command:

    ```
    scrapy crawl amazon_scraper -o amazon_articles.csv
    ```

## About the Spider

### Spider Details

- **Name:** amazon_scraper
- **Allowed Domains:** www.amazon.in

### Custom Settings

- **DOWNLOADER_MIDDLEWARES:**
    - 'scrapy_amazon.middlewares.ProxyMiddleware': 350
    - 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400
- **CONCURRENT_REQUESTS:** 2
- **DOWNLOAD_DELAY:** 0.3 seconds

### Starting URLs

The spider starts by sending a request to the URL:
https://www.amazon.in/s?k=headphones+wireless&crid=WAIAFDNL3AWL&sprefix=head%2Caps%2C316&ref=nb_sb_ss_ts-doa-p_2_4

### Parsing

The spider parses each page for wireless headphone products and extracts the following information for each product:

- Product Title
- Product Description
- Product Image URL
- Product Price

### Pagination

The spider handles pagination to scrape through multiple pages of search results.

## Additional Information

- **User-Agent:** Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
- **Normalization Function:** Handles cleaning and normalization of text data.

