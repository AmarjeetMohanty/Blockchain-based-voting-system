import hashlib
import json
import time
import random


class Block:
    def __init__(self,index,timestamp,transactions,previousHash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        transactions = self.transactions

        for transaction in self.transactions:
            if (type (transaction)) != dict:
                newTran = transaction.__dict__
                transactions.append(newTran)
                self.transactions.remove(transaction)
        self.transactions = transactions
        block_string = json.dumps(self.__dict__, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    

    def mineblock(self,difficulty):
        if self.hash[:difficulty] != 0:
            self.nonce += 1
            self.hash = self.calculateHash()


class Transaction:
    def __init__(self,sender,reciever,proposal):
        self.sender = sender
        self.reciever = reciever
        self.proposal = proposal 
        self.timestamp = time.time()

    def verifyTransaction(self):
        # Generate generator g and prime p
        g = 2
        p = 13

        # Generate random numbers a and b
        a = random.randint(1, p-1)
        b = random.randint(1, p-1)

        # Compute A and B
        A = pow(g, a, p)
        B = pow(g, b, p)

        # Send A and B to the other party
        # In this case, we assume that the sender is the prover and the receiver is the verifier
        verifier = self.receiver
        verifier.send_proof(A, B)

        # Compute A' and B'
        A_prime = verifier.receive_A_prime()
        B_prime = verifier.receive_B_prime()

        # Compute shared key K
        K = pow(B, a, p)
        K_prime = pow(A_prime, b, p)

        # Verify that K and K' are the same
        return K == K_prime
   

        

class Blockchain:
    def __init__(self):
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
                if transaction["reciever"] == proposal:
                    count += 1

        return count                            

    def view_user(self,address):
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address or transaction["reciever"] == address:
                    transactions.append(transaction)
        return transactions            




# Create an instance of the blockchain
blockchain = Blockchain()




proposals = ["a","b","c","d"]

for i in proposals:
    blockchain.add_proposal(i)

voters = ["manas","amlan","amarjeet","bilal","waleed","ayushman","jaskirat","tarun","ankit","shaantanu"]

for j in voters:
    blockchain.authenticate_user(j)

transactionHistory = dict.fromkeys(voters)
print(transactionHistory)


for j in voters:
    candidate = input("Enter your candidate: ")
    blockchain.vote(j,candidate)
    blockchain.mine_pending_transaction()
    transactionHistory[j] = blockchain.view_user(j)

for i in proposals:
    print(type(i))
    print("Vote count of "+i+" : "+str(blockchain.get_vote_count(i)))

for j in voters:
    print("Transaction for "+j+" : "+str(transactionHistory[j]))

