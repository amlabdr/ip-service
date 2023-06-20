import os, logging
import pydot

class Config:
    def __init__(self):
        self.controller_url = os.environ.get('CONTROLLER_URL')
        


    