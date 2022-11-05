import schedule
from flask import Flask
from flask import request
from communication_with_db import insert_payments_into_db, Future_Transactions, Advanced_Transactions, local_session
from transaction_manager import transaction_manager

app = Flask(__name__)


@app.route("/perform_advance", methods=['POST'])
def perform_advance():
    print('received')
    src_bank_account = request.form['src_bank_account']
    dst_bank_account = request.form['dst_bank_account']
    amount = request.form['amount']
    insert_payments_into_db(int(src_bank_account), int(dst_bank_account), int(amount), number_of_payments=12)

    # schedule.every().day.at("23:59").do(transaction_manager())    # PERFORM ONCE A DAY AT MIDNIGHT

    report = transaction_manager()

    return report


if __name__ == "__main__":
    app.run(debug=True, port=5051)
