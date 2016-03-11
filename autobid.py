"""Aysnc Autobid script for HW."""

import re
import grequests
from conf import cookies, headers, AUTOBID_VALUE

with open('player_names.txt', 'r') as f:
    urls = f.readlines()
    autobid_amount = AUTOBID_VALUE

    request_list = []
    for url in urls:
        url = url.rstrip('\n')
        # temp headers to insert referer in header for this player
        temp_headers = headers
        temp_headers['Referer'] = url

        # fetch player id for sending request to autobid url
        player_id = re.findall('\d+', url)[0]

        # autobid form data
        data = 'AutoBid%5Bamount%5D={0}&AutoBid%5Bdont_out_bid_seller%5D=0&AutoBid%5Bdont_out_bid_seller%5D=1&AutoBid%5Bdelayed_start%5D=0&AutoBid%5Bdelayed_start%5D=1&yt1=Create+Auto+Bid'.format(
            autobid_amount)

        request_url = "http://hitwicket.com/premium/autoBid/create/player_id/%s" % player_id

        request_list.append(grequests.post(request_url, headers=temp_headers, cookies=cookies, data=data))

    print grequests.map(request_list)
