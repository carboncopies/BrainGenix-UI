 
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
import random
import os

from random import SystemRandom


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Core.Initialization.LoadConfig import LoadLoggerConfig
from Core.Initialization.LoadConfig import LoadDatabaseConfig
from Core.Initialization.LoadConfig import LoadZookeeperConfig

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


# Initialize Logger #
mLogger = InstantiateLogger(DBConfigDict, LoggerConfigDict)


# Purges The Log Buffer On System Exit #
@atexit.register
def CleanLog():
    mLogger.CleanExit()


# Connect To Zookeeper Service #
sZookeeper = InstantiateZK(mLogger, ZKConfigDict)


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



# Create A Connection zNode #
cryptogen = SystemRandom()
ConnectionNode = f'/BrainGenix/API/Connections/{cryptogen.randrange(38564328964397256432564372)}'
sZookeeper.ZookeeperConnection.create(ConnectionNode, ephemeral=True)


# Define Methods In API #
@API.get('/')
async def root():
    return {'message' : 'Congradulations, You\'ve successfully installed the BrainGenix Management API Backend! Now, go and set up your front end to match your backend configuration parameters.'}

@API.get('/RandomNumberTest')
async def RandomNumberTest():
    return {'message' : random.randint(0,100)}

@API.get('/test')
async def test():

    sZookeeper.ZookeeperConnection.set(ConnectionNode, b'{"CallStack": "Version", "KeywordArgs": {}}')

    while sZookeeper.ZookeeperConnection.get(ConnectionNode)[0] == b'{"CallStack": "Version", "KeywordArgs": {}}':
        pass


    return json.loads(sZookeeper.ZookeeperConnection.get(ConnectionNode)[0].decode())


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