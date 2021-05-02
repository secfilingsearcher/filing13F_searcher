"""Create table models for database"""
import hashlib

from dataclasses import dataclass
from filingapi.database import db


# pylint: disable=too-few-public-methods
@dataclass
class Company(db.Model):
    """Define CompanyInfo Table"""
    cik_no: str
    company_name: str

    __tablename__ = 'company'
    cik_no = db.Column(db.String, primary_key=True)
    company_name = db.Column(db.String)
    cik_numbers = db.relationship("EdgarFiling")

    def __repr__(self):
        return "<Company(cik_no='%s', company_name='%s')>" % (
            self.cik_no, self.company_name)


@dataclass
class EdgarFiling(db.Model):
    """Define EdgarFiling Table"""
    __tablename__ = 'edgar_filing'
    accession_no = db.Column(db.String, primary_key=True)
    cik_no = db.Column(db.String, db.ForeignKey('company.cik_no'))
    filing_date = db.Column(db.Date)
    data_13f_rows = db.relationship("Data13f")

    def __repr__(self):
        return "<EdgarFiling(accession_no='%s', cik_no='%s', filing_date='%s')>" % (
            self.accession_no, self.cik_no, self.filing_date)


@dataclass
class Data13f(db.Model):
    """Define Data13f Table"""
    __tablename__ = 'data_13f'
    equity_holdings_id = db.Column(db.String, primary_key=True)
    accession_no = db.Column(db.String, db.ForeignKey('edgar_filing.accession_no'))
    cik_no = db.Column(db.String)
    nameOfIssuer = db.Column(db.String)
    titleOfClass = db.Column(db.String)
    cusip = db.Column(db.String)
    value = db.Column(db.Numeric)
    sshPrnamt = db.Column(db.Integer)
    sshPrnamtType = db.Column(db.String)
    putCall = db.Column(db.String)
    investmentDiscretion = db.Column(db.String)
    otherManager = db.Column(db.String)
    votingAuthority_Sole = db.Column(db.Integer)
    votingAuthority_Shared = db.Column(db.Integer)
    votingAuthority_None = db.Column(db.Integer)

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

    def create_data_13f_primary_key(self):
        """Uses hash to generate Primary Key based on original row data for Data13f table"""
        data_13f_row_list = [self.accession_no,
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
        full_str = ''.join(str(cell) for cell in data_13f_row_list)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()

