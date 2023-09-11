from web3 import Web3
import requests
import json
# from exchange_amount import exchange_amount

# 初始化 web3 对象
w3 = Web3(Web3.HTTPProvider('https://zksync-mainnet.s.chainbase.online/v1/2UyFSMi7W9Q5r9HF1BnO5pve5jc'))

# 定义合约地址和 ABI
zkSync_SpokePool_address: str = '0xE0B015E54d54fc84a6cB9B666099c46adE9335FF'

# 你可以从 Etherscan 或其他源获取 ABI
zkSync_SpokePool_abi = []
zkSync_SpokePool = w3.eth.contract(address=zkSync_SpokePool_address, abi=zkSync_SpokePool_abi)

# 定义交易参数
transaction_date = {
    'from': 'useraddress',
    'value': w3.to_wei(1, 'ether'),  # 存款金额
    'gas': 2000000,
    'gasPrice': w3.to_wei('30', 'gwei'),
}

# 从 API 获取 QUOTE_TIMESTAMP 和 RELAYER_FEE_PCT
response = requests.get('https://across.to/api/suggested-fees?token=0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91&destinationChainId=10&amount=1000000000000000')
data = json.loads(response.text)
uint32_value_here = data['timestamp']
uint64_value_here = data['relayFeePct']
relayFeePct_uint64 = uint64_value_here
timestamp_uint32 = uint32_value_here
amount = 10000000000000000
amount_uint256 = amount
chainID = 10
chainID_uint256 = chainID
maxCount = 1
maxCount_uint256 = maxCount

# 从 exchange_amount.txt 文件中读取 AMOUNT
with open(r'F:\web3\Interactive_plan\exchange_amount.txt', 'r') as f:
    exchange_amount = int(f.read().strip())

# 定义 deposit 函数的参数
params = [f'deposit(useraddress, 0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91, {amount_uint256}, {chainID_uint256}, {relayFeePct_uint64}, {timestamp_uint32}, b"", {maxCount_uint256})']

private_key = "userPrivate"

# 构造交易
transaction = zkSync_SpokePool.functions.deposit(*params).build_transaction(transaction_date)

# 签署交易
signed_txn = w3.eth.account.signTransaction(transaction, private_key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# 等待交易被挖出
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print(f"交易哈希: {txn_receipt}")
