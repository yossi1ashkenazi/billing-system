from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, create_engine, MetaData, Boolean
import os
from datetime import timedelta, datetime
import datetime

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
Base = declarative_base()
engine = create_engine("postgresql://postgres:075151@localhost:5432/Payment System")
Session = sessionmaker()
local_session = Session(bind=engine)


class Future_Transactions(Base):
    __tablename__ = 'future_transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    a_id = Column(Integer, primary_key=False)
    trans_date = Column(DateTime, nullable=False)
    amount = Column(Integer, primary_key=False)
    transaction_id = Column(Integer, primary_key=False)
    status = Column(String(25), primary_key=False)


class Advanced_Transactions(Base):
    __tablename__ = 'advanced_transactions'
    a_id = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(Integer, primary_key=False)
    dst = Column(Integer, primary_key=False)
    total_amount = Column(Integer, primary_key=False)
    last_transaction = Column(DateTime, primary_key=False)
    status = Column(String(25), primary_key=False)


def filter_trans_by_date():
    try:
        today_trans = local_session.query(Future_Transactions).filter_by(trans_date=datetime.date.today()).all()
        all_info_today_transactions = []
        for trans in today_trans:
            A_id = trans.a_id
            perent_trans = local_session.query(Advanced_Transactions).filter_by(a_id=A_id).first()
            transaction_info = (trans.id, perent_trans.src, perent_trans.dst, trans.amount, 'debit')
            all_info_today_transactions.append(transaction_info)

        return (all_info_today_transactions)


    finally:
        local_session.close()


def insert_payments_into_db(src, dst, total_amount, number_of_payments=12):
    try:
        meta = MetaData()  # Create all tables by issuing CREATE TABLE commands to the DB.
        Base.metadata.create_all(engine)
        lastdate = datetime.date.today() + datetime.timedelta(days=7 * (number_of_payments - 1))
        new_advanced = Advanced_Transactions(src=src, dst=dst, total_amount=total_amount,
                                             last_transaction=lastdate, status='develop')

        local_session.add(new_advanced)

        all_advanced_trans = local_session.query(Advanced_Transactions).all()
        new_a_id = len(all_advanced_trans)

        for y in range(number_of_payments):
            new_future = Future_Transactions(a_id=new_a_id, trans_date=datetime.date.today() +
                                                                       datetime.timedelta(days=7 * y),
                                             amount=int(total_amount / 12),
                                             transaction_id=0, status='develop')
            local_session.add(new_future)
        local_session.commit()
        print('successfully insert data into db')

    finally:
        local_session.close()


def update_transactionID_in_db(Aid, tranID):
    try:
        change_trans = local_session.query(Future_Transactions).filter_by(id=Aid).first()
        if change_trans.transaction_id == 0:
            change_trans.transaction_id = tranID
            local_session.commit()

    finally:
        local_session.close()


def update_transactionSTATUS_in_db(tranID, status):
    try:
        change_trans = local_session.query(Future_Transactions).filter_by(transaction_id=tranID).first()
        if change_trans.status == 'develop':
            change_trans.status = status
            if status == 'fail':
                new_failed_transaction(change_trans.a_id, tranID)

        local_session.commit()

    finally:
        local_session.close()


def new_failed_transaction(a_id, failed_id):
    try:
        parent_trans = local_session.query(Advanced_Transactions).filter_by(a_id=a_id).first()
        new_date = (parent_trans.last_transaction + datetime.timedelta(days=7)).date()
        new_future = Future_Transactions(a_id=a_id, trans_date=new_date, amount=int(parent_trans.total_amount / 12),
                                         transaction_id=0, status='develop')
        local_session.add(new_future)
        change_parent_last_date = local_session.query(Advanced_Transactions).filter_by(a_id=a_id).first()
        change_parent_last_date.last_transaction = change_parent_last_date.last_transaction + datetime.timedelta(days=7)
        local_session.commit()

        print('Because transaction number: ' + str(failed_id) + ' failed.')
        print('We added a new transaction with the same transaction details on:  ' + str(new_date))
        print('*************************')

    finally:
        local_session.commit()
        local_session.close()
