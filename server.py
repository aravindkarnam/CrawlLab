from flask import Flask, render_template_string, redirect, request, Response, send_from_directory
import random
import time
import os

app = Flask(__name__)

# Configuration
MAX_DEPTH = 50  # Maximum number of nested pages
RATE_LIMIT_TIME = 0  # Tracks the last access time for rate limiting
RATE_LIMIT_DELAY = 2  # 2 seconds delay for rate-limited pages

# Path to serve the robots.txt file
STATIC_FOLDER = 'static'

# Helper function to generate random links
def generate_page_links(current_depth, max_depth, base_url):
    if current_depth >= max_depth:
        return []
    
    # Create a mix of allowed and disallowed links based on robots.txt rules
    allowed_links = [f"{base_url}/public/page/{current_depth + 1}" for _ in range(2)]  # Allowed links
    disallowed_links = [f"{base_url}/private/page/{current_depth + 1}",  # Blocked by robots.txt
                        f"{base_url}/admin/page/{current_depth + 1}",    # Blocked by robots.txt
                        f"{base_url}/hidden/page/{current_depth + 1}"]  # Blocked by robots.txt
    
    # Shuffle the links to simulate real-world scenarios
    return random.sample(allowed_links + disallowed_links, len(allowed_links + disallowed_links))

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

@app.route('/public/page/<int:depth>')
def public_page(depth):
    """
    Public page that is allowed by robots.txt.
    """
    base_url = request.host_url.rstrip('/')
    links = generate_page_links(depth, MAX_DEPTH, base_url)
    return render_template_string(generate_html_content(depth, links))

@app.route('/private/page/<int:depth>')
def private_page(depth):
    """
    Private page that is disallowed by robots.txt.
    """
    base_url = request.host_url.rstrip('/')
    links = generate_page_links(depth, MAX_DEPTH, base_url)
    return render_template_string(generate_html_content(depth, links))

@app.route('/admin/page/<int:depth>')
def admin_page(depth):
    """
    Admin page that is disallowed by robots.txt.
    """
    base_url = request.host_url.rstrip('/')
    links = generate_page_links(depth, MAX_DEPTH, base_url)
    return render_template_string(generate_html_content(depth, links))

@app.route('/hidden/page/<int:depth>')
def hidden_page(depth):
    """
    Hidden page that is disallowed by robots.txt.
    """
    base_url = request.host_url.rstrip('/')
    links = generate_page_links(depth, MAX_DEPTH, base_url)
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

@app.route('/robots.txt')
def robots_txt():
    """
    Serve the robots.txt file.
    """
    return send_from_directory(STATIC_FOLDER, 'robots.txt')

if __name__ == '__main__':
    # Ensure the static directory exists
    if not os.path.exists(STATIC_FOLDER):
        os.makedirs(STATIC_FOLDER)
    
    # Run the Flask app
    app.run(debug=True)
