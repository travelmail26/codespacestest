# import requests
# from bs4 import BeautifulSoup

# # Send a request to the webpage

# #url = "https://reason.org/testimony/colorado-could-improve-regulatory-rules-regarding-psychedelic-use/"
# response = requests.get(url)

# # Parse the webpage content with BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")

# # Find the main content container
# content_div = soup.find("div", class_="entry-content")

# all_text = content_div.get_text()
# print(all_text, "***END OF TEXT***")

# #Check if the content was found
# if content_div:
#     # Extract all paragraphs and lists within the content
#     paragraphs = content_div.find_all(['p', 'ul'])
    
#     # Print the text content of each paragraph and list
#     for tag in paragraphs:
#         print(tag.get_text())
# else:
#     print("Content not found.")

# from bs4 import BeautifulSoup
# import requests

# # Define headers with a user-agent to mimic a browser
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }

# # Fetch the page content
# response = requests.get("https://amazingribs.com/tested-recipes/beef-and-bison-recipes/home-made-pastrami-thats-close-katzs-recipe/", headers=headers)
# soup = BeautifulSoup(response.content, 'html.parser')

# # Find all <p> tags
# paragraphs = soup.find_all('p')

# # Print each paragraph
# for p in paragraphs:
#     print(p.get_text())

# from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse

# scrapfly = ScrapflyClient(key="scp-test-033670733392457884ba3d61431cd7f9")
# result: ScrapeApiResponse = scrapfly.scrape(ScrapeConfig(
#     tags=[
#     "player","project:default"
#     ],
#     format="text",
#     asp=True,
#     render_js=True,
#     url="https://amazingribs.com/tested-recipes/beef-and-bison-recipes/home-made-pastrami-thats-close-katzs-recipe/"
# ))

# print (result.content)


from bs4 import BeautifulSoup
import requests

# Define headers with a user-agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# URL of the website to scrape
url = "https://reason.org/testimony/colorado-could-improve-regulatory-rules-regarding-psychedelic-use/"  # Replace with the URL of the website you want to scrape

# Fetch the page content
response = requests.get(url, headers=headers)

# Check for successful request
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <p>, <h1>, <h2>, and <h3> tags
    paragraphs = soup.find_all('p')
    headings1 = soup.find_all('h1')
    headings2 = soup.find_all('h2')
    headings3 = soup.find_all('h3')
    contentheading = soup.find_all('content')

    content_div = soup.find('div', class_='content')

    if content_div:
        # Extract all text within the 'content' div, including nested tags
        all_text = content_div.get_text(separator='\n', strip=True)
        
        # Print the extracted text
        print("***Content Div Text***")
        print(all_text)
        print()

    # Print all <p> tags
    print("***Paragraphs***")
    for p in paragraphs:
        print(p.get_text())
        print()

    # Print all <h1> tags
    print("***Headings (h1)***")
    for h1 in headings1:
        print(h1.get_text())
        print()

    # Print all <content> tags
    print("***Content Headings***")
    for content in contentheading:
        print(content.get_text())
        print()

    # Print all <h2> tags
    print("***Headings (h2)***")
    for h2 in headings2:
        print(h2.get_text())
        print()

    # Print all <h3> tags
    print("***Headings (h3)***")
    for h3 in headings3:
        print(h3.get_text())
        print()

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
