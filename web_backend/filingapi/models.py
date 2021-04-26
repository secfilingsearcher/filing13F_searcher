"""Create table models for database"""
import hashlib

from dataclasses import dataclass
from web_backend.filingapi.database import db

@dataclass
class Infotable(db.Model):
    """Table class that show filing data"""
    # pylint: disable=too-many-instance-attributes

    row_id: str
    accession_no: str
    cik_no: str
    name_of_issuer: str
    title_of_class: str

    __tablename__ = 'infotable'
    row_id = db.Column(db.String, primary_key=True)
    accession_no = db.Column(db.String, db.ForeignKey('primary_doc.accession_no'))
    cik_no = db.Column(db.String)
    name_of_issuer = db.Column(db.String)
    title_of_class = db.Column(db.String)
    cusip = db.Column(db.String)
    value = db.Column(db.Numeric)
    ssh_prnamt = db.Column(db.Integer)
    ssh_prnamt_type = db.Column(db.String)
    put_call = db.Column(db.String)
    investment_discretion = db.Column(db.String)
    other_manager = db.Column(db.String)
    voting_authority_sole = db.Column(db.Integer)
    voting_authority_shared = db.Column(db.Integer)
    voting_authority_none = db.Column(db.Integer)

    def __repr__(self):
        return "<Infotable(accession_no='%s', cik_no='%s', nameOfIssuer='%s', " \
               "titleOfClass='%s', cusip='%s', value='%s', " \
               "sshPrnamt='%s', sshPrnamtType='%s', putCall='%s', " \
               "investmentDiscretion='%s', otherManager='%s', votingAuthority_Sole='%s', " \
               "votingAuthority_Shared='%s', votingAuthority_None='%s')>" % (
                   self.accession_no, self.cik_no, self.name_of_issuer,
                   self.title_of_class, self.cusip, self.value,
                   self.sshPrnamt, self.sshPrnamtType, self.putCall,
                   self.investment_discretion, self.other_manager, self.voting_authority_sole,
                   self.voting_authority_shared, self.voting_authority_none)

    def create_primary_key(self):
        """Uses hash to generate Primary Key based on original row data for infotable table"""
        infotable_row_list = [self.accession_no,
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
        full_str = ''.join(str(cell) for cell in infotable_row_list)
        result = hashlib.md5(full_str.encode())
        return result.hexdigest()


@dataclass
class PrimaryDoc(db.Model):
    """Main document displaying company data"""
    accession_no: str
    cik_no: str
    company_name: str
    filing_date: db.Date
    infotable_rows: Infotable

    """Define PrimaryDoc Table"""
    __tablename__ = 'primary_doc'
    accession_no = db.Column(db.String, primary_key=True)
    cik_no = db.Column(db.String)
    company_name = db.Column(db.String)
    filing_date = db.Column(db.Date)
    infotable_rows = db.relationship("Infotable")

    def __repr__(self):
        return "<PrimaryDoc(accession_no='%s', cik_no='%s', filing_date='%s', company_name='%s')>" \
               % (self.accession_no, self.cik_no, self.filing_date, self.company_name)
