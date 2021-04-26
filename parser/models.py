"""Create table models for database"""
import hashlib
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# pylint: disable=too-few-public-methods
class CompanyInfo(Base):
    """Define CompanyInfo Table"""
    __tablename__ = 'company_info'
    cik_no = Column(String, primary_key=True)
    company_name = Column(String)
    cik_numbers = relationship("Filing13f")

    def __repr__(self):
        return "<CompanyInfo(cik_no='%s', company_name='%s')>" % (
            self.cik_no, self.company_name)


class Filing13f(Base):
    """Define Filing13f Table"""
    __tablename__ = 'filing_13f'
    accession_no = Column(String, primary_key=True)
    cik_no = Column(String, ForeignKey('company_info.cik_no'))
    filing_date = Column(Date)
    data_13f_rows = relationship("Data13f")

    def __repr__(self):
        return "<Filing13f(accession_no='%s', cik_no='%s', filing_date='%s')>" % (
            self.accession_no, self.cik_no, self.filing_date)


class Data13f(Base):
    """Define Data13f Table"""
    __tablename__ = 'data_13f'
    equity_holdings_id = Column(String, primary_key=True)
    accession_no = Column(String, ForeignKey('filing_13f.accession_no'))
    cik_no = Column(String)
    nameOfIssuer = Column(String)
    titleOfClass = Column(String)
    cusip = Column(String)
    value = Column(Numeric)
    sshPrnamt = Column(Integer)
    sshPrnamtType = Column(String)
    putCall = Column(String)
    investmentDiscretion = Column(String)
    otherManager = Column(String)
    votingAuthority_Sole = Column(Integer)
    votingAuthority_Shared = Column(Integer)
    votingAuthority_None = Column(Integer)

    def __repr__(self):
        return "<Data13f(accession_no='%s', cik_no='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%s', sshPrnamtType='%s', putCall='%s', " \
               "investmentDiscretion='%s', otherManager='%s', votingAuthority_Sole='%s', " \
               "votingAuthority_Shared='%s', votingAuthority_None='%s')>" % (
                   self.accession_no, self.cik_no, self.nameOfIssuer,
                   self.titleOfClass, self.cusip, self.value,
                   self.sshPrnamt, self.sshPrnamtType, self.putCall,
                   self.investmentDiscretion, self.otherManager, self.votingAuthority_Sole,
                   self.votingAuthority_Shared, self.votingAuthority_None)

    def create_filing_13f_primary_key(self):
        """Uses hash to generate Primary Key based on original row data for infotable table"""
        filing_13f_row_list = [self.accession_no,
                              self.cik_no,
                              self.nameOfIssuer,
                              self.titleOfClass,
                              self.titleOfClass,
                              self.cusip,
                              self.value,
                              self.sshPrnamt,
                              self.sshPrnamtType,
                              self.putCall,
                              self.investmentDiscretion,
                              self.otherManager,
                              self.votingAuthority_Sole,
                              self.votingAuthority_Shared,
                              self.votingAuthority_None
                              ]
        full_str = ''.join(str(cell) for cell in filing_13f_row_list)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()
