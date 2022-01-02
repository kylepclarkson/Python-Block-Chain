import hashlib
import random
import string
import json
import binascii
# import numpy as np
# import pandas as pd
# import pylab as pl
import logging
import datetime
import collections

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Client:
    """ A user of the system. """
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
    
    @property
    def identity(self):
        """ Return hexidecimal representation of this client. """
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


class Transaction:
    """ A transaction between two users of the system. """
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        """ A dictionary representation of the transaction. """
        
        identity = "GENISIS" if self.sender == "GENISIS" else self.sender.identity
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time })

    def sign_transaction(self):
        """ Have the sender sign the transaction using their private key. """
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    def print_transaction(self):
        """ Display contents of transaction. """
        print(f"Sender: {self.sender}")
        print(f"Recipient: {self.recipient}")
        print(f"Value: {self.value}")
        print(f"Time: {self.time}")
        print("========================================================================")


last_blonk_hash = ""
class Block:

    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""