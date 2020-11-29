# Up transactions fetch

At the moment, the quickest way to get all your transactions for a given date
range is via Up's API.
This is how I accessed my data to help filing my tax, and now you can too :)
Transactions between your savers and spending account are ignored.

## Usage

Get your up key from https://api.up.com.au/getting_started

```sh
# use a python>=3.7 environment
pip install -r requirements.txt
# exmaple for financial year 2019/2020
UP_KEY=<up:yeah:XXXX> python main.py 2019-07-01 2020-06-30
# alternatively, add your UP_KEY to your environment another way
```
