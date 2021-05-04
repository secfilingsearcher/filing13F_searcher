from edgar_filing_searcher.parsers.crawler_current_events import get_text, \
    parse_13f_filing_detail_urls
from edgar_filing_searcher.database import db


def create_url_list(url_edgar_current_events):
    text_edgar_current_events = get_text(url_edgar_current_events)
    return parse_13f_filing_detail_urls(text_edgar_current_events)


def send_data_to_db(company_row, edgar_filing_row, data_13f_table):
    db.session.add(company_row)
    db.session.add(edgar_filing_row)
    db.session.add_all(data_13f_table)
    db.session.commit()
