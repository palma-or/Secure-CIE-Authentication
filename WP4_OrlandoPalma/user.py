import os
import shutil
import math
import subprocess
import ast
import time

from server import Server


class User():

    """
    This class represents a user.
    """

    __slots__ = '_ecdsaKeyFile', '_ecdsaPubFile', '_ecdsaParamFile', '_IP', '_server', '_tlsHandler', '_greenPass', '_otp', '_keyManagement', '_folderName'

    def __init__(self, IP):
        """
        Initialize the user with the given IP address.

        Args:
            IP (str): The IP address of the user.
        """
        self._IP = IP
        self._folderName = "User_" + self._IP
        self._server = None
  

        


    def connect(self, server):
        """
        Connect the user to the given server.

        Args:
            server (Server): The server to connect to.
        
        Raises:
            TypeError: If server is not an instance of Server.
        """
        if not isinstance(server, Server):
            print('[User {}]: '.format(self), 'invalid server')
            return -1
        
        self._server = server
        print('[User {}]: '.format(self), 'connecting to {}...'.format(server))
        time.sleep(1)
        self._server.startConnection(self) 

        # TLS handshake 
        print('\n[User {}]: '.format(self), 'starting TLS handshake...')
        time.sleep(1)
        self._tlsHandler = TLSClientHandler(self, self._folderName, self._server) # da definire
        self._tlsHandler.handshakeStep(1) 
    
    def closeConnection(self):
        """
        Close the connection with the server.
        """
        self._server.closeConnection(self)
        self._server = None
        self._tlsHandler = None
        self._otp = None
    
    


class Citizen(User):

    """
    This class represents a citizen.
    """

    def __init__(self, IP):
        """
        Initialize the player with the given IP address.

        Args:
            IP (str): The IP address of the player.
        """
        super().__init__(IP)
    
    def sendInitialInformation(self):
        """
        Send the initial information to the server. In particular, the public key of the user 
        """
        
    
    def identificationScheme(self):
        """
        Execute the identification scheme with the server.
        """
        print('\n[User {}]: '.format(self), 'starting identification...')
        time.sleep(1)
        bytes_q = math.ceil((math.log2(abs(self._tlsHandler.q) + 1)) / 8)
        com = ['openssl', 'rand', str(bytes_q)]
        self.r = int.from_bytes(subprocess.check_output(com), byteorder='big')
        a = pow(self._tlsHandler.g, self.r, self._tlsHandler.p)
        
        message = (pow(self._tlsHandler.g, self._tlsHandler.x, self._tlsHandler.p), a)
        encryptedMessage, tagMac, iv = self._tlsHandler.encryptMessage(message)
        return self._server.identificationSchemeStep1({'message': encryptedMessage, 'tagMac': tagMac, 'iv': iv}, self)

    def identificationSchemeStep2(self, params):
        """
        Execute the second step of the identification scheme with the server.

        Args:
            params (dict): The dictionary containing the encrypted message, the tagMac and the iv.
        """
        if params is not None:
            message = self._tlsHandler.decryptMessage(params['message'], params['tagMac'], params['iv'])
            z = self.r + ast.literal_eval(message) * self._tlsHandler.x
            encryptedMessage, tagMac, iv = self._tlsHandler.encryptMessage(z)
            self._server.identificationSchemeStep2({'message': encryptedMessage, 'tagMac': tagMac, 'iv': iv}, self)

    
    