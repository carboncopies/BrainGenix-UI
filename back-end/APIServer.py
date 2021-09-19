
###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

'''
Name: API Server
Description: This is the file used by the BrainGenix API System to get the server to communicate with the leader. This is run standalone due to issues with IP addresses changing based on the currently elected leader zookeeper node.
Date-Created: 2021-03-03
'''

import json
import uvicorn
import os
import secrets

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


from Core.Initialization.LoadConfig import LoadLocalConfig

from Core.ThreadManager import ThreadManager

from Core.Initialization.Instantiator import InstantiateLogger

from Core.VersionData import VersionNumber
from Core.VersionData import BranchVersion

from Core.BackendAPIClient.SocketClient import GetSocketClientConfig
from Core.BackendAPIClient.SocketClient import SocketClient

from Core.BackendAPIClient.Auth import AuthenticationManager

# Load Config #
SystemConfiguration = LoadLocalConfig(ConfigFilePath = 'Config.yaml')


# Start Uvicorn #
if __name__ == '__main__':

    # Launch UVICorn Instance #
    uvicorn.run(
        "APIServer:API",
        host=SystemConfiguration['APIServerAddress'],
        port=SystemConfiguration['APIServerPort'],
        log_level="info"
    )

    # Shutdown Server #
    os._exit(0)



##############################################################################
## NOTE: A Lowercase "m" Preceeding A Class Means It's a Main System        ##
## NOTE: A Lowercase "s" Preceeding A Class Means It's a Subsystem          ##
##############################################################################



# Set Version Information
Version = VersionNumber
Branch = BranchVersion


# Initialize Logger #
mLogger = InstantiateLogger(SystemConfiguration)


# Instantiate Thread Manager #
mThreadManagerInstance = ThreadManager(mLogger)


# Connect To Zookeeper Service #
sZookeeper = mThreadManagerInstance.InstantiateZK(mLogger, SystemConfiguration)


# Get Socket Client Config #
SocketClientConfig = GetSocketClientConfig(mLogger, sZookeeper, SystemConfiguration)


# Connect To NES Server #
sNESSocketConnection = SocketClient(mLogger, SocketClientConfig)
sNESSocketConnection.BenchmarkConnection()


# Instantiate Auth Manager #
sAuthenticationManager = AuthenticationManager(mLogger, SystemConfiguration)


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

# Add a new user #
@API.post('/AddUser')
async def mAPI_CreateUser(RequestJSON: Request): # Create User Statemenet #

    try:

        # Decode Incoming JSON #
        RequestBytes = await RequestJSON.body()
        APIArgs = json.loads(RequestBytes.decode())
        print(APIArgs)
        # Get User Info #
        UserName = APIArgs['Username']
        Password = APIArgs['Password']
        FirstName = APIArgs['FirstName']
        LastName = APIArgs['LastName']
        Notes = APIArgs['Notes']
        PermissionLevel = APIArgs['PermissionLevel']

        # Create Salt Token #
        Salt = secrets.token_urlsafe(65535)

        # Add User To DB #
        sNESSocketConnection.addUser(UserName, Password, Salt, FirstName, LastName, Notes, int(PermissionLevel))

        # Acknowledge Add User Success #
        return {'Acknowledgement' : 'Add User Success'}

    except Exception as e:
        print(e)
        
        
# Authentication #
@API.post('/Authenticate')
async def Authentication(RequestJSON: Request):

    try:

        # Decode Incoming JSON #
        RequestBytes = await RequestJSON.body()
        CommandScope = json.loads(RequestBytes.decode())

        print(CommandScope)

        # Get Uname, Passwd #
        Username = CommandScope['Username']
        Password = CommandScope['Password']

        # Check Uname, Passwd #
        if sNESSocketConnection.WriteAuthentication(Username,Password):

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
mLogger.Log('\x1b[38;2;0;128;55m██████╗ ██████╗  █████╗ ██╗███╗   ██╗\x1b[38;2;130;68;208m ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗', 5)
mLogger.Log('\x1b[38;2;0;128;55m██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║\x1b[38;2;130;68;208m██╔════╝ ██╔════╝████╗  ██║██║╚██╗██╔╝', 5)
mLogger.Log('\x1b[38;2;0;128;55m██████╔╝██████╔╝███████║██║██╔██╗ ██║\x1b[38;2;130;68;208m██║  ███╗█████╗  ██╔██╗ ██║██║ ╚███╔╝ ', 5)
mLogger.Log('\x1b[38;2;0;128;55m██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║\x1b[38;2;130;68;208m██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ ', 5)
mLogger.Log('\x1b[38;2;0;128;55m██████╔╝██║  ██║██║  ██║██║██║ ╚████║\x1b[38;2;130;68;208m╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗', 5)
mLogger.Log('\x1b[38;2;0;128;55m╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝\x1b[38;2;130;68;208m ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝', 5)
mLogger.Log('---------------------------------------------------------------------------')
mLogger.Log('')
mLogger.Log('    +-----------------------------------------------------------------+')
mLogger.Log(f'    |          Welcome To BrainGenix-APIServer Version {Version}-{Branch}      |')
mLogger.Log('    +-----------------------------------------------------------------+')
mLogger.Log('')
