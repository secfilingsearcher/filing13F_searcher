import pandas as pd
from crawler_current_events import crawl_page
from parser_13f_primary_doc import primary_doc_parser
from parser_13f_infotable_V2 import infotable_parser

edgar_13f_list = []
primary_doc_list = []
infotable_list = []

# TODO; make function with no arg that returns lists that can be used outside

def main():
    crawl_page(edgar_13f_list, primary_doc_list, infotable_list)
    # create for loop and use one row function to get cik
    for primary_doc in primary_doc_list:
        primary_doc_parser(primary_doc)
    # create for loop and use infotable function to get database
    df = pd.DataFrame()
    for infotable in infotable_list:
        infotable_parser(infotable, df)

if __name__ == "__main__":
    main()

# print("check")
# print(edgar_13f_list)
# print(primary_doc_list)
# print(infotable_list)
