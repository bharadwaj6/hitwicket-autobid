import grequests, random, re, time
from datetime import datetime, timedelta
from urllib import quote_plus
from bs4 import BeautifulSoup as bs4

from conf import headers, cookies

def get_schedule_duration():
    return 48

request_url = "http://hitwicket.com/premium/scheduler/transferScheduler"

def fetch_asking_price(rsp_price):
    rsp_price = int(rsp_price)
    if rsp_price > 1000000:
        return rsp_price - 250000
    elif 450000 < rsp_price < 1000000:
        return rsp_price - 150000
    else:
        return rsp_price - 30000

player_rsp = {}
def parse_rsp_factory(*factory_args, **factory_kwargs):
    def parse_responses(response, *request_args, **request_kwargs):
        if response.status_code != 200:
            return None

        soup = bs4(response.content, 'html.parser')
        ele_text = soup.find_all('p')[-1].text # the last one is always RSP text (even in case of players with bdays)
        m = re.search(r'[\d\,]+', ele_text)
        amt_string = m.group(0).replace(',', '')
        rsp_price = int(amt_string)
        player_rsp[factory_kwargs['player_url']] = fetch_asking_price(rsp_price)

    return parse_responses

def get_player_rsp(player_urls):
    player_rsp_pool = grequests.Pool(len(player_urls))
    for player_url in player_urls:
        player_url = player_url.strip() # remove the newline at the end

        # fetch player_id for this guy
        player_id = re.findall(r'\d+', player_url)[0]

        # fetch RSP using sale URL
        sale_url = "http://hitwicket.com/player/sell/{0}".format(player_id)

        req = grequests.get(
            sale_url, headers=headers, cookies=cookies, hooks={'response': [parse_rsp_factory(player_url=player_url)]}
        )

        grequests.send(req, player_rsp_pool)

    print "waiting for responses for 5 seconds..."
    time.sleep(5)
    return player_rsp

def get_random_timedeltas(start_time, end_time, n):
    """Get n number of random timestamps between start_time and end_time.

    start_time, end_time are in seconds.
    """
    return [timedelta(seconds=x) for x in random.sample(range(start_time, end_time), n)]

def generate_bid_times(no_of_players):
    # generate timestamps for the next day
    time_now = datetime.now()
    today = datetime(time_now.year, time_now.month, time_now.day)
    scheduled_day = today + timedelta(days=1)
    peak_time_begin = 64800 # 18:00 clock in the evening
    peak_time_end = 86340 # 23.59 midnight
    least_bid_end = 34200 # day begin to 9:30 AM morning

    # 20% players to least bid time, 45% to peak time, 35% to rest of the day
    least_bid_time_number = int(no_of_players * 0.2)
    peak_time_number = int(no_of_players * 0.45)
    rest_of_the_day_number = no_of_players - peak_time_number - least_bid_time_number

    least_bid_timestamps = [scheduled_day + x for x in get_random_timedeltas(0, least_bid_end, least_bid_time_number)]
    peak_bid_timestamps = [scheduled_day + x for x in get_random_timedeltas(peak_time_begin, peak_time_end, peak_time_number)]
    rest_of_the_day_timestamps = [scheduled_day + x for x in get_random_timedeltas(least_bid_end, peak_time_begin, rest_of_the_day_number)]

    all_timestamps = least_bid_timestamps + peak_bid_timestamps + rest_of_the_day_timestamps
    return all_timestamps

def main():
    with open('transfer_player_names.txt', 'r') as f:
        player_urls = f.readlines()

        # fetch RSP and generate asking price for all players
        get_player_rsp(player_urls)

        req_list = []
        bid_timestamps = generate_bid_times(len(player_urls))
        for i in xrange(len(player_urls)):
            player_url = player_urls[i].strip()
            player_id = re.findall(r'\d+', player_url)[0]

            current_payload = {}
            current_payload['Referer'] = player_url
            schedule_time_url_format = quote_plus(datetime.strftime(bid_timestamps[i], "%d %B, %Y %H:%M")) # convert to format HW uses
            schedule_duration = get_schedule_duration()

            data = 'bidamount={0}&duration_hrs={1}&schedule_transfer=1&schedule_time={2}&player_id={3}'.format(
                player_rsp[player_url], schedule_duration, schedule_time_url_format, player_id
            )
            req_list.append(grequests.post(request_url, data=data, headers=headers, cookies=cookies))

        print player_rsp
        print "placing {} players on sale...".format(len(player_urls))
        print grequests.map(req_list)


if __name__ == "__main__":
    main()
