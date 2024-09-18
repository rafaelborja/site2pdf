# Web Content to PDF Generator

**Author:** [Rafael Borja](https://github.com/rafaelborja/)

## Description

This script allows you to generate a PDF document by scraping content from a website. It fetches specified web pages, extracts the desired content, and compiles it into a single PDF file.

## Features

- **Multiple Navigation Methods:**
    - **Index-Based Navigation:** Start from a table of contents page and follow links within a specified HTML element.
    - **Next Link Navigation:** Navigate through pages by following a "next" link until no further links are found.
- **Content Extraction:**
    - Specify the HTML element class that contains the main content to extract.
- **PDF Generation:**
    - Generate a consolidated PDF file with the scraped content.
- **Customization:**
    - Customizable through command-line arguments.
- **Logging:**
    - Includes logging to monitor the scraping process.

## Prerequisites

- Python 3.x installed on your system.
- An active internet connection.

## Installation

1. **Clone the Repository or Download the Script**

   ```bash
   git clone https://github.com/rafaelborja/web-content-to-pdf.git
   ```

   Or simply download the `download_as_pdf.py` script to your local machine.

2. **Navigate to the Script Directory**

   ```bash
   cd web-content-to-pdf
   ```

3. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

    - On Unix or macOS:

      ```bash
      source venv/bin/activate
      ```

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

4. **Install Required Python Packages**

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, install the packages manually:

   ```bash
   pip install requests beautifulsoup4 xhtml2pdf
   ```

## Usage

Run the script using the command line with the required arguments.

### Command-Line Arguments

- `--url`: **(Required)** The URL of the start page.
- `--content_class`: **(Required)** The `class` attribute of the HTML element containing the content to include in the PDF.
- `--filename`: **(Required)** The name of the output PDF file.
- `--log-level`: *(Optional)* Set the logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default is `INFO`.
- **Navigation Options (Choose One):**
    - `--index_id`: The `id` attribute of the HTML element containing links to content pages.
    - `--next_page_class`: The `class` attribute of the "next" link to navigate through pages.

### Important Note

- You must provide either `--index_id` or `--next_page_class`, but not both.
- These arguments are **mutually exclusive**, and the script will exit with an error if neither is provided.

### Examples

#### **Example 1: Index-Based Navigation**

Generate a PDF by following links from a table of contents page:

```bash
python download_as_pdf.py \
--url "https://example.com/docs/index.html" \
--index_id "docs-links" \
--content_class "main-content" \
--filename "example_docs.pdf" \
--log-level INFO
```

#### **Example 2: Next Link Navigation**

Generate a PDF by navigating through pages using a "next" link:

```bash
python download_as_pdf.py \
--url "https://example.com/articles/part1.html" \
--next_page_class "next-button" \
--content_class "article-content" \
--filename "articles_series.pdf" \
--log-level INFO
```

### Explanation of Parameters

- `--url`: Starting URL for scraping.
- `--index_id`: The `id` of the HTML element that contains links to other pages.
- `--next_page_class`: The `class` of the "next" link to navigate through pages.
- `--content_class`: The `class` of the HTML elements that contain the main content to extract.
- `--filename`: The desired name for the output PDF file.
- `--log-level`: Logging verbosity level.

## Detailed Steps

1. **Check Python Version**

   Ensure you are using Python 3.x:

   ```bash
   python --version
   ```

2. **Install Dependencies**

   Install the required packages if you haven't already:

   ```bash
   pip install requests beautifulsoup4 xhtml2pdf
   ```

3. **Run the Script**

   Use the command-line arguments to specify your parameters.

    - **For Index-Based Navigation:**

      ```bash
      python download_as_pdf.py \
      --url "YOUR_URL" \
      --index_id "YOUR_INDEX_ID" \
      --content_class "YOUR_CONTENT_CLASS" \
      --filename "YOUR_FILENAME.pdf" \
      --log-level INFO
      ```

    - **For Next Link Navigation:**

      ```bash
      python download_as_pdf.py \
      --url "YOUR_START_URL" \
      --next_page_class "YOUR_NEXT_PAGE_CLASS" \
      --content_class "YOUR_CONTENT_CLASS" \
      --filename "YOUR_FILENAME.pdf" \
      --log-level INFO
      ```

   Replace placeholders with your specific values.

4. **Wait for Completion**

   The script will output logs indicating the progress. If you've set `--log-level` to `INFO` or `DEBUG`, you'll see more detailed information.

5. **Check the Output**

   Once the script finishes, you should find the PDF file with the specified name in your current directory.

## Tips

- **Adjust Logging Level**

  Use `--log-level DEBUG` to get detailed logs for troubleshooting.

- **Verify HTML Structure**

  Ensure the `index_id`, `next_page_class`, and `content_class` match the actual `id` and `class` attributes in the website's HTML.

- **Respect Website Policies**

  Make sure you have permission to scrape content from the website and that you're not violating any terms of service.

- **Virtual Environment**

  Using a virtual environment can prevent package conflicts and maintain project-specific dependencies.

## Limitations

- **JavaScript-Rendered Content**

  The script does not execute JavaScript. If the website relies on JavaScript to load content, the script may not capture it.

- **CSS Support**

  The `xhtml2pdf` library supports a subset of CSS. Complex styles may not render as expected in the PDF.

- **Percentage Values in Styles**

  Due to limitations of `xhtml2pdf`, the script removes percentage values from HTML attributes and inline styles to prevent errors during PDF generation.

## Dependencies

- [requests](https://pypi.org/project/requests/): For HTTP requests.
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/): For parsing HTML content.
- [xhtml2pdf](https://pypi.org/project/xhtml2pdf/): For converting HTML to PDF.

Install them via `pip`:

```bash
pip install requests beautifulsoup4 xhtml2pdf
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Rafael Borja**

- **GitHub**: [https://github.com/rafaelborja/](https://github.com/rafaelborja/)

Feel free to reach out for any questions or collaborations.

## Acknowledgments

- Thanks to the developers of `requests`, `beautifulsoup4`, and `xhtml2pdf` for their invaluable libraries.
- Inspired by the need to automate PDF generation from web content.
