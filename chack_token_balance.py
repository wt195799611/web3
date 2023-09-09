# 修复以下这段代码中的错误，这段代码中的第32行输出结果只有token_name和继续执行，这是错误的，遗漏了当前余额等信息
from web3 import Web3
import time

def get_token_name(w3, token_contract_address):
    name_method_id = w3.keccak(text="name()").hex()[0:10]
    token_name_hex = w3.eth.call({"to": token_contract_address, "data": name_method_id})
    token_name = token_name_hex.decode('utf-8').rstrip('\x00')

    return token_name


def check_token_balance(w3, token_contract_address, user_address, required_amount):
    token_name = get_token_name(w3, token_contract_address)
    balance_of_method_id = w3.keccak(text="balanceOf(address)").hex()[0:10]
    call_data = balance_of_method_id + "0" * 24 + user_address[2:]
    balance_hex = w3.eth.call({"to": token_contract_address, "data": call_data})
    balance_wei = int(balance_hex.hex(), 16)
    required_amount_wei = required_amount * 1e18

    while balance_wei < required_amount_wei:
        balance_str = "{:.5f}".format(balance_wei / 1e18)
        required_amount_str = "{:.6f}".format(required_amount_wei / 1e18)
        print(f"当前余额 {balance_str} {token_name} 小于所需金额 {required_amount_str} {token_name}, 等待5秒后重新检查...")
        time.sleep(5)
        balance_hex = w3.eth.call({"to": token_contract_address, "data": call_data})
        balance_wei = int(balance_hex.hex(), 16)

    # 注意：这里重新计算了 balance_str 和 required_amount_str
    balance_str = "{:.5f}".format(balance_wei / 1e18)
    required_amount_str = "{:.6f}".format(required_amount_wei / 1e18)
    print(f"当前余额 {balance_str} {token_name} 大于或等于所需金额 {required_amount_str} {token_name}, 继续执行...")

    return True

