import requests
from communication_with_db import update_transactionID_in_db, update_transactionSTATUS_in_db
from communication_with_db import local_session, Future_Transactions, filter_trans_by_date


def transaction_manager():
    today_transactions = filter_trans_by_date()
    print('*************************')
    print('Today performed transactions ID: ')

    for trans in today_transactions:
        check_for_new_transactions = local_session.query(Future_Transactions).filter_by(id=trans[0]).first()
        if check_for_new_transactions.transaction_id == 0:
            transaction_id = perform_transaction(trans[1], trans[2], trans[3], trans[4])
            update_transactionID_in_db(trans[0], transaction_id)
            print(transaction_id)
    report = download_report()

    print('*************************')
    print('Transaction Report from the last 5 days:')
    for key, value in report.items():
        print(key, ' : ', value)
    print('END OF REPORT')
    print('*************************')
    for key, value in report.items():
        update_transactionSTATUS_in_db(key, value)
    print('Thank you, hope to see you soon!')
    return report

def perform_transaction(src_bank_account, dst_bank_account, amount, direction):
    URL = "http://localhost:5050/perform_transaction"
    PARAMS = {'src_bank_account': src_bank_account, 'dst_bank_account': dst_bank_account, 'amount': amount, 'direction': direction}
    r = requests.post(url=URL, data=PARAMS)
    data = r.json()
    return data

def download_report():
    URL = "http://localhost:5050/download_report"
    r = requests.get(url=URL)
    return r.json()

