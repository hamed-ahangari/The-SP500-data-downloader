
# S&P 500 data loader
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17EmGwu6_bgm7KqQcImlunCJVaDeocMIB?usp=sharing)
I have written an S&P500 data downloader class in python to retrieve the history of prices for stocks indexed as S&P 500. The data loader came in handy when I was working on training recurrent neural networks to forecast returns from the stock market.
## S&P 500 
The S&P 500, or simply the S&P, is a stock market index that measures the stock performance of 500 large companies listed on stock exchanges in the United States. It is one of the most commonly followed equity indices. (read more on [Wikipedia](https://en.wikipedia.org/wiki/S%26P_500))
## Code and how to use
### Prerequisite 
First of all, you should install [yfinance](https://pypi.org/project/yfinance/) package on your Python 3 environment. The `yfinance` Python package is the tool used in my code to extract the prices for each asset from [Yahoo! Finance](http://finance.yahoo.com/ "Yahoo! Finance is a media property that is part of the Yahoo! network, which, since 2017, is owned by Verizon Media. It provides financial news, data, and commentary, including stock quotes, press releases, financial reports, and original content. It also offers some online tools for personal finance management.") webpages.
For a simple installation, run the below code in your terminal/cmd:
```
pip install yfinance
```
For more information on yfinance python package: [yfinance . PyPI](https://pypi.org/project/yfinance/)
### How to use
Create an object to let the constructor of the data downloader class read the stocks codes from the [S&P 500 page on Wikipedia](https://en.wikipedia.org/wiki/S%26P_500). Then you will be able to call the method functions to download the prices and write the data on disk.

#### Methods of the class
Here is a list of method functions you call using the created object:


- Return a list of stock names in the S&P 500 index:
```python
get_stocks_list()
```

- Return raw prices data (which is not cleaned):

```python
get_raw_prices(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False)
```

- Calculate and return raw returns data (which is not cleaned):
```python
get_raw_returns(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False)
```

- Return cleaned prices data (stocks with at least one NAN value are excluded):
```python
get_cleaned_prices(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False)
```

- Calculate return values using cleaned data, and return the dataframe:
```python
get_cleaned_returns(self, start_date: tuple, end_date: tuple, interval='1d', column='Adj Close', save_as_h5=False, save_as_csv=False)
```

- Return the last values for raw prices without redownloading them:
```python
get_last_raw_prices(self, save_as_h5=False, save_as_csv=False)
```

- Return the last values for raw returns without redownloading them:
```python
get_last_raw_returns(self, save_as_h5=False, save_as_csv=False)
```

- Return the last values for cleaned prices without redownloading them:
```python
get_last_cleaned_prices(self, save_as_h5=False, save_as_csv=False)
```

- Return the last values for cleaned returns without redownloading them:
```python
get_last_cleaned_returns(self, save_as_h5=False, save_as_csv=False)
```
#### Example of driver code
Finally, below is an example of how you can download data via SP500DataLoader class.
```python
# TEST
# Driver code
data_downloader_object = SP500DataLoader()

# Get cleaned return values
cleaned_returns = data_downloader_object.get_cleaned_returns(
	start_date=(2006,  1,  1), end_date=(2020,  12,  30),
	interval='1d', column='Adj Close',
	save_as_h5=True, save_as_csv=True
)

# Print a part of the dataframe of cleaned returns
print("--------------------------------------------")
print(cleaned_returns.head(10))
```
