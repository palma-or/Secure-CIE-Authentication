import os
import subprocess
import datetime
import math
import ast
import time 



class Server():

    def __init__(self, IP):
        """
        Constructor of the Server class.
        
        Args:
            IP (str): IP address of the server
        """
        self._connections = {}
        self._IP = IP
        self._folderName = "Server_" + self._IP
        self._tlsHandler = TLSServerHandler(self, self._folderName)
        self._keyManagement = KeyManagement()
        self._generateKey()

    def _generateKey(self):
        """
        Generate the ECDSA key pair.
        """
        self._ecdsaKeyFile = self._folderName + '/ecdsa_key.pem'
        self._ecdsaPubFile = self._folderName + '/ecdsa_pub.pem'
        self._ecdsaParamFile = self._folderName + '/prime256v1.pem'
        if not os.path.exists(self._folderName):
            os.mkdir(self._folderName)
            self._keyManagement.generateKey(self._ecdsaParamFile, self._ecdsaKeyFile, self._ecdsaPubFile)

    def startConnection(self, user):
        """
        Start a new connection with the client.
        
        Args:
            user (User): user object
        """
        print('[Server {}]: '.format(self), 'new connection from {}'.format(user))
        self._connections[user] = None 
    
    def closeConnection(self, user):
        """
        Close the connection with the client.

        Args:
            user (User): user object
        """
        print('[Server {}]: '.format(self), 'closing connection with {}...'.format(user))
        time.sleep(1)
        del self._connections[user]
        del self._tlsHandler._connections[user]
        print('[Server {}]: '.format(self), 'connection closed')
    
    @property
    def tlsHandler(self):
        """
        Getter of the TLS handler object.
        """
        return self._tlsHandler
    
    @property
    def connections(self):
        """
        Getter of the active connections dictionary.
        """
        return self._connections

    
class ServerAuthority(Server):

    """
    Class that extends the Server class. It represents the server of the Authority.

    """

    __slots__ = '_internalDB'
    def __init__(self, IP):
    
        super().__init__(IP)
        self._internalDB = Database()
        self._otp = {}
    
    


class ServerService(Server):

    """
    Class that extends the Server class. It represents the server of digital services.

   """

   
    def __init__(self, IP):
        """
        Constructor of the ServerMJ class.

        Args:
            IP (str): IP address of the server
        """
        super().__init__(IP)

    def receiveInitialInformation(self, params, user):
        """
        Receive the initial information from the client in order to verify that the green pass is valid e has not been revoked.

        Args:
            params (dict): dictionary of the parameters
            user (User): user object
        """
        if user not in self._connections:
            print('[Server {}]: '.format(self), 'user not found')
            self.closeConnection(user)
            return
        
        message = self._tlsHandler.decryptMessage(params['message'], params['tagMac'], params['iv'], user)
        message = ast.literal_eval(message)
        pubkey, pubkeyProof = message[0], message[1]
        v_ci, v_ciProof = message[2], message[3]
       
        self.closeConnection(user)
        return

    def identificationSchemeStep1():
    
    def identificationSchemeStep2():
    
    def _verifyPolicy():
        
    def __str__(self) -> str:
        """
        Return the string representation of the user.
        """
        return 'Service'