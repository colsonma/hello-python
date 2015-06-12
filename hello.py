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

api = twitter.Api(['Twitter'])
 access_consumer_key = os.environ['access_consumer_key'],
 access_consumer_secret = os.environ['access_consumer_secret']
 access_token_key = os.environ['access_token_key']
 access_token_secret = os.environ['access_token_secret']

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

#attempt at adding a GUI
    
class simpleapp_tk(Tkinter):
    def __init__(self,parent):
        Tkinter.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")
        
        button = Tkinter.Button(self,text=u"Click me!",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello!")
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
          
    
def OnButtonClick(self):
    self.labelVariable.set( self.entryVariable.get()+" (You clicked the button!)")
    self.entry.focus_set()
    self.entry.selection_range(0, Tkinter.END)
    
def OnPressEnter(self,event):
    self.labelVariable.set( self.entryVariable.get()+" (You Pressed Enter!)")
    self.entry.focus_set()
    self.entry.selction_range(0, Tkinter.END)
    


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
	""".format(COLOR,my_uuid,r.get("hit_counter"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
	 app = simpleapp_tk(None)
	 app.title('Twitter Search')
	 app.mainloop()




    


