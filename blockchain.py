import hashlib
import json
import time
import random


class Block:
    def _init_(self,index,timestamp,transactions,previousHash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        block_string = json.dumps(self._dict_, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mineblock(self,difficulty):
        while self.hash[:difficulty] != 0:
            self.nonce += 1
            self.calculateHash()

import hashlib
import json
import random

class Transaction:
    def _init_(self,sender,receiver,proposal):
        self.sender = sender
        self.receiver = receiver
        self.proposal = proposal 
        self.timestamp = time.time()

    def verifyTransaction(self):
        # Generate random secret number k
        k = random.randint(1, 2**256 - 1)
        
        # Calculate point R on the elliptic curve secp256k1
        G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
             0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
        a = -3
        p = 2*256 - 232 - 29 - 28 - 27 - 26 - 2*4 - 1
        b = 0x7E73D3A88DAA3F55FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        secp256k1 = (a, b, p, G)
        R = self.scalar_multiply(secp256k1, k, G)
        
        # Calculate challenge value e and signature value s
        m = hashlib.sha256(
            json.dumps(
                {"sender": self.sender, "receiver": self.receiver, "proposal": self.proposal},
                sort_keys=True,
            ).encode()
        ).digest()
        e = int.from_bytes(hashlib.sha256(self.point_to_bytes(R) + m).digest(), "big")
        d = int.from_bytes(hashlib.sha256(self.sender.encode()).digest(), "big")
        s = pow(k + e * d, p-2, p) * (e + d * R[0]) % p
        
        # Verify that the signature is valid
        if s == 0:
            return False
        P = self.scalar_multiply(secp256k1, d, G)
        Q = self.point_add(secp256k1, self.scalar_multiply(secp256k1, e, G), self.scalar_multiply(secp256k1, s, P))
        return R == Q
    
    def scalar_multiply(self, curve, k, P):
        a, b, p, G = curve
        Q = None
        while k > 0:
            if k % 2 == 1:
                Q = self.point_add(curve, Q, P)
            P = self.point_add(curve, P, P)
            k //= 2
        return Q
    
    def point_add(self, curve, P, Q):
        a, b, p, G = curve
        if P is None:
            return Q
        if Q is None:
            return P
        if P == Q:
            return self.point_double(curve, P)
        if P[0] == Q[0]:
            return None
        s = ((Q[1]-P[1]) * pow(Q[0]-P[0], p-2, p)) % p
        x = (s**2 - P[0] - Q[0]) % p
        y = (s*(P[0]-x) - P[1]) % p
        return (x, y)
    
    def point_double(self, curve, P):
        a, b, p, G = curve
        if P is None:
            return None
        s = ((3 * P[0]**2 + a) * pow(2 * P[1], p-2, p)) % p
        x = (s**2 - 2 * P[0]) % p
        y = (s * (P[0] - x) - P[1]) % p
        return (x, y)
    def point_to_bytes(self, P):
    # This method encodes a point on the elliptic curve to bytes.
    # We assume that the point is a tuple of two integers (x, y).
        x_bytes = P[0].to_bytes(32, byteorder="big")
        y_bytes = P[1].to_bytes(32, byteorder="big")
        return x_bytes + y_bytes
    
   

        

class Blockchain:
    def _init_(self):
        self.chain = [self.create_first_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.proposals = []
        self.voters = {}

    def create_first_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transaction(self):
        new_block = Block(len(self.chain),time.time(),self.pending_transactions,self.get_latest_block().hash)
        new_block.mineblock(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []

    def addTransaction(self,transaction):
        if transaction.verifyTransaction():
            self.pending_transactions.append(transaction)
    
    def add_proposal(self, proposal_name):
        self.proposals.append(proposal_name)

    def authenticate_user(self,address):
        self.voters[address] = True

    def vote(self,sender,reciever):
        if sender in self.voters and self.voters[sender]:
            transaction = Transaction(sender,reciever,self.proposals.index(reciever))
            self.addTransaction(transaction)

    def get_vote_count(self,proposal):
        count = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.proposal == proposal:
                    count += 1
        return count                            

    def view_user(self,address):
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address or transaction.reciever == address:
                    transactions.append(transaction._dict_)
        return transactions            




# Create a new blockchain
my_blockchain = Blockchain()

# Add a proposal to the blockchain
my_blockchain.add_proposal("Proposal 1")
# print(len(my_blockchain.proposal_name))
# Add two users and authenticate them
user1 = "address1"
user2 = "address2"
user3 = "address3"
my_blockchain.authenticate_user(user1)
my_blockchain.authenticate_user(user2)
my_blockchain.authenticate_user(user3)
print(my_blockchain.voters)

my_blockchain.vote(user1, "Proposal 1")
my_blockchain.mine_pending_transaction()
print(my_blockchain.get_vote_count("Proposal 1"))

# # User2 votes for Proposal 1
# my_blockchain.vote(user2, "Proposal 1")

# # Get the current vote count for Proposal 1
# vote_count = my_blockchain.get_vote_count("Proposal 1")
# print("Current vote count for Proposal 1:", vote_count)

# # View all transactions for User1
# user1_transactions = my_blockchain.view_user(user1)
# print("User1 transactions:", user1_transactions)

# # View all transactions for User2
# user2_transactions = my_blockchain.view_user(user2)
# print("User2 transactions:", user2_transactions)