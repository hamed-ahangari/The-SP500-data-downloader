try:
    import yfinance as yf
except ImportError:
    raise ImportError("Cannot start without 'yfinance' package.\nInstall it before running the code again.")

import bs4 as bs
import numpy as np
import os
import requests
from datetime import datetime
from pandas.core.frame import DataFrame


class SP500DataLoader:
    def __init__(self):
        if not os.path.exists('Data'):
            os.makedirs('Data')

        self.start_date, self.end_date = None, None
        self.cleaned_prices = None
        self.cleaned_returns = None
        self.raw_prices = None
        self.raw_returns = None

        # Download stocks names from S&P500 page on wikipedia
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        self.tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            self.tickers.append(ticker)
        self.tickers = [s.replace('\n', '') for s in self.tickers]
        self.tickers = self.tickers + ["SPY"]

    # Check whether 'start_date' and 'end_date' make a valid date range or not
    def check_date_range(self, start_date: tuple, end_date: tuple):
        start = datetime(*start_date)
        end = datetime(*end_date)

        if end <= start:
            raise Exception("The start date must be before the end date!")

        return start, end

    # Doanload prices using yfinance
    def download_prices(self, start_date, end_date, interval='1d', column='Adj Close'):
        self.start_date, self.end_date = self.check_date_range(start_date, end_date)
        self.raw_prices = yf.download(self.tickers, start=self.start_date, end=self.end_date, interval=interval)[column]

    # Helper function to write dataframes on files with specified names
    def write_on_disk(self, data: DataFrame, filename: str):
        if "csv" in filename:
            data.to_csv('Data/' + filename)
        elif "h5" in filename:
            data.to_hdf('Data/' + filename, 'fixed', mode='w', complib='blosc', complevel=9)

        print(f"Saved: Data/{filename}")
    
    # Return a list of stock names in S&P 500 index
    def get_ticker_list(self):
        return self.tickers.copy()

    # Return raw prices data (which is not cleaned)
    def get_raw_prices(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False):
        self.download_prices(start_date, end_date)

        if save_as_csv:
            self.write_on_disk(self.raw_prices, "S&P500-raw_prices.csv")
        if save_as_h5:
            self.write_on_disk(self.raw_prices, "S&P500-raw_prices.h5")

        return self.raw_prices

    # Calculate and return raw returns data (which is not cleaned)
    def get_raw_returns(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False):
        self.get_raw_prices(start_date, end_date)

        self.raw_returns = self.raw_prices.copy()
        self.raw_returns = np.log(self.raw_returns).diff()
        self.raw_returns = self.raw_returns.iloc[1:]  # removes first row which is NaN after diff()

        if save_as_csv:
            self.write_on_disk(self.raw_returns, "S&P500-raw_returns.csv")
        if save_as_h5:
            self.write_on_disk(self.raw_returns, "S&P500-raw_returns.h5")

        return self.raw_returns

    # Return cleaned prices data (stocks with at least on NAN value are excluded)
    def get_cleaned_prices(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False):
        self.get_raw_prices(start_date, end_date)

        self.cleaned_prices = self.raw_prices.copy()
        # Remove companies (columns) with all missing values for whole time range
        self.cleaned_prices.dropna(axis='columns', how='all', inplace=True)
        # Remove days (rows) with missing values for all of companies
        self.cleaned_prices.dropna(axis='index', how='all', inplace=True)
        # Finally, remove the columns with at least one Nan (missing value)
        self.cleaned_prices.dropna(axis='columns', how='any', inplace=True)

        if save_as_csv:
            self.write_on_disk(self.self.cleaned_prices, "S&P500-cleaned_prices.csv")
        if save_as_h5:
            self.write_on_disk(self.self.cleaned_prices, "S&P500-cleaned_prices.h5")

        return self.cleaned_prices

    # Calculate return values using cleaned data, and return the dataframe
    def get_cleaned_returns(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False):
        self.get_cleaned_prices(start_date, end_date)

        self.cleaned_returns = self.cleaned_prices.copy()
        self.cleaned_returns = np.log(self.cleaned_returns).diff()
        self.cleaned_returns = self.cleaned_returns.iloc[1:]  # removes first row which is NaN after diff()

        if save_as_csv:
            self.write_on_disk(self.cleaned_returns, "S&P500-cleaned_returns.csv")
        if save_as_h5:
            self.write_on_disk(self.cleaned_returns, "S&P500-cleaned_returns.h5")

        return self.cleaned_returns

    # Return the last values for raw prices without redownloading them
    def get_last_raw_prices(self, save_as_h5=False, save_as_csv=False):
        if self.raw_prices is None:
            return None

        if save_as_csv:
            self.write_on_disk(self.raw_prices, "S&P500-raw_prices.csv")
        if save_as_h5:
            self.write_on_disk(self.raw_prices, "S&P500-raw_prices.h5")

        return self.raw_prices

    # Return the last values for raw returns without redownloading them
    def get_last_raw_returns(self, save_as_h5=False, save_as_csv=False):
        if self.raw_returns is None:
            return None

        if save_as_csv:
            self.write_on_disk(self.raw_returns, "S&P500-raw_returns.csv")
        if save_as_h5:
            self.write_on_disk(self.raw_returns, "S&P500-raw_returns.h5")

        return self.raw_returns

    # Return the last values for cleaned prices without redownloading them
    def get_last_cleaned_prices(self, save_as_h5=False, save_as_csv=False):
        if self.cleaned_prices is None:
            return None

        if save_as_csv:
            self.write_on_disk(self.cleaned_prices, "S&P500-cleaned_prices.csv")
        if save_as_h5:
            self.write_on_disk(self.cleaned_prices, "S&P500-cleaned_prices.h5")

        return self.cleaned_prices

    # Return the last values for cleaned returns without redownloading them
    def get_last_cleaned_returns(self, save_as_h5=False, save_as_csv=False):
        if self.cleaned_returns is None:
            return None

        if save_as_csv:
            self.write_on_disk(self.cleaned_returns, "S&P500-cleaned_returns.csv")
        if save_as_h5:
            self.write_on_disk(self.cleaned_returns, "S&P500-cleaned_returns.h5")

        return self.cleaned_returns
