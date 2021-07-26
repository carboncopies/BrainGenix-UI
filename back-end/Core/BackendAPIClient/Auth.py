
###########################################################
## This file is part of the BrainGenix Simulation System ##
###########################################################

import secrets
import time

# from requests.models import Response


'''
Name: Auth
Description: This subsystem is used to handle system authentication for the API Server.
Date-Created: 2021-03-03
'''

class AuthenticationManager(): # Handles Auth for API #

    def __init__(self, Logger, DBInfo): # Initialization #

        # Store Logger #
        self.Logger = Logger

        self.Logger.Log('Initializing mAPI Authentication Manager')

        # Store DB Creds #
        # pass # Skip this for now

        # Create Token Dict #
        self.Tokens = {}

        # Note, we're going to have two types of authentication tokens. Both are Long, (8192 or more chars), however, one is a short term token, and it expires after a set amount of time on the server side.
        # The Long type of token lasts indefinately, and is for API Integrations.
        # Do we store tokens locally or in the db? if db then we should make a tokens table


        # Log Init Done #
        self.Logger.Log('Authentication Manager Initialization Complete')


    def ValidateToken(self, Token): # Checks If A Token Is Valid #

        # Check Token #
        try:
            # AssociatedUsername = self.Tokens[Token]['Username']
            TokenExpireDate = self.Tokens[Token]['ExpireTime']

            # Check If Token Expired #
            if time.time() > TokenExpireDate:
                Response = 'Expired Token'
            
            # Valid Token #
            else:
                Response = 'Valid Token'

        except KeyError:
            Response = 'Invalid Token'

        # Return Bool #
        return Response


    def GenerateToken(self, AssociatedUsername, TokenLifetime=3600, TokenExpires=True, SaveToken=False, TokenLength=512): # Generate A New Token For Auth #

        # Log Token Creation #
        self.Logger.Log(f'Creating Token With Following Params For Username: {AssociatedUsername}', 5)
        self.Logger.Log(f'Token Lifetime: {TokenLifetime}')
        self.Logger.Log(f'Token Expires: {TokenExpires}')
        self.Logger.Log(f'Token Persistent: {SaveToken}')
        self.Logger.Log(f'Token Length: {TokenLength}')
        
        # Generate Random String #
        Token = secrets.token_urlsafe(TokenLength)

        # Set Token Metadata #
        ExpireTime = time.time() + TokenLifetime

        # Set Token Metadata #
        Metadata = {
            'ExpireTime' : ExpireTime,
            'TokenExpires' : TokenExpires,
            'SaveToken' : SaveToken,
            'Username' : AssociatedUsername
            }

        # Save Token #
        # pass
        # pass # FILL THIS IN LATER!!!!!
        # pass

        # Add To Token Dict #
        self.Tokens.update({Token : Metadata})

        # Log Completion #
        self.Logger.Log('Generated Token')

        # Return Token #
        return Token
