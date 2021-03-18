"""docstring"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine(os.environ.get('DB_CONNECTION_STRING'), echo=True)
Base = declarative_base()


class Infotable(Base):
    """docstring"""
    __tablename__ = 'infotable'
    id = Column(Integer, primary_key=True)
    accession_no = Column(String(50))
    cik = Column(String(50))
    nameOfIssuer = Column(String(50))
    titleOfClass = Column(String(50))
    cusip = Column(String(50))
    value = Column(Numeric)
    sshPrnamt = Column(Integer)
    sshPrnamtType = Column(String(50))
    putCall = Column(String(50))
    investmentDiscretion = Column(String(50))
    otherManager = Column(String(50))
    votingAuthority_Sole = Column(Integer)
    votingAuthority_Shared = Column(Integer)
    votingAuthority_None = Column(Integer)

    def __repr__(self):
        return "<User(accession_no='%i', cik='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%i', sshPrnamtType='%i', putCall='%i', " \
               "investmentDiscretion='%i', otherManager='%i', votingAuthority_Sole='%i', " \
               "votingAuthority_Shared='%i', votingAuthority_None='%i')>" % (
                   self.accession_no, self.cik, self.nameOfIssuer,
                   self.titleOfClass, self.cusip, self.value,
                   self.sshPrnamt, self.sshPrnamtType, self.putCall,
                   self.investmentDiscretion, self.otherManager, self.votingAuthority_Sole,
                   self.votingAuthority_Shared, self.votingAuthority_None)


class PrimaryDoc(Base):
    """docstring"""
    __tablename__ = 'primary_doc'
    id = Column(Integer, primary_key=True)
    cik = Column(String(50))
    company_name = Column(String(50))
    filing_date = Column(Date)

    def __repr__(self):
        return "<User(cik='%s', filing_date='%s', company_name='%s')>" % (
            self.cik, self.filing_date, self.company_name)


Base.metadata.create_all(engine_)
Session = sessionmaker(bind=engine_)
session = Session()



def insert_in_primary_table(id, cik, company_name, filing_date):
    """docstring"""
    session.add(PrimaryDoc(id=id, cik=cik, company_name=company_name, filing_date=filing_date))
    session.commit()


def insert_in_infotable_table(engine, df: pd.DataFrame):
    """docstring"""
    df.to_sql(name='infotable', con=engine, if_exists="fail")
