# Crawler Testing Server
This project provides a local server to simulate various real-world edge cases for testing web crawlers or scrapers. It allows you to evaluate how your crawler handles slow pages, redirects, large content, error pages (404/503), duplicate links, and rate-limiting scenarios.

## Features
- Slow-Loading Pages: Simulate pages that introduce delays between 2 to 5 seconds.
- Infinite Redirect Loops: Pages that redirect to themselves, creating a loop.
- Large Pages: Pages containing large amounts of content (up to 1 MB).
- 404 Not Found Pages: Simulate broken links returning a 404 error.
- 503 Service Unavailable Pages: Simulate temporary server issues returning a 503 error.
- Duplicate Links: Pages that contain multiple links pointing to the same URL.
- Rate-Limited Pages: Simulate rate-limited access to specific pages.
- Nested Pages: Crawl through a sequence of pages with increasing depth (up to 50 levels).

## Prerequisites
Python 3.7+
Flask 3.0.0

## Installation
1. Clone the repository:

```bash
git clone <your-repository-url>
cd crawler-testing-server
```

2. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

#### Running the Server
To start the server, simply run:

```bash
python server.py
```
The server will be accessible at http://127.0.0.1:5000/.

## Endpoints

1. Home Page (/)

- This is the entry point for the crawler.
- Provides a link to the first page (/page/1).

2. Page at Depth (/page/<depth>)

- Simulates pages at increasing depth levels. Each page contains 3 random links and one of the following edge cases:
- Slow-loading pages
- Large content pages
- Pages returning 404 or 503 errors
- Infinite redirect loops
- Duplicate links
- Rate-limited pages
- Regular pages with no issues

3. Rate-Limited Page (/rate_limit)

- This endpoint specifically simulates rate-limited behavior, returning a "429 Too Many Requests" status if accessed too frequently.

### Edge Case Simulation
Each page at /page/<depth> is designed to simulate one of several predefined edge cases randomly:

- Slow Pages: Introduces a delay before the page loads.
- Large Pages: Returns a page with a large content body (1 MB).
- 404 Pages: Returns a 404 Not Found status.
- 503 Pages: Returns a 503 Service Unavailable status.
- Infinite Redirects: The page redirects to itself.
- Duplicate Links: Returns multiple links pointing to the same URL.
- Rate-Limited Pages: Throttles access to simulate rate limiting (returns a 429 status).

## Customizing the Server
You can adjust the server's behavior in the server.py file by changing the following parameters:

- MAX_DEPTH: Defines how many levels deep the pages can go. The default is set to 50.
- RATE_LIMIT_DELAY: The delay (in seconds) for rate-limited pages. The default is set to 2 seconds.
- Edge Case Frequency: Modify the problem_type selection in the page function to control the frequency of each edge case.

Example Workflow
1. Start the server:

```bash
python server.py
```
2. Point your web scraper or browser to http://127.0.0.1:5000/ to begin crawling.

3. Monitor how the crawler handles various scenarios like slow pages, redirects, large content, error pages, and rate-limiting.


