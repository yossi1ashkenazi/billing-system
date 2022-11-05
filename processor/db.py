from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, create_engine, Boolean, MetaData

Base = declarative_base()
engine = create_engine("postgresql://postgres:075151@localhost:5432/Processor")
Session = sessionmaker()
local_session = Session(bind=engine)
meta = MetaData()


class TransactionReport(Base):
    __tablename__ = 'transactions_report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trans_id = Column(Integer, primary_key=True)
    trans_date = Column(DateTime, nullable=False)
    status = Column(String(25), primary_key=False)

# Create all tables by issuing CREATE TABLE commands to the DB.
Base.metadata.create_all(engine)
