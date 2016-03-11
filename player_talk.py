import re
import grequests

from conf import headers, cookies, player_talk_description

with open('player_talk.txt', 'r') as f:
    player_urls = f.readlines()
    request_list = []

    for player_url in player_urls:
        player_url = player_url.rstrip()
        new_headers = headers
        new_headers['Referer'] = player_url

        player_id = re.findall(r'\d+', player_url)[0]
        data = 'player_id={}&description={}'.format(player_id, player_talk_description)

        request_list.append(grequests.post('http://hitwicket.com/premium/player/updateDescription', headers=new_headers, cookies=cookies, data=data))

    print grequests.map(request_list)
