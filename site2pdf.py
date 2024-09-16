#!/usr/bin/env python3
"""
Script to generate a PDF by scraping content from a website.

Author: Rafael Borja (https://github.com/rafaelborja/)
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import logging
import argparse
from xhtml2pdf import pisa

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a PDF by scraping content from a website.')
    parser.add_argument('--url', required=True, help='URL of the table of contents page')
    parser.add_argument('--index_id', required=True, help='ID of the element containing links to content')
    parser.add_argument('--content_class', required=True, help='Class of the content to include in the PDF')
    parser.add_argument('--filename', required=True, help='Name of the output PDF file')
    parser.add_argument('--log-level', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    args = parser.parse_args()

    # Configure logging
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {args.log_level}')
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

    # Base URL
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(args.url))

    # Initialize a set to keep track of visited URLs to avoid duplicates
    visited_urls = set()

    # Initialize a list to keep track of content
    html_contents = []

    def fetch_and_parse(url):
        """
        Fetches the content of the URL and returns a BeautifulSoup object.
        """
        logging.debug(f'Fetching {url}')
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(f'Successfully fetched {url}')
        return BeautifulSoup(response.content, 'html.parser')

    def is_valid_link(href):
        """
        Checks if the href is a valid link (not an anchor link).
        """
        return href and not href.startswith('#') and not href.startswith('mailto:')

    def process_links(container, current_url):
        """
        Processes the links inside the given container element.
        """
        # Find all 'a' tags within this element
        link_elements = container.find_all('a', href=True)
        logging.debug(f'Found {len(link_elements)} links in the container')

        for link in link_elements:
            href = link.get('href')
            if is_valid_link(href):
                # Construct full URL
                full_url = urljoin(current_url, href)
                # Ensure we stay within the base domain
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    logging.debug(f'Found link to {full_url} in {current_url}')
                    process_page(full_url)
                else:
                    logging.debug(f'Skipping external link {full_url}')
            else:
                logging.debug(f'Ignoring invalid link {href}')

    def process_page(url):
        """
        Processes a page: fetches content, extracts main content.
        """
        if url in visited_urls:
            logging.debug(f'Already visited {url}')
            return
        visited_urls.add(url)
        logging.info(f'Processing {url}')
        try:
            soup = fetch_and_parse(url)
        except Exception as e:
            logging.error(f'Failed to fetch {url}: {e}')
            return

        # Extract main content
        main_content = soup.find('div', class_=args.content_class)
        if main_content:
            # Fix relative links for images and other resources
            for tag in main_content.find_all(['img', 'a', 'link', 'script']):
                for attr in ['src', 'href']:
                    if tag.has_attr(attr):
                        old_value = tag[attr]
                        tag[attr] = urljoin(url, tag[attr])
                        logging.debug(f'Updated {attr} from {old_value} to {tag[attr]} in tag {tag}')
            html_contents.append(str(main_content))
            logging.debug(f'Added content from {url}')
        else:
            logging.warning(f'No content with class "{args.content_class}" found at {url}')

    # Start processing from the start URL
    logging.info(f'Starting processing from {args.url}')
    try:
        soup = fetch_and_parse(args.url)
    except Exception as e:
        logging.error(f'Failed to fetch start URL {args.url}: {e}')
        exit(1)

    # Include the content from the start page first
    main_content = soup.find('div', class_=args.content_class)
    if main_content:
        # Fix relative links for images and other resources
        for tag in main_content.find_all(['img', 'a', 'link', 'script']):
            for attr in ['src', 'href']:
                if tag.has_attr(attr):
                    old_value = tag[attr]
                    tag[attr] = urljoin(args.url, tag[attr])
                    logging.debug(f'Updated {attr} from {old_value} to {tag[attr]} in tag {tag}')
        html_contents.append(str(main_content))
        logging.debug(f'Added content from start URL')
    else:
        logging.warning(f'No content with class "{args.content_class}" found at start URL {args.url}')

    # Now process the links inside the specified element
    container = soup.find(id=args.index_id)
    if not container:
        logging.error(f"No element found with id '{args.index_id}' on {args.url}")
        exit(1)

    process_links(container, args.url)

    # Combine all HTML content into a single HTML string
    logging.info('Combining content into a single HTML document')
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Combined Document</title>
        <style>
            /* Add basic styling to improve PDF appearance */
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2, h3, h4, h5, h6 {{ color: #2c3e50; }}
            p {{ font-size: 14px; line-height: 1.6; }}
            pre {{ background-color: #f5f5f5; padding: 10px; overflow-x: auto; }}
            code {{ background-color: #f9f9f9; padding: 2px 4px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    '''.format(content='\n'.join(html_contents))

    # Convert the combined HTML to PDF using xhtml2pdf
    logging.info(f'Converting combined HTML to {args.filename}')
    try:
        with open('combined.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        with open('combined.html', 'r', encoding='utf-8') as f:
            source_html = f.read()
        with open(args.filename, 'wb') as output_file:
            pisa_status = pisa.CreatePDF(
                src=source_html,
                dest=output_file,
                encoding='utf-8',
                link_callback=lambda uri, rel: urljoin(base_url, uri)
            )
        if pisa_status.err:
            logging.error(f'Failed to generate PDF: {pisa_status.err}')
        else:
            logging.info(f'Successfully generated {args.filename}')
    except Exception as e:
        logging.error(f'Exception occurred during PDF generation: {e}')
    finally:
        # Clean up the temporary HTML file
        try:
            os.remove('combined.html')
            logging.debug(f'Removed temporary file combined.html')
        except Exception as e:
            logging.warning(f'Failed to remove temporary file combined.html: {e}')

if __name__ == '__main__':
    main()
