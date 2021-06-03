###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

from json.decoder import JSONDecodeError
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


    def SendRaw(self, CommandString:bytes): # Sends A Command To The Server (RAW Bytes) #



        # Send To Server #
        self.Socket.send(CommandString)

        # Await Response #
        self.ResponseBytes = self.Socket.recv(65535)

        # Decode Response #
        self.ResponseString = self.ResponseBytes.decode()

        # Convert To Dict #
        try:

            self.ResponseDictionary = json.loads(self.ResponseString)

        except JSONDecodeError:

            self.ResponseDictionary = {"Message":"BAD COMMAND"}


        # Return String #
        return self.ResponseDictionary


    def BenchmarkConnection(self, NumberCommands = 1000, LogOutput = True): # Runs Connection Benchmark #

        # If Log Output, Log Output #
        if LogOutput:
            self.Logger.Log(f'Starting MAPI Server Benchmark With {NumberCommands} Command Calls')


        # Get Current Unix Epoch #
        StartTime = time.time()

        # Enter Loop And Send Test Command #
        for _ in range(NumberCommands):
            self.SendCommand({"SysName":"NES", "CallStack":"TestAPI", "KeywordArgs": {}})

        # Measure Duration Of Test #
        DeltaTime = time.time() - StartTime

        # Calculate Time Per Call #
        TimePerCall = DeltaTime / NumberCommands

        # If LogOutput, Show Results #
        if LogOutput:
            self.Logger.Log(f'Benchmark Complete, Each API Call (TestAPI Command) Took {round(TimePerCall*1000, 4)}ms')

        # Return Value #
        return TimePerCall



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