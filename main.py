import requests
from bs4 import BeautifulSoup

initial_page_url = "https://neocities.org/browse"

# Loop traverse each pagination. There is a next button with the HTML element <a class="next_page">
while initial_page_url:
    response = requests.get(initial_page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("div", class_="title")
    for link in links:
        a_tag = link.find("a")
        # if a_tag and "neocities.org" in a_tag["href"]:
        #     print(a_tag["href"])
    next_page = soup.find("a", class_="next_page")

print(len(links))

# # Send a GET request to the neocities.org/browse page
# response = requests.get("https://neocities.org/browse")

# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")

# # Find all links for Neocities sites which follow the format username.neocities.org
# # The <a> we are seeking is inside a <div> with the class "title"
# links = soup.find_all("div", class_="title")
# for link in links:
#     a_tag = link.find("a")
#     if a_tag and "neocities.org" in a_tag["href"]:
#         print(a_tag["href"])
