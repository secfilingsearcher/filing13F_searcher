"""Generates Primary Key"""
import hashlib

from models import Infotable

def primary_key_generator_primary_doc(row):
    """Uses hash to generate Primary Key based on original row data"""
    full_str = ''.join(str(cell) for cell in row)
    result = hashlib.md5(full_str.encode())
    return result.hexdigest()

def primary_key_generator_infotable(infotable_row: Infotable):
    """Uses hash to generate Primary Key based on original row data"""
    infotable_row_list = [Infotable.nameOfIssuer, Infotable.titleOfClass,
                          Infotable.titleOfClass,
                          Infotable.cusip,
                          Infotable.value,
                          Infotable.sshPrnamt,
                          Infotable.sshPrnamtType,
                          Infotable.putCall,
                          Infotable.investmentDiscretion,
                          Infotable.otherManager,
                          Infotable.votingAuthority_Sole,
                          Infotable.votingAuthority_Shared,
                          Infotable.votingAuthority_None
                          ]
    full_str = ''.join(str(cell) for cell in infotable_row_list)
    result = hashlib.md5(full_str.encode())
    return result.hexdigest()
