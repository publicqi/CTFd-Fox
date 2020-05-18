from web3 import Web3, HTTPProvider
infura_api = ""

def verify(address, assigned_content, txn_addr):
    w3 = Web3(HTTPProvider(infura_api))
    func_header = 'leaveMsg(string)'

    txn_receipt = w3.eth.getTransactionReceipt(txn_addr)
    if txn_receipt['to'] != address:
        return False
    if txn_receipt['status'] == 0:  # maybe reverted
        return False
    else:
        txn = w3.eth.getTransaction(txn_addr)
        hash_func_header = w3.toHex(w3.keccak(text=func_header)[:4])
        assigned_content = w3.toHex(assigned_content.encode())[2:]
        return assigned_content in txn['input'] and txn['input'][:10] == hash_func_header
