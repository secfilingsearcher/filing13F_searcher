"""Create table models for database"""
import hashlib
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# pylint: disable=too-few-public-methods
class PrimaryDoc(Base):
    """Define PrimaryDoc Table"""
    __tablename__ = 'primary_doc'
    accession_no = Column(String(50), primary_key=True)
    cik_no = Column(String(50))
    company_name = Column(String(50))
    filing_date = Column(Date)
    infotable_rows = relationship("Infotable")

    def __repr__(self):
        return "<User(accession_no='%s', cik_no='%s', filing_date='%s', company_name='%s')>" % (
            self.accession_no, self.cik_no, self.filing_date, self.company_name)


class Infotable(Base):
    """Define Infotable Table"""
    __tablename__ = 'infotable'
    row_id = Column(String(70), primary_key=True)
    accession_no = Column(String(70), ForeignKey('primary_doc.accession_no'))
    cik_no = Column(String(70))
    nameOfIssuer = Column(String(70))
    titleOfClass = Column(String(70))
    cusip = Column(String(70))
    value = Column(Numeric)
    sshPrnamt = Column(Integer)
    sshPrnamtType = Column(String(70))
    putCall = Column(String(70))
    investmentDiscretion = Column(String(70))
    otherManager = Column(String(70))
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
