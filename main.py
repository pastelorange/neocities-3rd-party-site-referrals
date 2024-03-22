import requests
from bs4 import BeautifulSoup


# Returns only the root domain of a URL
def link_formatter(href):
    if href.startswith("http://"):
        href = href[7:]
    if href.startswith("https://"):
        href = href[8:]
    if href.startswith("www."):
        href = href[4:]
    if "/" in href:
        href = href.split("/")[0]
    return href


# Loop traverse each pagination. There is a next button with the HTML element <a class="next_page">.
# Collect the link which is listed in the HTML element: <div class="title"> <a href="https://username.neocities.org"> </a> </div>
# If there is no next button, then the loop should stop.
# The initial_page_url is the first page of the pagination.
def get_all_neocities_sites():
    all_neocities_sites = []
    initial_page_url = "https://neocities.org/browse?sort_by=newest&tag="
    next_page_url = initial_page_url
    page_count = 1
    while True:
        if page_count == 10:
            break
        response = requests.get(next_page_url)

        # Handle HTTP errors
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Collect the link which is listed in the HTML element: <div class="title"> <a href="https://username.neocities.org"> </a> </div>
        links = soup.find_all("div", class_="title")
        for link in links:
            neocities_site = link.find("a")["href"]
            all_neocities_sites.append(neocities_site)

        print(f"Scraped {len(all_neocities_sites)} neocities sites")

        # Try to go to next page
        page_count += 1
        next_page_url = initial_page_url + f"&page={page_count}"

    return all_neocities_sites


# Write the list of neocities sites to a txt file
def write_to_file(filename, data):
    with open(filename, "w") as file:
        for site in data:
            file.write(site + "\n")


# write_to_file("all_neocities_sites.txt", get_all_neocities_sites())


# Now enter each neocities site and find referrals to other neocities sites.
# If we find a link to another neocities site, then create an object with fields: root_site, referred_sites[].
# Make sure to exclude any links that are not to neocities sites.
def get_all_neocities_referrals():
    # Create a dictionary to store the root site and referred sites
    all_neocities_referrals = {}

    count = 1
    with open("all_neocities_sites.txt", "r") as file:
        for line in file:
            # if count == 10:
            #     break
            site = line.strip()
            response = requests.get(site)
            soup = BeautifulSoup(response.content, "html.parser")

            # Initialize the current site into all_neocities_referrals with fields: site, referred_sites[]. We will add referred sites to the list. This is to make it easier to create a graph and show the relationship between the sites.
            site = link_formatter(site)
            all_neocities_referrals[site] = {"referred_sites": []}

            print("#" + str(count) + " " + site)
            count += 1

            links = soup.find_all("a")
            for link in links:
                if link.has_attr("href"):
                    # Check if link is not the root site and is not neocities.org and is not already in this site key and is not a relative link
                    if (
                        (site not in link["href"])
                        and ("://neocities.org" not in link["href"])
                        and (
                            link_formatter(link["href"]) not in all_neocities_referrals
                        )
                        and (
                            link["href"].startswith("http")
                            or link["href"].startswith("https")
                        )
                    ):
                        referral = link_formatter(link["href"])

                        # Add the referred site to the dictionary
                        all_neocities_referrals[site]["referred_sites"].append(referral)

    return all_neocities_referrals


all_neocities_referrals = get_all_neocities_referrals()

# Write the dictionary to a csv file. Keep the root site and referred sites in the same row.
with open("all_neocities_referrals.csv", "w") as file:
    for site, referrals in all_neocities_referrals.items():
        file.write(site + ",")
        for referral in referrals["referred_sites"]:
            file.write(referral + ",")
        file.write("\n")

# Now we have a list of neocities sites and their referrals. We can now create a graph of the sites.
