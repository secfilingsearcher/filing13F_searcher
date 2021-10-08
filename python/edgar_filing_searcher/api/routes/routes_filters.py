"""APi for web back-end"""
from datetime import datetime

from edgar_filing_searcher.models import EdgarFiling


def filter_company_by_date(filings, start_date, end_date):
    """Filter companies by edgar_filings and date"""

    if start_date and end_date:
        filings = filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, '%Y-%m-%d')
        )
        filings = filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, '%Y-%m-%d')
        )
        return filings

    if start_date:
        return filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, '%Y-%m-%d')
        )

    if end_date:
        return filings.join(EdgarFiling).filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, '%Y-%m-%d')
        )
    return filings


def filter_edgar_filing_by_date(filings, start_date, end_date):
    """Filter edgar_filings by date"""

    if start_date and end_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, '%Y-%m-%d')
        )
        filings = filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, '%Y-%m-%d')
        )
        return filings
    if start_date:
        return filings.filter(
            EdgarFiling.filing_date >= datetime.strptime(start_date, '%Y-%m-%d')
        )
    if end_date:
        return filings.filter(
            EdgarFiling.filing_date <= datetime.strptime(end_date, '%Y-%m-%d')
        )

    return filings
