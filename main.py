import requests
from bs4 import BeautifulSoup
import time


def get_all_neocities_sites():
    """Traverse the Neocities most followed page and collect all the links to the Neocities sites."""
    all_neocities_sites = []
    page_count = 1
    initial_page_url = (
        f"https://neocities.org/browse?sort_by=followers&tag=&page={page_count}"
    )
    next_page_url = initial_page_url
    while page_count <= 100:  # 100 sites per page, 10,000 sites total
        response = requests.get(next_page_url)

        soup = BeautifulSoup(response.content, "html.parser")

        # Collect the link which is listed in the HTML element: <div class="title"> <a href="https://username.neocities.org"> </a> </div>
        links = soup.find_all("div", class_="title")
        for link in links:
            neocities_site = link.find("a")["href"]
            all_neocities_sites.append(link_formatter(neocities_site))

        # If there are no more links, then break the loop
        if links == []:
            break

        print(
            f"Scraped {len(all_neocities_sites)} neocities sites on url {next_page_url}"
        )

        # Try to go to next page
        page_count += 1
        next_page_url = (
            f"https://neocities.org/browse?sort_by=followers&tag=&page={page_count}"
        )

    return all_neocities_sites


def save_all_neocities_sites_to_txt(all_neocities_sites: list):
    with open("all_neocities_sites.txt", "w", encoding="utf-8") as file:
        for site in all_neocities_sites:
            file.write(site + "\n")


def link_formatter(href):
    """Format the href to only show the root domain. (ex. https://username.neocities.org/ -> username.neocities.org)"""
    if href.startswith("http://"):
        href = href[7:]
    if href.startswith("https://"):
        href = href[8:]
    if href.startswith("www."):
        href = href[4:]
    if "/" in href:
        href = href.split("/")[0]
    return href


def process_link(link, site, site_mentions):
    """Check the link and add it to the site_mentions dictionary if it meets the criteria."""
    if link.has_attr("href"):
        # Check if link is not the root site and is not neocities.org and is not already in this site key and is not a relative link
        if (
            (site not in link["href"])
            and ("://neocities.org" not in link["href"])
            and (
                link_formatter(link["href"])
                not in site_mentions[site]["referred_sites"]
            )
            and (link["href"].startswith("http") or link["href"].startswith("https"))
        ):
            referral = link_formatter(link["href"])

            # Add the referred site to the dictionary
            site_mentions[site]["referred_sites"].append(referral)


def search_for_site_mentions():
    """Search for site mentions within each site. This function will return a dictionary with the root site and referred sites."""

    # Create a dictionary to store the root site and referred sites
    site_mentions = {}

    count = 1
    with open("all_neocities_sites.txt", "r") as file:
        for line in file:
            site = line.strip()
            try:
                response = requests.get("https://" + site)
                response.raise_for_status()  # Raise an exception for HTTP errors
                soup = BeautifulSoup(response.content, "html.parser")
            except Exception:
                continue  # Skip the iteration if any errors are encountered

            # Initialize the current site into a dictionary with fields: site, referred_sites[].
            # We will add referred sites to the list. This is to make it easier to create a graph and show the relationship between the sites.
            site_mentions[site] = {"referred_sites": []}

            print("#" + str(count) + " " + site)
            count += 1

            links = soup.find_all("a")
            for link in links:
                process_link(link, site, site_mentions)

            # Now check if the neocities site has a /links page. If it does, then scrape the page for more referrals.
            try:
                response = requests.get("https://" + site + "/links")
                response.raise_for_status()  # Raise an exception for HTTP errors
                soup = BeautifulSoup(response.content, "html.parser")
            except Exception:
                continue  # Skip the iteration if any errors are encountered

            links = soup.find_all("a")
            for link in links:
                process_link(link, site, site_mentions)

            # If no links are found, then remove the site from the dictionary
            if site_mentions[site]["referred_sites"] == []:
                del site_mentions[site]

    return site_mentions


# Write the dictionary to a csv file. Keep the root site and referred sites in the same row.
def save_site_mentions_to_csv(site_mentions: dict):
    with open("site_mentions.csv", "w", encoding="utf-8") as file:
        for site, referrals in site_mentions.items():
            file.write(site + ",")
            for referral in referrals["referred_sites"]:
                file.write(referral + ",")
            file.write("\n")


# Step 1: Get all neocities sites

# all_neocities_sites = get_all_neocities_sites()
# save_all_neocities_sites_to_txt(all_neocities_sites)

# Step 2: Search for site mentions within each site

site_mentions = search_for_site_mentions()
save_site_mentions_to_csv(site_mentions)

# Now we have a list of neocities sites and their referrals. We can now create a graph of the sites.
