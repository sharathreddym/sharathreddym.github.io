#!/usr/bin/env python3
"""
Medium Stories Sync Script
Reads embed codes from stories.txt and updates index.html
"""

import re
import sys
from datetime import datetime

def read_stories_from_file(filename='stories.txt'):
    """Read iframe embed codes or URLs from stories.txt"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Filter out comments and empty lines
        stories = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                stories.append(line)

        return stories
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        sys.exit(1)

def generate_stories_html(stories):
    """Generate HTML for Medium stories carousel"""
    if not stories:
        return """      <div class="medium-stories-container">
        <p style="text-align: center; color: var(--text-muted);">No stories available yet. Add Medium story embed codes to stories.txt</p>
      </div>"""

    html_parts = ['      <div class="medium-stories-container">']
    html_parts.append('        <div class="medium-carousel-wrapper">')
    html_parts.append('          <div class="carousel-arrow" id="prevStory" onclick="navigateStoriesCarousel(-1)">‹</div>')
    html_parts.append('          <div class="medium-stories-grid">')
    html_parts.append('            <div class="medium-stories-track" id="storiesTrack">')

    for story in stories:
        html_parts.append(f"""              <div class="medium-story-wrapper">
                {story}
              </div>""")

    html_parts.append('            </div>')
    html_parts.append('          </div>')
    html_parts.append('          <div class="carousel-arrow" id="nextStory" onclick="navigateStoriesCarousel(1)">›</div>')
    html_parts.append('        </div>')
    html_parts.append(f'        <div class="carousel-counter" id="storiesCarouselCounter">1 / {len(stories)}</div>')
    html_parts.append('      </div>')

    return '\n'.join(html_parts)

def update_index_html(stories_html, filename='index.html'):
    """Update the Medium Stories section in index.html"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Define markers for the Medium stories section
        start_marker = '    <!-- Medium Stories Section -->\n    <section id="stories" class="fade-in">\n      <h2 class="section-title">Medium Stories Collection</h2>\n'
        end_marker = '    </section>\n\n    <!-- Projects Section -->'

        # Find the section
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print("Error: Medium Stories section not found in index.html!")
            sys.exit(1)

        # Find the end of the section
        section_start = start_idx + len(start_marker)
        end_idx = content.find(end_marker, section_start)

        if end_idx == -1:
            print("Error: Could not find end of Medium Stories section!")
            sys.exit(1)

        # Replace the section content
        new_content = (
            content[:section_start] +
            stories_html + '\n' +
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Medium stories sync...")

    # Read stories from stories.txt
    stories = read_stories_from_file()
    print(f"Found {len(stories)} story/stories in stories.txt")

    # Generate HTML
    stories_html = generate_stories_html(stories)

    # Update index.html
    if update_index_html(stories_html):
        print("Successfully updated index.html!")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sync completed successfully!")
    else:
        print("Failed to update index.html")
        sys.exit(1)

if __name__ == '__main__':
    main()
