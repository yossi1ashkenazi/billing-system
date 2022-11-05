import random
from flask import Flask
from flask import request
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, create_engine, Boolean, MetaData
from db import TransactionReport
from datetime import timedelta, datetime

app = Flask(__name__)

engine = create_engine("postgresql://postgres:075151@localhost:5432/Processor")
Session = sessionmaker()
local_session = Session(bind=engine)


@app.route("/perform_transaction", methods=['POST'])
def perform_transaction():
    src_bank_account = request.form['src_bank_account']
    dst_bank_account = request.form['dst_bank_account']
    amount = request.form['amount']
    direction = request.form['direction']
    print(src_bank_account, dst_bank_account, amount, direction)

    random_transaction_id = random.randint(10000, 99999)
    print("perform transaction number:" + str(random_transaction_id))
    random_status = random.choice([True, False])
    if random_status:
        _status = 'success'
    else:
        _status = 'fail'

    r = TransactionReport(trans_id=random_transaction_id, trans_date=datetime.today().date(), status=_status)
    local_session.add(r)
    local_session.commit()
    return str(random_transaction_id)


@app.route("/download_report")
def download_report():
    filter_after = datetime.today() - timedelta(days=5)

    all_trans = local_session.query(TransactionReport) \
        .filter(TransactionReport.trans_date >= filter_after) \
        .all()

    results = {}
    for t in all_trans:
        results[t.trans_id] = t.status

    print(results)
    return results


if __name__ == "__main__":
    app.run(debug=True, port=5050)
