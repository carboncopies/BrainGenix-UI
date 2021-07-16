
###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

'''
Name: API Server
Description: This is the file used by the BrainGenix API System to get the server to communicate with the leader. This is run standalone due to issues with IP addresses changing based on the currently elected leader zookeeper node.
Date-Created: 2021-03-03
'''

import atexit
import json

import uvicorn
import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware



from Core.Initialization.LoadConfig import LoadLocalConfig

from Core.ThreadManager import ThreadManager

from Core.Initialization.Instantiator import InstantiateLogger

from Core.Initialization.CheckLibraries import CheckImports

from Core.Management.Logger.CLAS import CentralizedLoggerAggregationSystem

from Core.Management.API.ManagementAPI import ManagementAPISocketServer

from Core.Internode.Zookeeper.LFTransitionManager import LFTM

from Core.VersionData import VersionNumber
from Core.VersionData import BranchVersion


from Core.BackendAPIClient.SocketClient import GetSocketClientConfig
from Core.BackendAPIClient.SocketClient import SocketClient


from Core.BackendAPIClient.Auth import AuthenticationManager




# Start Uvicorn #
if __name__ == '__main__':

    # Launch UVICorn Instance #
    uvicorn.run("APIServer:API", host="0.0.0.0", port=2001, log_level="info")
    
    # Shutdown Server #
    os._exit(0)



##############################################################################
## NOTE: A Lowercase "m" Preceeding A Class Means It's a Main System        ##
## NOTE: A Lowercase "s" Preceeding A Class Means It's a Subsystem          ##
##############################################################################



# Set Version Information
Version = '0.0.7'
Branch = 'dev' # 'dev' or 'rel'


# Load Config #
LoggerConfigDict = LoadLoggerConfig(ConfigFilePath = 'Config/LoggerConfig.yaml')
DBConfigDict = LoadDatabaseConfig(ConfigFilePath = 'Config/DatabaseConfig.yaml')
ZKConfigDict = LoadZookeeperConfig(ConfigFilePath = 'Config/ZookeeperConfig.yaml')
MAPIConfigDict = LoadManagementAPIServerConfig(ConfigFilePath = 'Config/ManagementAPIConfig.yaml')


# Initialize Logger #
mLogger = InstantiateLogger(DBConfigDict, LoggerConfigDict)


# Purges The Log Buffer On System Exit #
@atexit.register
def CleanLog():
    mLogger.CleanExit()


# Connect To Zookeeper Service #
sZookeeper = mThreadManagerInstance.InstantiateZK(mLogger, SystemConfiguration)


# Get Socket Client Config #
SocketClientConfig = GetSocketClientConfig(mLogger, sZookeeper, MAPIConfigDict)


# Connect To NES Server #
sNESSocketConnection = SocketClient(mLogger, SocketClientConfig)
sNESSocketConnection.BenchmarkConnection()


# Instantiate Auth Manager #
sAuthenticationManager = AuthenticationManager(mLogger, DBConfigDict)


# Instantiate FastAPI System #
API = FastAPI()


# Set Allowed Origins #
origins = [
    "*"
]

API.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


# Define Methods In API #
@API.post('/')
async def root(RequestJSON: Request):

    try:


        # Decode Incoming Command #
        RequestBytes = await RequestJSON.body()
        CommandScope = json.loads(RequestBytes.decode())


        # Check if Token Present #
        if 'Token' not in CommandScope:
            return {'Name':'Error', 'Content':'Token not in request!'}

        # Check Authentication #
        TokenStatus = sAuthenticationManager.ValidateToken(CommandScope['Token'])
        if TokenStatus != 'Valid Token':
            return {'Name': 'Error', 'Content':TokenStatus}

        # Check If Scope Present #
        if 'SysName' not in CommandScope:
            return {'Name':'Error', 'Content':'Scope Not Set, Check SysName Parameter'}


        # Load And Return Command For NES #
        if CommandScope['SysName'] == 'NES':
            return sNESSocketConnection.SendRaw(RequestBytes)
        ## NOTE: ADD OTHER SCOPES FOR ERS AND STS HERE LATER ##
        else:
            return {'Name':'Error', 'Content':'ScopeError: No Valid Server Is Available To Handle Your Request With The Given Scope. Valid Scopes Are "NES", "ERS", "STS".'}

    except Exception as e:
        print('Error: ' + e)

# Authentication #
@API.post('/Authenticate')
async def Authentication(RequestJSON: Request):

    try:

        # Decode Incoming JSON #
        RequestBytes = await RequestJSON.body()
        CommandScope = json.loads(RequestBytes.decode())

        #print(CommandScope)

        # Get Uname, Passwd #
        Username = CommandScope['Username']
        Password = CommandScope['Password']

        # Check Uname, Passwd #
        if ((Username == 'Parzival') and (Password == 'Riddle')): ## This needs to be replaced with real auth, not hardcoded ##

            Response = {'Token' : sAuthenticationManager.GenerateToken(Username)}

        # Auth Fails #
        else:
            
            # Set Fail Msg #
            Response = {'Error' : 'Authentication Failure'}

        # Return Response #
        return Response
    
    except Exception as e:
        print(e)



# Define Test Requests #
@API.get('/APIServerTest')
async def RandomNumberTest():
    return {'Name': 'Get Request Test', 'Content' : '"It just works" - Todd Howard'}


@API.get('/APIBackendTest')
async def APIBackendTest():
    return sNESSocketConnection.SendCommand({"SysName":"NES", "CallStack":"TestAPI", "KeywordArgs": {}})


# Print MOTD #
mLogger.Log('Starting API Server')
mLogger.Log('')
mLogger.Log('---------------------------------------------------------------------------')
mLogger.Log('██████╗ ██████╗  █████╗ ██╗███╗   ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗')
mLogger.Log('██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝████╗  ██║██║╚██╗██╔╝')
mLogger.Log('██████╔╝██████╔╝███████║██║██╔██╗ ██║██║  ███╗█████╗  ██╔██╗ ██║██║ ╚███╔╝ ')
mLogger.Log('██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ ')
mLogger.Log('██████╔╝██║  ██║██║  ██║██║██║ ╚████║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗')
mLogger.Log('╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝')
mLogger.Log('---------------------------------------------------------------------------')
mLogger.Log('')
mLogger.Log('    +-----------------------------------------------------------------+')
mLogger.Log(f'    |          Welcome To BrainGenix-APIServer Version {Version}-{Branch}      |')
mLogger.Log('    +-----------------------------------------------------------------+')
mLogger.Log('')
