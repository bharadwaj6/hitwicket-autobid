"""Autobid script for HW."""

import re
import requests

cookies = {
    'e9w1h7v': '952f90111c3934e291624ac2e4c5433f5ee747c7',
    'G_ENABLED_IDPS': 'google',
    'fbm_264141583692052': 'base_domain=.hitwicket.com',
    '__insp_wid': '492284738',
    '__insp_nv': 'true',
    '__insp_ref': 'd',
    '__insp_targlpu': 'http%3A%2F%2Fhitwicket.com%2F',
    '__insp_targlpt': 'Cricket%20News%20%7C%20Play%20Online%20Cricket%20Manager%20Game%20%7C%20Hitwicket',
    '__insp_norec_sess': 'true',
    '__insp_slim': '1450813593535',
    '_ga': 'GA1.2.869549258.1444623036',
    '65e1c853a6a57da7cd092dd9beb53a47': '51b4c1e20f93ea7dfa90d4e0999a2acfa68d0eaba%3A4%3A%7Bi%3A0%3Bs%3A5%3A%2266815%22%3Bi%3A1%3Bs%3A9%3A%22Bharadwaj%22%3Bi%3A2%3Bi%3A1296000%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D',
    'PHPSESSID': 'bsbbgeak5e86l0kqfbttlkeab4',
    'fbsr_264141583692052': 'finjGRMh7IzZDsgM1xAN4fsxZ2EdYO4yxOCJGHcO6LM.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUQ3WXluUGZVQXNIbkU4REpkQ0NGejMteGxSb3J1ZkNkcWFDRE9ZZ2VYbmpMYmx0Mk5OVy1sSFp1T21pRmhkaUY0T3dPYXlTWFVNb0JNUmVPc1gyaFRPaDlLMDRKNElTVU9hVWM4MUpVa2pDaEI0Y0NEOTZVa3pXd3ZPbGhwQUVIVjNjdUN0TGU3TFE2UVhBSlA2SFJMVWJicFl0SFBVcjR5cm1vRmhMbEJ5SnZWUmMxVXkzdGlVN2NsZ3Y3enFDdkJBVDk0bnY3cTNfZEowdjRGb3lIMGtlQXNzRlY1LUIwUC1scHRaR1dqQXRrWkFuUWlZQnhfVUtiNjlZU09XN0pONGhzb0o5X0VxYmlSbENVc3lkSExBZTFYTGI1VHpaVkxaZHVRNlNhUERON3JIZWQxSHRpdktXaDF2TEhKYnNkcHJMbGJ6ZWRkVnlVdlQ4cVdWc295UyIsImlzc3VlZF9hdCI6MTQ1NDg0NjQ4OCwidXNlcl9pZCI6IjE0MzE2NTEzMDYifQ',
}

headers = {
    'Pragma': 'no-cache',
    'Origin': 'http://hitwicket.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,te;q=0.6',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
}

with open('player_names.txt', 'r') as f:
    urls = f.readlines()
    autobid_amount = "500000" # change the amount here
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

        r = requests.post(request_url, headers=temp_headers, cookies=cookies, data=data)

        if r.status_code == 200:
            print "success for player: ", url
        else:
            print "failed for player: ", url
            print r.content
