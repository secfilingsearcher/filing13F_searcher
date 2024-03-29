"""Create table models for database"""
import hashlib
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from edgar_filing_searcher.database import db


@dataclass
class EdgarFiling(db.Model):
    """Define EdgarFiling Table"""
    accession_no: str
    cik_no: str
    filing_type: str
    filing_date: date

    __tablename__ = 'edgar_filing'
    # accession_no: filing id number
    accession_no = db.Column(db.String, primary_key=True)
    # cik_no: central index key number
    cik_no = db.Column(db.String, db.ForeignKey('company.cik_no'), index=True)
    # filing_type: type of SEC filing
    filing_type = db.Column(db.String)
    # filing_date: date of filing
    filing_date = db.Column(db.Date)
    data_13f_rows = db.relationship("Data13f")


# pylint: disable=too-few-public-methods
@dataclass
class Company(db.Model):
    """Define CompanyInfo Table"""
    cik_no: str
    company_name: str
    filing_count: int

    __tablename__ = 'company'
    # cik_no: central index key number
    cik_no = db.Column(db.String, primary_key=True)
    # company_name: name of company
    company_name = db.Column(db.String, index=True)
    # filing_count: number of stored filings
    filing_count = db.Column(db.Integer)
    filings = db.relationship("EdgarFiling")

    __table_args__ = (
        db.Index('company_company_name_cover_index',
                 company_name,
                 cik_no,
                 filing_count),
        db.Index('company_company_name_gin_index',
                 company_name,
                 postgresql_ops={"company_name": "gin_trgm_ops"},
                 postgresql_using='gin'),
    )


# pylint: disable=too-many-instance-attributes
@dataclass
class Data13f(db.Model):
    """Define Data13f Table"""
    equity_holdings_id: str = field(repr=False)
    accession_no: str
    cik_no: str
    name_of_issuer: str
    title_of_class: str
    cusip: str
    value: Decimal
    ssh_prnamt: int
    ssh_prnamt_type: str
    put_call: str
    investment_discretion: str
    other_manager: str
    voting_authority_sole: int
    voting_authority_shared: int
    voting_authority_none: int

    __tablename__ = 'data_13f'
    # equity_holdings_id: id of equity holdings. Generated by create_data_13f_primary_key function
    equity_holdings_id = db.Column(db.String, primary_key=True)
    # accession_no: filing id number
    accession_no = db.Column(db.String, db.ForeignKey('edgar_filing.accession_no'), index=True)
    # cik_no: central index key number
    cik_no = db.Column(db.String)
    # name_of_issuer: issuer for each class of security reported
    name_of_issuer = db.Column(db.String)
    # title_of_class: title of the class of the security
    title_of_class = db.Column(db.String)
    # cusip: 9 digit CUSIP number of the security
    cusip = db.Column(db.String, index=True)
    # value: market value of the holding of the particular class of security
    value = db.Column(db.Numeric(asdecimal=False))
    # ssh_prnamt: shares or principal amount
    ssh_prnamt = db.Column(db.Integer)
    # ssh_prnamt_type: shares or principal amount code (SH or PRN)
    ssh_prnamt_type = db.Column(db.String)
    # put_call: put and call options designation following such segregated entries
    put_call = db.Column(db.String)
    # investment_discretion: designate investment discretion as “sole” (SOLE),
    # “shareddefined” (DEFINED), or “shared-other” (OTHER)
    investment_discretion = db.Column(db.String)
    # other_manager: other Manager on whose behalf this Form 13F report is being filed with
    other_manager = db.Column(db.String)
    # voting_authority_sole: number of shares for which the Manager exercises sole voting authority
    voting_authority_sole = db.Column(db.Integer)
    # voting_authority_shared: number of shares where the Manager exercises shared voting authority
    voting_authority_shared = db.Column(db.Integer)
    # voting_authority_none: number of shares for which the Manager exercises no voting authority
    voting_authority_none = db.Column(db.Integer)

    __table_args__ = (
        db.Index('data_13f_name_of_issuer_gin_index',
                 name_of_issuer,
                 postgresql_ops={"name_of_issuer": "gin_trgm_ops"},
                 postgresql_using='gin'),
    )

    def create_data_13f_primary_key(self):
        """Uses hash to generate Primary Key based on original row data for Data13f table"""
        data_13f_row_list = [
            self.accession_no,
            self.cik_no,
            self.name_of_issuer,
            self.title_of_class,
            self.title_of_class,
            self.cusip,
            self.value,
            self.ssh_prnamt,
            self.ssh_prnamt_type,
            self.put_call,
            self.investment_discretion,
            self.other_manager,
            self.voting_authority_sole,
            self.voting_authority_shared,
            self.voting_authority_none
        ]
        full_str = ''.join(str(cell) for cell in data_13f_row_list)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()
