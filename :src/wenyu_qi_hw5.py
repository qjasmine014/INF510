import argparse
import requests
import pandas as pd
import ast
from datetime import datetime
from bs4 import BeautifulSoup
from remote import grab_data_by_scraping_and_api_requests
from download_url import download
from local import grab_data_from_downloaded_raw_files
from clean import clean_data
from draw_picture import draw_picuture

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local", "remote"], nargs=1, help="where data should be gotten from")
    args = parser.parse_args()

    location = args.source[0]

    if location == "local":
        download()
        grab_data_from_downloaded_raw_files()
    else:
        grab_data_by_scraping_and_api_requests()

    future_dates,past_dates_format = clean_data()
    draw_picuture(future_dates, past_dates_format)

if __name__ == "__main__":
    main()