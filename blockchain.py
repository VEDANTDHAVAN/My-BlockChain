
"""
GENESIS BLOCK    //to kickstart the BlockChain
{
  index: 0,
  timestamp: current Time,
  data: "fryetyhughpegfb",
  proof: 3,
  previous_hash: "0"
} -> hash() -> 2343aaa//hash value

{
  index: 1,
  timestamp: current Time,
  data: "fuuirhbkfn",
  proof: 23485,
  previous_hash: 2343aaa
} -> hash() -> 9876ffe

{
  index: 2,
  timestamp: current Time,
  data: "afyesiugyr",
  proof: 94800948,
  previous_hash: 9876ffe
} -> hash() -> 8909ggk
"""
import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:

    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self._create_block(
            data="I am the Genesis Block",
            proof=1, 
            prev_hash= "0", 
            index=1
            )
        self.chain.append(genesis_block)
    
    def mine_block(self, data: str) -> dict:
        prev_block = self.get_previous_block()
        prev_proof = prev_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(prev_proof, index, data)
        prev_hash = self._hash(block= prev_block)
        block = self._create_block(
            data=data, 
            prev_hash=prev_hash, 
            proof=proof, 
            index=index)
        self.chain.append(block)
        return block

    def _hash(self, block: dict) -> str:
        """
        Hash a block and return the cryptographic hash of the block
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()

        return _hashlib.sha512(encoded_block).hexdigest()

    def _to_digest(self, new_proof: int, prev_proof: int, index: str, data: str) -> bytes:
        to_digest = str(new_proof **3 - prev_proof **3 + index) + data
        return to_digest.encode()

    def _proof_of_work(self, prev_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            
            to_digest = self._to_digest(
                new_proof= new_proof,
                prev_proof= prev_proof, 
                index=index, 
                data=data
                )
            hash_value = _hashlib.sha256(to_digest).hexdigest()

            if hash_value[:4] == "0000":
               check_proof = True
            else:
                new_proof += 1
        
        return new_proof

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _create_block(self, data: str, proof: int, prev_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "prev_hash": prev_hash,
        }
        
        return block
    
    def is_chain_valid(self) -> bool:
        current_block = self.chain[0]
        block_index = 1 

        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block["prev_hash"] != self._hash(current_block):
                return False
            
            current_proof = current_block["proof"]
            next_index, next_data, next_proof = (
                next_block["index"], 
                next_block["data"], 
                next_block["proof"],
                )
            hash_value = _hashlib.sha256(
                self._to_digest(
                    new_proof=next_proof, 
                    prev_proof= current_proof, 
                    index=next_index, 
                    data=next_data,
                    )
            ).hexdigest()

            if hash_value[:4] != "0000":
                return False
            
            current_block = next_block
            block_index += 1

        return True

