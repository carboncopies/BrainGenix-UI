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

        # Create Socket Host Variable #
        self.Logger.Log('Creating Host Variable')
        self.SocketHost = (self.IP, self.Port)

        # Connect To Server #
        self.Logger.Log(f'Connecting To Remote Host At Host: {self.SocketHost}')
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.connect(self.SocketHost)


    def SendCommand(self, CommandDict:dict): # Sends A Command To The Server #

        # Encode Dict As JSON String #
        self.CommandString = json.dumps(CommandDict)

        # Encode As Bytes #
        self.CommandString = self.CommandString.encode()

        # Send To Server #
        self.Socket.send(self.CommandString)

        # Await Response #
        self.ResponseBytes = self.Socket.recv(65535)

        # Decode Response #
        self.ResponseString = self.ResponseBytes.decode()

        # Convert To Dict #
        self.ResponseDictionary = json.loads(self.ResponseString)

        # Return String #
        return self.ResponseDictionary


    def Disconnect(self): # Disconnects The Client #

        # Call Disconnect #
        self.Socket.send(json.dumps({'CallStack': 'Disconnect'}).encode())
        self.Socket.close()


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
    ZookeeperLeaderInformation = json.loads(ZookeeperLeaderInformation)
    IPAddr = ZookeeperLeaderInformation['IP'].split(':')[0]

    # Get Port Information #
    Port = BackendConfigDict['Port']

    return {'IP' : IPAddr, 'Port' : Port}