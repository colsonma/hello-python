import os
import uuid
import urlparse
import redis
import json
import sys
import codecs
from datetime import datetime
from TwitterAPI import TwitterAPI
CONSUMER_KEY = os.environ['access_consumer_key']
CONSUMER_SECRET = os.environ['access_consumer_secret']
ACCESS_TOKEN_KEY = os.environ['access_token_key']
ACCESS_TOKEN_SECRET = os.environ['access_token_secret']

#o.CONSUMER_KEY = os.environ['access_consumer_key']
#o.CONSUMER_SECRET = os.environ['access_consumer_secret']
#o.ACCESS_TOKEN_KEY = os.environ['access_token_key']
#o.ACCESS_TOKEN_SECRET = os.environ['access_token_secret']

TRACK_TERM = 'DevOps'

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
#api = TwitterOAuth(o.CONSUMER_KEY, o.CONSUMER_SECRET, o.ACCESS_TOKEN_KEY, o.ACCESS_TOKEN_SECRET)

t = api.request('statuses/filter', {'track': TRACK_TERM})

all_the_tweets = ""
for item in t:
    if 'text' in item:
            all_the_tweets += item['text'] 

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
r.set("hit_counter", 1)

  
@app.route('/')
def hello():
	r.incr("hit_counter")
 
	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:<br/>
	{}
	<center><h1><font color="black">Hit Counter:<br/>
	{}
	<center><h1><font color="white">Twitter Search:<br/>
	{}
	</center>

	</body>
	</html>
	""".format(COLOR,my_uuid,r.get("hit_counter"),all_the_tweets)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
	




    


