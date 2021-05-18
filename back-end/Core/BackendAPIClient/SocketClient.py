###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

import time
import socket
import json

'''
Name: Socket Backend Client
Description: This is the main file for the BrianGenix Socket Based Backend.
Date-Created: 2021-05-17
''' 

class SocketClient(): # Creates A Client Socket System #

    def __init__(self, Logger, ConfigParams): # Initialization #

        # Save Local Pointers #
        self.Logger = Logger
        self.IP = ConfigParams['IP']
        self.Port = ConfigParams['Port']

        # Connect To Server #
        

def GetSocketClientConfig(Logger, ZookeeperInstance, BackendConfigDict): # Reads Configuration For SocketClient #

    # Log Start Message #
    Logger.Log('Getting Socket Client Host Information')

    # Get Leader Znode #
    Logger.Log('Finding Leader Znode')

    # Check For Leader #
    while not ZookeeperInstance.ZookeeperConnection.exists('/BrainGenix/System/Leader'):
        time.sleep(0.1)

    # Decode Leader Information #    
    ZookeeperLeaderInformation = ZookeeperInstance.ZookeeperConnection.get('/BrainGenix/System/Leader')[0]
    print(ZookeeperLeaderInformation)
    ZookeeperLeaderInformation = json.loads(ZookeeperLeaderInformation)

    print(ZookeeperLeaderInformation)