from sqlalchemy import func, select, MetaData, Table, \
    create_engine


def primary_doc_checker(engine):
    if count_duplicate_primary(engine):
        remove_duplicate_primary(engine)


def infotable_checker(engine):
    if count_duplicate_infotable(engine):
        remove_duplicate_infotable(engine)


def count_duplicate_infotable(engine):
    infotable = Table('infotable', MetaData(), autoload=True, autoload_with=engine)
    statement = select(
        [infotable.columns.accession_no,
         infotable.columns.cik,
         infotable.columns.nameOfIssuer,
         infotable.columns.titleOfClass,
         infotable.columns.cusip,
         infotable.columns.value,
         infotable.columns.sshPrnamt,
         infotable.columns.sshPrnamtType,
         infotable.columns.putCall,
         infotable.columns.investmentDiscretion,
         infotable.columns.otherManager,
         infotable.columns.votingAuthority_Sole,
         infotable.columns.votingAuthority_Shared,
         infotable.columns.votingAuthority_None,
         func.count().label('num of duplicates')]) \
        .group_by(infotable.columns.accession_no,
                  infotable.columns.cik,
                  infotable.columns.nameOfIssuer,
                  infotable.columns.titleOfClass,
                  infotable.columns.cusip,
                  infotable.columns.value,
                  infotable.columns.sshPrnamt,
                  infotable.columns.sshPrnamtType,
                  infotable.columns.putCall,
                  infotable.columns.investmentDiscretion,
                  infotable.columns.otherManager,
                  infotable.columns.votingAuthority_Sole,
                  infotable.columns.votingAuthority_Shared,
                  infotable.columns.votingAuthority_None) \
        .having(func.count() > 1)
    print(str(statement))
    print(engine.execute(statement).fetchall())
    return engine.execute(statement).fetchall()



def count_duplicate_primary(engine):
    primary_doc = Table('primary_doc', MetaData(), autoload=True, autoload_with=engine)
    statement = select(
        [primary_doc.columns.cik, primary_doc.columns.filing_date, primary_doc.columns.company_name,
         func.count().label('num of duplicates')]) \
        .group_by(primary_doc.columns.cik, primary_doc.columns.filing_date,
                  primary_doc.columns.company_name) \
        .having(func.count() > 1)
    print(str(statement))
    print(engine.execute(statement).fetchall())
    return engine.execute(statement).fetchall()



def remove_duplicate_infotable(engine):
    infotable = Table('infotable', MetaData(), autoload=True, autoload_with=engine)
    statement = infotable.delete() \
        .where(
        infotable.columns.id.notin_(select([func.max(infotable.columns.id).label('MaxRecordID')])
                                    .select_from(infotable)
                                    .group_by(infotable.columns.accession_no,
                                              infotable.columns.cik,
                                              infotable.columns.nameOfIssuer,
                                              infotable.columns.titleOfClass,
                                              infotable.columns.cusip,
                                              infotable.columns.value,
                                              infotable.columns.sshPrnamt,
                                              infotable.columns.sshPrnamtType,
                                              infotable.columns.putCall,
                                              infotable.columns.investmentDiscretion,
                                              infotable.columns.otherManager,
                                              infotable.columns.votingAuthority_Sole,
                                              infotable.columns.votingAuthority_Shared,
                                              infotable.columns.votingAuthority_None)
                                    ))
    print(str(statement))
    print(engine.execute(statement).fetchall())
    return engine.execute(statement).fetchall()



def remove_duplicate_primary(engine):
    primary_doc = Table('primary_doc', MetaData(), autoload=True, autoload_with=engine)
    statement = primary_doc.delete() \
        .where(primary_doc.columns.id.notin_(
            select([func.max(primary_doc.columns.id).label('MaxRecordID')]).select_from(
                primary_doc).group_by(primary_doc.columns.cik, primary_doc.columns.filing_date,
                                      primary_doc.columns.company_name)))
    print(str(statement))
    print(engine.execute(statement).fetchall())
    return engine.execute(statement).fetchall()




