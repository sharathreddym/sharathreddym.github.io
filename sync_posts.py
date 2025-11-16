#!/usr/bin/env python3
"""
LinkedIn Posts Sync Script
Reads embed codes from posts.txt and updates index.html
"""

import re
import sys
from datetime import datetime

def read_posts_from_file(filename='posts.txt'):
    """Read iframe embed codes from posts.txt"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Filter out comments and empty lines
        posts = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                posts.append(line)

        return posts
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        sys.exit(1)

def generate_posts_html(posts):
    """Generate HTML for LinkedIn posts carousel"""
    if not posts:
        return """      <div class="linkedin-posts-container">
        <p style="text-align: center; color: var(--text-muted);">No posts available yet. Add embed codes to posts.txt</p>
      </div>"""

    html_parts = ['      <div class="linkedin-posts-container">']
    html_parts.append('        <div class="linkedin-carousel-wrapper">')
    html_parts.append('          <div class="carousel-arrow" id="prevPost" onclick="navigateCarousel(-1)">‹</div>')
    html_parts.append('          <div class="linkedin-posts-grid">')
    html_parts.append('            <div class="linkedin-posts-track" id="postsTrack">')

    for post in posts:
        html_parts.append(f"""              <div class="linkedin-post-wrapper">
                {post}
              </div>""")

    html_parts.append('            </div>')
    html_parts.append('          </div>')
    html_parts.append('          <div class="carousel-arrow" id="nextPost" onclick="navigateCarousel(1)">›</div>')
    html_parts.append('        </div>')
    html_parts.append(f'        <div class="carousel-counter" id="carouselCounter">1 / {len(posts)}</div>')
    html_parts.append('      </div>')

    return '\n'.join(html_parts)

def update_index_html(posts_html, filename='index.html'):
    """Update the LinkedIn Posts section in index.html"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Define markers for the LinkedIn posts section
        start_marker = '    <!-- LinkedIn Posts Section -->\n    <section id="posts" class="fade-in">\n      <h2 class="section-title">LinkedIn Posts Collection</h2>\n'
        end_marker = '    </section>\n\n    <!-- Projects Section -->'

        # Find the section
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print("Error: LinkedIn Posts section not found in index.html!")
            sys.exit(1)

        # Find the end of the section
        section_start = start_idx + len(start_marker)
        end_idx = content.find(end_marker, section_start)

        if end_idx == -1:
            print("Error: Could not find end of LinkedIn Posts section!")
            sys.exit(1)

        # Replace the section content
        new_content = (
            content[:section_start] +
            posts_html + '\n' +
            content[end_idx:]
        )

        # Write back to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating index.html: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting LinkedIn posts sync...")

    # Read posts from posts.txt
    posts = read_posts_from_file()
    print(f"Found {len(posts)} post(s) in posts.txt")

    # Generate HTML
    posts_html = generate_posts_html(posts)

    # Update index.html
    if update_index_html(posts_html):
        print("Successfully updated index.html!")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sync completed successfully!")
    else:
        print("Failed to update index.html")
        sys.exit(1)

if __name__ == '__main__':
    main()
