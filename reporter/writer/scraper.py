import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    """
    Scrapes the title, subtitle, and body text of an opinion editorial from the given URL.

    Parameters:
        url (str): The URL of the opinion editorial to scrape.

    Returns:
        dict: A dictionary containing the title, subtitle, and article body text.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title_tag = soup.find('h1', class_='Title')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # Extract the subtitle
        subtitle_tag = soup.find('h3', class_='subtitle')
        subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else "No Subtitle Found"

        # Extract the main article body
        article_container = soup.find('div', class_='post-content')
        if article_container:
            paragraphs = article_container.find_all('p')
            article_text = '\n\n'.join([para.get_text(strip=True) for para in paragraphs])
        else:
            article_text = "Article body not found."

        return {
            "title": title,
            "subtitle": subtitle,
            "body": article_text
        }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the article: {e}")
        return None


def print_any_text(url):
    """
    Prints any text found on the page.

    Parameters:
        url (str): The URL to check.

    Returns:
        None
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the page
        page_text = soup.get_text(strip=True)

        # Print the text if found
        if page_text:
            print("Text found on the page:\n")
            print(page_text)
        else:
            print("No text found on the page.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")

if __name__ == "__main__":
    url = "https://reason.org/commentary/states-can-legalize-mdma-for-pharmaceutical-use-even-if-the-federal-government-does-not/"
    article_data = scrape_article(url)
    any_text = print_any_text(url)

    if any_text:
        print("DEBUG: any text executed", any_text)

    if article_data:
        print("Title:\n", article_data['title'])
        print("\nSubtitle:\n", article_data['subtitle'])
        print("\nArticle Body:\n", article_data['body'])

