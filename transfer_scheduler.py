import re
import requests
from datetime import datetime, timedelta
from urllib import quote_plus
from bs4 import BeautifulSoup as bs4

from conf import headers, cookies

SCHEDULE_DURATION = 48

request_url = "http://hitwicket.com/premium/scheduler/transferScheduler"

def auto_asking_price(rsp_price):
    rsp_price = int(rsp_price)
    if rsp_price > 1000000:
        return rsp_price - 10000
    elif 450000 < rsp_price < 1000000:
        return rsp_price - 5000
    else:
        return rsp_price


with open('transfer_player_names.txt', 'r') as f:
    player_urls = f.readlines()

    req_list = []
    payload = {}
    prev_time = None # to store time entered between subsequent players for easy input
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
        ele_text = soup.find_all('p')[-1].text # the last one is always RSP text (even in case of players with bdays)
        m = re.search(r'[\d\,]+', ele_text)
        amt_string = m.group(0).replace(',', '')
        rsp_price = int(amt_string)

        # take input asking price from input
        print "Enter Asking Price (RSP is {0}): ".format(rsp_price)
        price = raw_input()
        if price == "":
            # if nothing is entered use auto_asking_price function to get auto price
            price = auto_asking_price(rsp_price)
        else:
            # to check in while and loop if not in safe range
            price = int(price)

        while not (0.65 * rsp_price) <= price <= (1.5 * rsp_price):
            # check if entered price is in safe range
            print "Sorry, please enter again (RSP is {0}: )".format(rsp_price)
            price = raw_input()
            if price == "quit":
                exit()
            elif price == "":
                price = auto_asking_price(rsp_price)
            else:
                price = int(price) # trust user input, no cast checks here

        print "price entered is: ", price
        current_payload = payload
        current_payload['Referer'] = each_url
        prev_time_string = "" if prev_time is None else prev_time
        print "Enter time (format: {0}) ('p', 'prev' or [ENTER] for previous time {1}):".format(
            datetime.strftime(
                datetime.now() + timedelta(minutes=35), # HW needs schedule to be at least 30 minutes ahead. lets go 35 ahead
                "%d-%m-%y %H:%M"
            ), prev_time_string
        )

        time_string = raw_input()
        prev_inputs = ['prev', 'p', '']
        if time_string in prev_inputs and prev_time is not None:
            time_string = prev_time
        elif time_string in prev_inputs and prev_time is None:
            print "enter valid time."
            exit()
        else:
            prev_time = time_string

        schedule_time = datetime.strptime(time_string, "%d-%m-%y %H:%M")
        schedule_time = quote_plus(datetime.strftime(schedule_time, "%d %B, %Y %H:%M")) # convert to format HW uses
        data = 'bidamount={0}&duration_hrs={1}&schedule_transfer=1&schedule_time={2}&player_id={3}'.format(
            price, SCHEDULE_DURATION, schedule_time, player_id
        )

        r = requests.post(
            request_url, data=data, headers=headers, cookies=cookies
        )

        if r.status_code == 200:
            print "Successfully placed bid of {0} for {1}".format(price, each_url)
        else:
            import pdb; pdb.set_trace()
            print "Error occured. Status code: ", r.status_code
            print "response content: "
            # print r.content

        # just some extra spacing to clear up stuff
        print
        print
