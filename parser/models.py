"""Create table models for database"""
import hashlib
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PrimaryDoc(Base):
    """Define PrimaryDoc Table"""
    __tablename__ = 'primary_doc'
    row_id = Column(String(50), primary_key=True)
    accession_no = Column(String(50))
    cik_no = Column(String(50))
    company_name = Column(String(50))
    filing_date = Column(Date)

    def __repr__(self):
        return "<User(accession_no='%s', cik_value='%s', filing_date='%s', company_name='%s')>" % (
            self.accession_no, self.cik_no, self.filing_date, self.company_name)

    def create_pk_for_primary_doc(self):
        """Uses hash to generate Primary Key based on original row data for primary doc table"""
        row = [self.cik_no, self.company_name, self.filing_date]
        full_str = ''.join(str(cell) for cell in row)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()


class Infotable(Base):
    """Define Infotable Table"""
    __tablename__ = 'infotable'
    row_id = Column(String, primary_key=True)
    accession_no = Column(String(50))
    cik_no = Column(String(50))
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
        return "<User(accession_no='%s', cik_value='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%s', sshPrnamtType='%s', putCall='%s', " \
               "investmentDiscretion='%s', otherManager='%s', votingAuthority_Sole='%s', " \
               "votingAuthority_Shared='%s', votingAuthority_None='%s')>" % (
            self.accession_no, self.cik_no, self.nameOfIssuer,
            self.titleOfClass, self.cusip, self.value,
            self.sshPrnamt, self.sshPrnamtType, self.putCall,
            self.investmentDiscretion, self.otherManager, self.votingAuthority_Sole,
            self.votingAuthority_Shared, self.votingAuthority_None)

    def create_pk_for_infotable(self):
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
