import re
import grequests
from bs4 import BeautifulSoup

from conf import headers, autobid_cancel_headers, cookies, autobid_cancel_cookies

with open('player_transfers_to_delete.txt', 'r') as f:
    player_urls = [url.strip() for url in f.readlines()]

    req_list = [grequests.get(each_url, headers=headers, cookies=cookies) for each_url in player_urls]
    initial_player_ids = [re.findall(r'\d+', each_url)[0] for each_url in player_urls]
    responses = grequests.map(req_list)

    ctr = 0
    cancel_bids_players = {}
    bid_urls_players = {}
    for resp in responses:
        if resp is not None and resp.status_code < 400:
            soup = BeautifulSoup(resp.content, 'html.parser')
            # bid is placed on this guy, add their player_id to cancel_bids_players list
            cancel_bids_players[initial_player_ids[ctr]] = player_urls[ctr]

            # autobid cancel url is unique for each player and has to be scraped again
            for ele in soup.findAll(text=re.compile(r'Cancel it!')):
                link = ele.parent
                bid_urls_players[initial_player_ids[ctr]] = "http://hitwicket.com" + link.attrs['href']
        ctr += 1

print "cancel_bids_player_details: ", cancel_bids_players

cancel_req_list = []
for player_id in cancel_bids_players:
    temp_headers = autobid_cancel_headers
    temp_headers['Referer'] = cancel_bids_players[player_id]

    cancel_url = bid_urls_players[player_id]
    cancel_req_list.append(grequests.get(cancel_url, headers=temp_headers, cookies=autobid_cancel_cookies))

resps = grequests.map(cancel_req_list)

print "canceled transfers: ", resps
