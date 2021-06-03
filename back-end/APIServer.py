 
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

from requests.sessions import REDIRECT_STATI
import uvicorn
import random
import os

from random import SystemRandom


from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from Core.Initialization.LoadConfig import LoadLoggerConfig
from Core.Initialization.LoadConfig import LoadDatabaseConfig
from Core.Initialization.LoadConfig import LoadZookeeperConfig
from Core.Initialization.LoadConfig import LoadManagementAPIServerConfig

from Core.BackendAPIClient.SocketClient import GetSocketClientConfig
from Core.BackendAPIClient.SocketClient import SocketClient

from Core.Initialization.Instantiator import InstantiateZK
from Core.Initialization.Instantiator import InstantiateLogger


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
sZookeeper = InstantiateZK(mLogger, ZKConfigDict)


# Get Socket Client Config #
SocketClientConfig = GetSocketClientConfig(mLogger, sZookeeper, MAPIConfigDict)


# Connect To NES Server #
sNESSocketConnection = SocketClient(mLogger, SocketClientConfig)
#sNESSocketConnection.BenchmarkConnection()


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
    
    RequestString = await RequestJSON.body()
    RequestString = RequestString.decode()


    # Check For Empty Command #
    if RequestString != '"{\"SysName\": \"NES\", \"CallStack\": \"\", \"KeywordArgs\": {}}"':
    
        # Load And Return Command #
        RequestString = json.loads(RequestString)
        return sNESSocketConnection.SendRaw(RequestString)
    
    else:
    
        # Return Bad Command #
        return '{"Message":"BAD COMMAND"}'


@API.get('/APIServerTest')
async def RandomNumberTest():
    return {'message' : '"It just works" - Todd Howard'}


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
