###########################################################
# NOTE: DO NOT USE THIS IN PRODUCTION, IT IS *NOT* SECURE #
###########################################################

###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

import time
import uuid
import atexit
import json
import requests
from requests.sessions import Request


'''
Name: ZKCLI-Client
Description: This file is the BG Cli client.
Date-Created: 2021-01-19
'''

class Client(): # Client For BrainGenix System #

    '''
    This class contains the ZKCLI client setup.
    It connects to ZK via the arguments passed to __init__ and authenticates via the given username and password.
    The client can then be run via calling the Main function, which drops the user into the actual command line environment.
    '''


    def __init__(self, Host:str):

        '''
        Initializes the Client, Authenticates, and waits until connection accepted.
        '''

        # Set Local Pointer #
        self.Host = Host


    def Main(self): # Main Loop #

        '''
        This is the actual interactive ZKCLI aspect of the client.
        This contains the loop that gets the user's input and passes it on to the server.
        '''

        # Connect To HTTP API #
        RequestObject = requests.post(self.Host, json="{'SysName':'NES', 'CallStack':'TestAPI', 'KeywordArgs': {}}")
        print(RequestObject.json())


# Instantiate The Client #
CLI = Client('http://10.1.4.2:2001')
CLI.Main()