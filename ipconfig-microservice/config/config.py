import os, logging
import pydot

class Config:
    def __init__(self):
        self.repeat_timer = os.environ.get('REPEAT_TIMER','10')
        self.controller_url = os.environ.get('CONTROLLER_URL','http://10.11.200.125:8787')
        


    