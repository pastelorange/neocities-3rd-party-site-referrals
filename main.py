import requests
from bs4 import BeautifulSoup
from neo4j import GraphDatabase


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


def get_all_neocities_sites():
    """Traverse the Neocities most followed page and collect all user sites."""

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
    """Writes the list of all neocities sites to a text file."""

    with open("all_neocities_sites.txt", "w", encoding="utf-8") as file:
        for site in all_neocities_sites:
            file.write(site + "\n")


def process_link(link: str, site: str, site_referrals: dict):
    """Check the link and add it to the site_referrals dictionary if it meets the criteria."""

    if link.has_attr("href"):
        link = link["href"]
        # Check if link is not the root site and is not neocities.org and is not already in this site key and is not a relative link
        if (
            (site not in link)
            and ("://neocities.org" not in link)
            and (link_formatter(link) not in site_referrals[site]["referrals"])
            and (link.startswith("http") or link.startswith("https"))
        ):
            referral = link_formatter(link)

            # Add the referred site to the dictionary
            site_referrals[site]["referrals"].append(referral)


def search_for_site_referrals():
    """
    Search for site referrals within each site.
    It will search through the index, home, and links pages of each site.
    This function will return a dictionary ("site": {"referrals": []})
    """

    # Create a dictionary to store the root site and referred sites
    site_referrals = {}

    count = 1

    with open("all_neocities_sites.txt", "r") as file:
        for line in file:
            try:
                print(f"Scraping site {count}")
                count += 1

                site = line.strip()

                response = requests.get("https://" + site)
                soup = BeautifulSoup(response.content, "html.parser")

                # Initialize the current site into a dictionary with fields: site, referrals[].
                site_referrals[site] = {"referrals": []}

                # Find and collect links
                links = soup.find_all("a")
                for link in links:
                    process_link(link, site, site_referrals)

                # Check if the site has a /home page. If it does, then scrape the page for more referrals.
                response = requests.get("https://" + site + "/links")
                soup = BeautifulSoup(response.content, "html.parser")

                # Find and collect links
                links = soup.find_all("a")
                for link in links:
                    process_link(link, site, site_referrals)

                # Check if the site has a /links page. If it does, then scrape the page for more referrals.
                response = requests.get("https://" + site + "/links")
                soup = BeautifulSoup(response.content, "html.parser")

                # Find and collect links
                links = soup.find_all("a")
                for link in links:
                    process_link(link, site, site_referrals)

            except Exception as err:
                print(err)
                continue  # Skip the iteration if any errors are encountered

    return site_referrals


def save_site_referrals_to_csv(site_referrals: dict):
    """Write the dictionary to a csv file. Keep the root site and referred sites in the same row."""

    with open("site_referrals.csv", "w", encoding="utf-8") as file:
        # Write the header
        file.write("Site,Referrals\n")

        for site, referrals in site_referrals.items():
            # If there are no referrals, then skip the site
            if referrals["referrals"] == []:
                continue

            file.write(site + ",")
            for referral in referrals["referrals"]:
                file.write(referral + ",")
            file.write("\n")


def create_neo4j_graph():
    """Create a webgraph of the sites in Neo4j. NOTE: You need to place the csv file in the import folder of your Neo4j database."""

    uri = "bolt://localhost:7687"
    database = "neo4j"
    password = "bruh1234"
    driver = GraphDatabase.driver(uri, auth=(database, password))

    with driver.session() as session:
        session.run(
            """
            LOAD CSV WITH HEADERS FROM 'file:///site_referrals.csv' AS row
            MERGE (site:Site {name: COALESCE(row.Site, "")})
            WITH site, split(row.Referrals, ",") AS referrals
            UNWIND referrals AS referral
            MERGE (referred:Site {name: COALESCE(referral, "")})
            MERGE (site)-[:REFERS]->(referred)
            """
        )

    driver.close()


# Step 1: Get all neocities sites
# save_all_neocities_sites_to_txt(get_all_neocities_sites())

# Step 2: Search for site mentions within each site
# save_site_referrals_to_csv(search_for_site_referrals())

# Step 3: Create a graph of the sites in Neo4j
# create_neo4j_graph()

"""Use this script to query the most referred sites
MATCH (n)--()
RETURN n, COUNT(*) AS neighbours
ORDER BY neighbours DESC
LIMIT 100
"""
