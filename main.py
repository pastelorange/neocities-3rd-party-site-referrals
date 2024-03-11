import requests
from bs4 import BeautifulSoup

initial_page_url = "https://neocities.org/browse?sort_by=newest&tag="
all_neocities_sites = []
neocities_site_referrals = []

# TODO Account for custom domain. Scan for the neocities user's username.

# Loop traverse each pagination. There is a next button with the HTML element <a class="next_page">.
# Collect the links to each site which are in the format "https://username.neocities.org".
# If there is no next button, then the loop should stop.
# The initial_page_url is the first page of the pagination.
next_page_url = initial_page_url
while True:
    response = requests.get(next_page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    sites = soup.find_all(
        "a",
        href=lambda href: href
        and href.startswith("https://")
        and ".neocities.org" in href,
    )
    all_neocities_sites.extend(sites)  # Add to list

    # Try to go to next page
    next_button = soup.find("a", class_="next_page")
    if not next_button:
        break
    next_page_url = next_button["href"]


# Now enter each link in links and scrape the content of each site.
# We are looking for links to other neocities sites in the HTML content of each site, so make sure to exclude the current site from the list of referrals.
# Also, make sure to exclude any links that are not to neocities sites.
# You can use the requests library to send a GET request to each site and then use BeautifulSoup to parse the HTML content.
# You can use the find_all method to find all <a> tags in the HTML content and then check if the href attribute contains "neocities.org".
