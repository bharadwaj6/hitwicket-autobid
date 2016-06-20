import requests
from all_conf import credentials

for cred in credentials:
    print "checking in ", cred[2]
    r = requests.get('http://hitwicket.com/alliance/submitAttendance/206', headers=cred[0], cookies=cred[1])
    print "checked in ", cred[2], r.status_code

print "finished checking in alliance"
