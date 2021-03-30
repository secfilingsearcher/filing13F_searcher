"""Create table models for database"""
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PrimaryDoc(Base):
    """Define PrimaryDoc Table"""
    __tablename__ = 'primary_doc'
    id = Column(String(50), primary_key=True)
    cik = Column(String(50))
    company_name = Column(String(50))
    filing_date = Column(Date)

    def __repr__(self):
        return "<User(cik='%s', filing_date='%s', company_name='%s')>" % (
            self.cik, self.filing_date, self.company_name)


class Infotable(Base):
    """Define Infotable Table"""
    __tablename__ = 'infotable'
    id = Column(String, primary_key=True)
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
        return "<User(accession_no='%s', cik='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%s', sshPrnamtType='%s', putCall='%s', " \
               "investmentDiscretion='%s', otherManager='%s', votingAuthority_Sole='%s', " \
               "votingAuthority_Shared='%s', votingAuthority_None='%s')>" % (
                   self.accession_no, self.cik, self.nameOfIssuer,
                   self.titleOfClass, self.cusip, self.value,
                   self.sshPrnamt, self.sshPrnamtType, self.putCall,
                   self.investmentDiscretion, self.otherManager, self.votingAuthority_Sole,
                   self.votingAuthority_Shared, self.votingAuthority_None)
