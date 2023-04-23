Python Voting System Implementation

The code is an implementation of a blockchain-based voting system. It consists of three classes: `Block`, `Transaction`, and `Blockchain`. 

The `Block` class has five attributes: `index`, `timestamp`, `transactions`, `previousHash`, and `nonce`. The class has three methods: `__init__()`, which initializes the block object with the given attributes, `calculateHash()`, which calculates the hash of the block by converting the object into a JSON string and hashing it using the SHA256 algorithm, and `mineblock()`, which mines the block by incrementing the `nonce` attribute and recalculating the hash until the hash starts with `difficulty` number of zeros.

The `Transaction` class has four attributes: `sender`, `receiver`, `proposal`, and `timestamp`. The class has one method: `verifyTransaction()`, which verifies the transaction using the Diffie-Hellman key exchange method.

The `Blockchain` class has five attributes: `chain`, `difficulty`, `pending_transactions`, `proposals`, and `voters`. The class has six methods: `__init__()`, which initializes the blockchain with an empty chain, sets the difficulty level, and initializes empty arrays for pending transactions, proposals, and voters, `create_first_block()`, which creates the first block with a hash of zero, `get_latest_block()`, which returns the latest block in the chain, `mine_pending_transaction()`, which mines a block for the pending transactions, `addTransaction()`, which adds a transaction to the pending transactions array after verifying it, and `add_proposal()`, which adds a new proposal to the proposals array.

We have already initialized a blockhain and added a list of cadidates and and voters .Upon running the code each voter will be asked for his vote and after voting the vote is mined and then verified and added to the blockchain. The transaction details are then shown for each user. At the end of the voting process each candidates' vote count is shown.

This project is made by:-
1)Amarjeet Mohanty
2)Ayushman Kar
3)Shashwat Bajpai
4)P Sarvesh Kumar
5)Bhargav Nutalapati