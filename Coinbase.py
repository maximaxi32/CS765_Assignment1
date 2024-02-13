import hashlib

class Block:
    def __init__(self, previous_hash, data):
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.previous_hash) + str(self.data) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block mined:", self.hash)

# Example usage
block = Block("0", "Hello, world!")
block.mine_block(4)
