import os
import uuid
import urlparse
import redis
import json
import twitter
import Tkinter
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

api = twitter.Api(
 access_consumer_key = os.environ['access_consumer_key'],
 access_consumer_secret = os.environ['access_consumer_secret']
 access_token_key = os.environ['access_token_key']
 access_token_secret = os.environ['access_token_secret']
)

search = api.GetSearch(
    term=raw_input("Search Term"),
    lang='en',
    result_type='recent',
    count=100,
    max_id=''
)

for t in search:
    print t.user.screen_name + ' (' + t.created_at + ')'
    #Add the .encode to force encoding
    print t.text.encode('utf-8')
    print ''

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
	""".format(COLOR,my_uuid,r.get("hit_counter"),search("Search Term"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
	 app = simpleapp_tk(None)
	 app.title('Twitter Search')
	 app.mainloop()




    


