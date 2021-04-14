"""Create table models for database"""
import hashlib

from database import Base
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship


# pylint: disable=too-few-public-methods
@dataclass
class PrimaryDoc(Base):
    accession_no: str
    cik_no: str
    company_name: str
    filing_date: Date

    """Define PrimaryDoc Table"""
    __tablename__ = 'primary_doc'
    accession_no = Column(String, primary_key=True)
    cik_no = Column(String)
    company_name = Column(String)
    filing_date = Column(Date)
    infotable_rows = relationship("Infotable")

    def __repr__(self):
        return "<User(accession_no='%s', cik_no='%s', filing_date='%s', company_name='%s')>" % (
            self.accession_no, self.cik_no, self.filing_date, self.company_name)


class Infotable(Base):
    """Define Infotable Table"""
    __tablename__ = 'infotable'
    row_id = Column(String, primary_key=True)
    accession_no = Column(String, ForeignKey('primary_doc.accession_no'))
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
        return "<User(accession_no='%s', cik_no='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%s', sshPrnamtType='%s', putCall='%s', " \
               "investmentDiscretion='%s', otherManager='%s', votingAuthority_Sole='%s', " \
               "votingAuthority_Shared='%s', votingAuthority_None='%s')>" % (
                   self.accession_no, self.cik_no, self.nameOfIssuer,
                   self.titleOfClass, self.cusip, self.value,
                   self.sshPrnamt, self.sshPrnamtType, self.putCall,
                   self.investmentDiscretion, self.otherManager, self.votingAuthority_Sole,
                   self.votingAuthority_Shared, self.votingAuthority_None)

    def create_primary_key(self):
        """Uses hash to generate Primary Key based on original row data for infotable table"""
        infotable_row_list = [self.accession_no,
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
        full_str = ''.join(str(cell) for cell in infotable_row_list)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()
