import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs4

from conf import headers, cookies

SCHEDULE_DURATION = 48

request_url = "http://hitwicket.com/premium/scheduler/transferScheduler"

print "input time to start: (like 24-02-2016 03:00:00)"

with open('transfer_player_names.txt', 'r') as f:
    player_urls = f.readlines()

    req_list = []
    payload = {}
    for each_url in player_urls:
        # fetch player_id for this guy
        player_id = re.findall(r'\d+', each_url)[0]

        # fetch RSP using sale URL
        sale_url = "http://hitwicket.com/player/sell/{0}".format(player_id)
        r = requests.get(sale_url, headers=headers, cookies=cookies)
        # Recommended selling price for this player is <i class="fa fa-inr rupee_symbol_visibility"></i> 1,370,000</p>
        if r.status_code != 200:
            print "something went wrong while fetching player sell price details."
            print "status_code: ", r.status_code
            print r.content
            break

        soup = bs4(r.content, 'html.parser')
        ele_text = soup.div.div.div.p.text
        m = re.search(r'[\d\,]+', ele_text)
        amt_string = m.group(0).replace(',', '')
        rsp_price = int(amt_string)

        # take input asking price from input
        print "Enter Asking Price (RSP is {0}): ".format(rsp_price)
        price = input()
        while not (0.65 * rsp_price) <= price <= (1.5 * rsp_price):
            print "Sorry, please enter again (RSP is {0}: )".format(rsp_price)
            price = raw_input()
            if price == "quit":
                exit()
            else:
                price = int(price) # trust user input, no cast checks here

        print "price entered is: ", price
        current_payload = payload
        current_payload['Referer'] = each_url
        data = 'bidamount={0}&duration_hrs={1}&schedule_transfer=1&schedule_time=24+February%2C+2016+07%3A25&player_id=12734304'
        print "data: ", data

        # requests.post(
        #     request_url, data=data, headers=headers, cookies=cookies
        # )
