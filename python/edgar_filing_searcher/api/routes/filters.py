"""Filters for API for web back-end"""
from datetime import datetime

from edgar_filing_searcher.models import EdgarFiling


def filter_company_by_date(filings, start_date, end_date):
    """Filter companies by edgar_filings and date"""
    filings = filings.join(EdgarFiling)

    if start_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= start_date
        )

    if end_date:
        filings = filings.filter(
            EdgarFiling.filing_date <= end_date
        )
    return filings


def filter_edgar_filing_by_date(filings, start_date, end_date):
    """Filter edgar_filings by date"""

    if start_date:
        filings = filings.filter(
            EdgarFiling.filing_date >= start_date
        )
    if end_date:
        filings = filings.filter(
            EdgarFiling.filing_date <= end_date
        )

    return filings
