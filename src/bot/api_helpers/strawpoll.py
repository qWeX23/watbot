import requests
import json

def get_poll_data(id):
	url='https://www.strawpoll.me/api/v2/polls/{}'.format(id)
	response = requests.get(url)
	return

def get_poll_url(id):
	return 'http://www.strawpoll.me/{}'.format(id)

def make_poll(title,options,multi=False,dupckeck='normal',captcha='false'):
	url='https://www.strawpoll.me/api/v2/polls'
	payload = {'title':title,'options':options,'multi':multi,'dupcheck':dupckeck,'captcha':captcha}
	payload = json.dumps(payload)
	headers = {'Content-Type':'application/json'}
	response = requests.post(url,data=payload,headers=headers)
	return response.json()
