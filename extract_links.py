from BeautifulSoup import BeautifulSoup
import re

with open('auction_page.html', 'r') as f:
    html_page = f.read()

soup = BeautifulSoup(html_page)
all_links = []
for link in soup.findAll('a', attrs={'href': re.compile("^/player/show")}):
    current = link.get('href')
    all_links.append(current)
    print current

with open('player_names.txt', 'w') as f:
    f.write('\n'.join(["http://hitwicket.com" + x for x in all_links]))
