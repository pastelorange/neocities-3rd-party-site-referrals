# Neocities Webgraph

This is a web scraping project of [Neocities](https://neocities.org), investigating what are the most referenced (hyperlinked) third-party sites on each popular Neocities sites.

The web scraping data is from April 1, 2024.

`all_neocities_sites.txt` contains the domains of the top 10,000 Neocities sites, sorted by follower count.\
`all_neocities_sites_sort_by_new.txt` contains the domains of every Neocities site (count: 358,000), sorted by last updated.\
`site_referrals.csv` contains each of the top 10,000 sites, and what third-party sites they referred.\
`most_referred_sites.csv` contains a list of the most referred third-party sites.

![Graph visualization of the 9565 sites](https://github.com/pastelorange/neocities-site-referrals/blob/main/Screenshot%202024-04-03%20114715.png?raw=true)

![Graph visualization of the 9565 sites](https://github.com/pastelorange/neocities-site-referrals/blob/main/Screenshot%202024-04-03%20114809.png?raw=true)

![Pie chart of the site referrals](https://cdn.discordapp.com/attachments/1142497370899222538/1331782055692079195/image.png?ex=6792de31&is=67918cb1&hm=6c609de2c7d47974c36180f712fe7ba40831037e1be1240c80877a2023ae58f2&)

## Abstract

This web scraping project is important as it delves into the intricate relationships
between Neocities sites. Neocities, the spiritual successor to the early internet's
GeoCities, is a free site hosting platform that was pivotal in popularizing indie web
culture in the modern age. A vital aspect of this culture is the interaction between
websites and how they foster community in a predominantly anonymous and read-only
digital realm. A prevalent practice observed in Neocities sites is the promotion or
'shouting out' of another Neocities user's site through a link. This report meticulously
examines the design and execution of the web crawler and provides valuable insights
into site referrals amongst the top 10,000 Neocities sites.

## Introduction

As of April 2nd, 2024, Neocities claims to host 760,000 user sites. However, this
number is either incorrect or could be the total number of sites created. The Neocities'
browse page is a site directory where one can sort by most followed, last updated,
newest, oldest, and more. There are 100 sites per pagination and 3585 pages, multiplied
to equal 358,000 sites, a little under half of the claimed number. Initially, the plan was
to utilize a dataset of 358,000 sites. However, the dataset was revised to the top 10,000
most followed sites due to time and computing constraints. These sites, being more
active, having more readers, and of higher quality, were deemed to provide a more
comprehensive and representative dataset. Computing this smaller subset was also
significantly more manageable than the entire dataset, ensuring the project's feasibility.

## Methods

This project was executed using the Python 3 package Beautiful Soup 4, a
powerful tool for web scraping. A script was created to crawl the Neocities' top 10,000
most followed sites. The crawling process was efficient, taking approximately 0.8
seconds per pagination, translating to 80 seconds to collect the 10,000 sites. Each site
was written in a text file. No errors were encountered parsing the HTML.
A second crawling process followed, where each site was crawled and checked for
external links (i.e., links not referring to the current site). This process heavily utilized
string parsing and validation. Validation only accepted external links, not the parent
neocities.org website, and links could only be collected once per site. It is worth noting
that Neocities sites can have custom domains and not fall under the Neocities.org
subdomain. If the link passed validation, it was added to a Python dictionary. Every site
collected was required to have one or more referrals. The resulting dictionary
represented a web graph of site referrals and was written into a CSV file.
The crawler checked three routes for each site: the index ("/") and a home and
links page ("/home" and "/links") if they existed. Through anecdotal experience, Neocities
sites are often structured in this way with these route names. Index and home pages
often contain banners and graphics for external links, while links pages refer readers to
other places on the web. An improvement could be traversing every site route
dynamically or according to a sitemap, but time and computing constraints did not allow
that.

It took approximately 1.2 seconds to crawl per site, totaling 131 minutes to crawl
and write the output to a CSV file. There were a total of 6562 sites out of the initial
10,000. This was the most tedious step in the project, as runtime errors would
sometimes only appear once thousands of iterations into the process. The most
common error encountered was HTTP or SSL-related and occurred when trying to
establish a response to the web page. If an exception occurred, the site was skipped,
and the iteration continued.

After this process, each CSV record was inserted into a local Neo4j database to
build the web graph. Then, a query was executed for the most referred sites, or in other
words, the nodes with the most neighbors.

## Results

Of the initial sample size of 10,000 Neocities sites, 9565 had no errors when web
crawling and one or more site referrals.

## Discussion

The top site with 299 referrals was YouTube, which is perhaps unsurprising. The
second was Twitter (258 referrals), also unsurprising. The third was Smart Guestbook
(smartgb.com), which had 146 referrals. Smart Guestbook is a web service allowing users
to embed a guest book on their site using HTML. Web admins often have a section on
their site for users to leave a comment, usually sorted by newest. Guest books are
archaic in the age of social media, where app users can more easily and directly
communicate with each other. However, this is not the case on Neocities, as sites are
mainly static but maintain a sense of community and interactivity.

In fourth place was Cursors-4U (cursors-4u.com), with 144 referrals—Cursors-4U,
which provides resources for custom cursor graphics. Neocities sites are more personal
and often creatively designed than the current web's popular clean and minimal design
language. Heavy usage of graphic elements, including custom cursors, is common.
Cursors-4U allow sites to hotlink the resource directly instead of hosting it on their site,
which likely contributes to the high referral count.

Skipping past fifth, which was Instagram (132 referrals), sixth was Web Neko
(webneko.net) with 120 referrals. Web Neko hosts graphics and JavaScript code to play a
game where an animated cat chases the mouse cursor around the web page.
Mab's Land (mabsland.com) is in seventh place, with 118 referrals. This site is
home to the furry digital artwork by its author. Concerning why sites refer to Mab's Land,
this site hosts graphics related to content and age ratings, which others often use and
credit on their sites.

In eighth place is imood (imood.com), with 97 referrals. imood is a site where
users can set a mood status to keep in touch with them. Users can embed a mood
indicator using HTML on their web pages. Neocities sites often feature a mood
indicator, which helps share an aspect of the person running the site. It is worth noting
that imood has been running since 1999 and is an example of early social media.

Skipping past more popular sites such as Tumblr, Ko-fi, Discord, SoundCloud, and
Internet Archive, sadgrl.online (sadgrl.online) is in 20th place with 41 referrals. In 2024,
this site was recently archived and moved to a new domain (goblin-heart.net), but it is
still the most followed Neocities site. sadgirl.online was a personal site primarily based
around internet culture. There are also guides and resources for web development, so
other sites likely refer back to this site as a way of crediting the help.
In 21st place is Hotline Webring (hotlinewebring.club), with 38 referrals. This site
exhibits the concept of a webring, a collection of sites where each site links to its
neighbors to form a ring. Webrings are an archaic method of finding related sites and
were popular before search engines became prevalent. Since 38 sites refer to the
Hotline Webring, it can be assumed that those sites are members of the Webring. More
popular sites, Neocities sites, web services, and resources appear after Hotline Webring.
A place for improvement is better handling subdomains in the string validation
function. The resulting dataset had sites like "web.archive.org" and "archive.org" when
they are effectively the same site, polluting the data quality. There could have been a
check to allow Neocities user sites that follow the "username.neocities.org" pattern while
disallowing subdomains from other sites from being collected as a unique site.

## Conclusion

Before conducting this project, it was expected that more Neocities sites would
have more referrals. A few factors can affect this expectation. One is the relatively small
sample size of this web crawling project. The sample size was only the top 10,000 sites
instead of the available 358,000. Another factor is the limitation of crawling predefined
routes (index, home, and links pages) when not all sites will follow the same format.
If there are any conclusions to be drawn by this limited-scope project, it is that
the indie web and modern Big Tech web coexist together. Popular websites such as
YouTube were among the most referred websites. Neocities is not in its own bubble and
still utilizes external sources from all around the World Wide Web. Many Neocities
conventions and culture revolve around early internet nostalgia and still use archaic
systems, which still have value if one values individuality and personal expression on the
internet.
