from flask import Flask, render_template_string, redirect, request, Response
import random
import time

app = Flask(__name__)

# Configuration
MAX_DEPTH = 50  # Maximum number of nested pages
RATE_LIMIT_TIME = 0  # Tracks the last access time for rate limiting
RATE_LIMIT_DELAY = 2  # 2 seconds delay for rate-limited pages

# Helper function to generate random links
def generate_page_links(current_depth, max_depth, base_url):
    if current_depth >= max_depth:
        return []
    return [f"{base_url}/page/{current_depth + 1}" for _ in range(3)]  # Three links per page

# Helper function to generate random HTML content
def generate_html_content(depth, links):
    divs = ''.join(f'<div>Random content for depth {depth}: {random.randint(1, 100)}</div>' for _ in range(10))
    links_html = ''.join(f'<a href="{link}">Go to {link}</a><br>' for link in links)
    return f'''
    <html>
        <head><title>Page at Depth {depth}</title></head>
        <body>
            <h1>Welcome to Page at Depth {depth}</h1>
            {divs}
            <h2>Links to Next Pages:</h2>
            {links_html}
        </body>
    </html>
    '''

@app.route('/')
def home():
    """
    Entry point for the crawler.
    """
    base_url = request.host_url.rstrip('/')
    initial_links = generate_page_links(0, MAX_DEPTH, base_url)
    return render_template_string(generate_html_content(0, initial_links))

@app.route('/page/<int:depth>')
def page(depth):
    """
    Generate a page at a specific depth level.
    This page will handle various edge cases.
    """
    base_url = request.host_url.rstrip('/')
    links = generate_page_links(depth, MAX_DEPTH, base_url)
    problem_type = random.choice(['slow', 'large', '404', '503', 'redirect', 'duplicate', 'normal', 'rate_limit'])

    # Handle various edge cases
    if problem_type == 'slow':
        time.sleep(random.uniform(2, 5))  # Simulate slow pages
    elif problem_type == 'large':
        # Returning a large response (this can also be an HTML page)
        large_content = generate_html_content(depth, links) + "<p>" + "A" * 1000000 + "</p>"  # 1 MB of 'A'
        return Response(large_content, status=200, content_type='text/html')
    elif problem_type == '404':
        return Response("404 Not Found", status=404)
    elif problem_type == '503':
        return Response("503 Service Unavailable", status=503)
    elif problem_type == 'redirect':
        return redirect(f"{base_url}/page/{depth}")  # Infinite redirect
    elif problem_type == 'duplicate':
        links.append(links[0])  # Add duplicate links
    elif problem_type == 'rate_limit':
        global RATE_LIMIT_TIME
        if time.time() - RATE_LIMIT_TIME < RATE_LIMIT_DELAY:
            return Response("429 Too Many Requests", status=429)
        RATE_LIMIT_TIME = time.time()

    return render_template_string(generate_html_content(depth, links))

@app.route('/rate_limit')
def rate_limited_page():
    """
    A specific endpoint to simulate rate-limited access.
    """
    global RATE_LIMIT_TIME
    if time.time() - RATE_LIMIT_TIME < RATE_LIMIT_DELAY:
        return Response("429 Too Many Requests", status=429)
    RATE_LIMIT_TIME = time.time()
    return render_template_string('<html><body><h1>Rate Limited Page</h1><p>This page is rate-limited.</p></body></html>')

if __name__ == '__main__':
    app.run(debug=True)
