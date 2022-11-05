import requests

def main():
    print('Welcome to Perform advanced transaction')
    print('please, insert source bank account:')
    src_bank = input()
    print('please, insert destination bank account:')
    dst_bank = input()
    print('please, insert amount:')
    amount = input()
    if int(amount) <= 0:
        print('invalid amount, please insert number bigger then 0 ')
        amount = input()
    perform_advance(src_bank, dst_bank, amount)


def perform_advance(src_bank_account, dst_bank_account, amount):
    URL = "http://localhost:5051/perform_advance"
    PARAMS = {'src_bank_account': src_bank_account, 'dst_bank_account': dst_bank_account, 'amount': amount}
    r = requests.post(url=URL, data=PARAMS)
    data = r.json()
    print(data)
    return data


if __name__ == '__main__':
    main()
