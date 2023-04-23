import hashlib
import json
import time
import random
from createprime import generate_prime

class Block:
    def __init__(self,index,timestamp,transactions,previousHash):
        """
        Initializing the contructor of the block with 4 parameters:-
        -index
        -timestamp
        -transactions
        -previousHash
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        """
        Calculating the unique hash of the Block that can be used  to keep track of the Block.
        It uses the haslib library 
        """
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
        """
        Mining the vote after it has been cast by calling the calculateHash function and 
        making sure that the user can only vote once
        """
        if self.hash[:difficulty] != 0:
            self.nonce += 1
            self.hash = self.calculateHash()


class Transaction:
    def __init__(self,sender,receiver,proposal):
        """
        Initializing the constructor of the Transaction class with 3 parameters:-
        -sender ie the voter
        -reciever ie the candidate who recieves the vote
        -proposal ie the index value of the candidate
        """
        self.sender = sender
        self.receiver = receiver
        self.proposal = proposal 
        self.timestamp = time.time()

    def verifyTransaction(self):
        """
        This method is used to verify the vote cast by the user using Zero Knowledge Proof.
        It uses Diffie Hellman Key Exchange method . 
        """
        #agreed generator
        g = 3 
        #agreed prime number (ideally should be larger but  couldn't be due to computer constraint)
        p = generate_prime(32) 
        #random integer as private key from the reciver side
        a = random.randint(1,p-1)
        # public key generated using the private key
        A = pow(g,a,p)
        
        #instance of the new Verifier Class
        verifier = Verifier(g,p)
        verifier.createPublicKey()
        B = verifier.B
        K = verifier.createSharedKey(A)
        
        K_prime = pow(B,a,p)
        
        return K==K_prime
    
class Verifier:
    def __init__(self,g,p):
        """
        Verifier class constructor is initialized using the 2 parameter:
        -g (agreed upon generator value)
        -p (agreed upon n-bits prime number)
        """
        self.g = g
        self.p = p
        # random private key generated
        self.b = random.randint(1,p-1) 
        self.B = None   

    def createPublicKey(self):
        """
        Creates public key for the verifier class
        """
        self.B = pow(self.g,self.b,self.p)

    def createSharedKey(self,A):
        """
        Creates the Key required for verification
        """
        K = pow(A,self.b,self.p)
        return K

class Blockchain:
    def __init__(self):
        """
        Blockchain class constructor in iniliazed :
        -  Chain is created withe first block in it
        - difficulty is set to 2
        - an empty array of pending transaction is initialized
        - an empty array of candidates is initialized
        - an empty list of voters is initialized
        """
        self.chain = [self.create_first_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.proposals = []
        self.voters = {}

    def create_first_block(self):
        """ 
        The block of the blockchain is initialized with index 0, timestap, 
        no transaction and a hash value of zero
        """
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        """
        This method is used to get the details about the 
        latest Block that has been added to the blockchain
        """
        return self.chain[-1]

    def mine_pending_transaction(self):
        """
        This method is used to create and added the new block of the vote that has been cast
        """
        # new block with the relevant details are created
        new_block = Block(len(self.chain),time.time(),self.pending_transactions,self.get_latest_block().hash) 
        # the block is mined and its hash value is created
        new_block.mineblock(self.difficulty)
        #the block is added to the chain
        self.chain.append(new_block)
        #  the pending_transaction array is emptied
        self.pending_transactions = []

    def addTransaction(self,transaction):
        """
        This is to verify whether the transaction is authentic or not
        """
        if transaction.verifyTransaction()==True:
            print("Transaction Verified")
            self.pending_transactions.append(transaction)
        else:
            print("error")
    
    def add_proposal(self, proposal_name):
        """
        This method is used to add candidate that the candidates can vote from
        """
        self.proposals.append(proposal_name)

    def authenticate_user(self,address):
        """
        This method is used to authenticate the list of voters that are allowed to vote
        """
        self.voters[address] = True

    def vote(self,sender,reciever):
        """
        This method allows the user to vote , 
        it makes sure that both the user and the candidate are in their respective list,
        and it makes sue the voter hasn't already voted.
        """
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == sender:
                    print("Already voted")
                    return 
        if sender in self.voters and self.voters[sender]:
            # initial instance of teh Transaction class is created 
            transaction = Transaction(sender,reciever,self.proposals.index(reciever))
            # Transaction is added to the pending transaction array
            self.addTransaction(transaction)


    def get_vote_count(self,proposal):
        """
        Gets the amout of vote a certain candidate recieved
        """
        count = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction["receiver"] == proposal:
                    count += 1

        return count                            

    def view_user(self,address):
        
        """
        This method allows us to view transaction of the voter
        """
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address or transaction["receiver"] == address:
                    transactions.append(transaction)
        return transactions            




# Create an instance of the blockchain
blockchain = Blockchain()


# this is the list of candidates
proposals = ["a","b","c","d"]
# candidates are added
for i in proposals:
    blockchain.add_proposal(i)

# thsi is the list of voters
voters = ["aa","bb","cc","dd","ee","ff","gg","hh","ii","jj"]
# the voters are authenticated
for j in voters:
    blockchain.authenticate_user(j)

transactionHistory = dict.fromkeys(voters)


for j in voters:
    candidate = input("Enter your candidate "+j+":")
    # the voters vote is cast
    blockchain.vote(j,candidate)
    # The vote is mined
    blockchain.mine_pending_transaction()
    # the transaction is added to transaction history
    transactionHistory[j] = blockchain.view_user(j)
    # The transaction is seen using view user method
    print("Transaction for "+j+" : "+str(transactionHistory[j]))

for  i in proposals:
    print("The candidate "+i+" has recieved: "+str(blockchain.get_vote_count(i)))












