"""Generates Primary Key"""
import hashlib

from models import Infotable


def pk_generator_for_primary_doc(row):
    """Uses hash to generate Primary Key based on original row data for primary doc table"""
    full_str = ''.join(str(cell) for cell in row)
    result = hashlib.md5(full_str.encode())
    return result.hexdigest()


def pk_generator_for_infotable(infotable_row: Infotable):
    """Uses hash to generate Primary Key based on original row data for infotable table"""
    infotable_row_list = [infotable_row.accession_no,
                          infotable_row.cik,
                          infotable_row.nameOfIssuer,
                          infotable_row.titleOfClass,
                          infotable_row.titleOfClass,
                          infotable_row.cusip,
                          infotable_row.value,
                          infotable_row.sshPrnamt,
                          infotable_row.sshPrnamtType,
                          infotable_row.putCall,
                          infotable_row.investmentDiscretion,
                          infotable_row.otherManager,
                          infotable_row.votingAuthority_Sole,
                          infotable_row.votingAuthority_Shared,
                          infotable_row.votingAuthority_None
                          ]
    full_str = ''.join(str(cell) for cell in infotable_row_list)
    result = hashlib.md5(full_str.encode())
    return result.hexdigest()
