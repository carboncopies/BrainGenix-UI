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
        self.EndChar = '#'
        self.Hostname = Host.strip('http://').strip('https://')
        self.Username = 'root'

        # Set Config Parameters #
        self.Scope = ''


    def Main(self): # Main Loop #

        '''
        This is the actual interactive ZKCLI aspect of the client.
        This contains the loop that gets the user's input and passes it on to the server.
        '''

        while True:

            # Get User Input From Command #
            CommandString = input(f'{self.Username}@{self.Hostname}{self.EndChar}')

            # Parse Command #
            if CommandString.lower().startswith('scope '):
                self.Scope = CommandString.split(' ')[1]
                print(f'Setting Scope To {self.Scope}')

            else:
                # Get Command Callstack #
                Callstack = CommandString.split(' ')[0]

                # Get Arguments #
                Arguments = {}
                for ArgumentString in CommandString.split(' ')[1:]:

                    ArgumentKey = ArgumentString.split('=')[0]
                    ArgumentValue = ArgumentString.split('=')[1]

                    Arguments.update({ArgumentKey : ArgumentValue})

                # Format As JSON #
                CommandDict = {'SysName':self.Scope, 'CallStack':Callstack, 'KeywordArgs':Arguments}

                # Send Command And Get Output #
                Output = self.ExecuteCommand(CommandDict)

                # Print Output #
                print(Output)


    def ExecuteCommand(self, CommandJSON:str): # Executes A Given Command #

        # Run Command #
        RequestObject = requests.post(self.Host, json=CommandJSON)
        return RequestObject.json()


# Instantiate The Client #
CLI = Client('http://10.1.4.2:2001')
CLI.Main()