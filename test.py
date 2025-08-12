from web3 import Web3
from eth_account import Account

NODEKEY_PATH = 'script/cn/data/klay/nodekey'
RPC_URL = 'http://localhost:8551'

def main():
    with open(NODEKEY_PATH, 'r') as f:
        prv_hex = f.read().strip()

    address = Account.from_key(prv_hex).address
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    balance_wei = w3.eth.get_balance(address)
    required_wei = 10 * 10**18

    print(f'Auction node address: {address}')
    print(f'Balance: {balance_wei} peb ({balance_wei/10**18:.6f} KAIA)')
    print('Auction condition: ' + ('OK (>= 10 KAIA)' if balance_wei >= required_wei else 'NG (< 10 KAIA)'))

if __name__ == '__main__':
    main()


