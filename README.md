# Application - 📝 Todo list

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/ghandic/PyCap-TODO-CRUD)
![coverage](https://img.shields.io/badge/coverage-0%25-red)

This commandline program is a basic implementation for a todo list application using Python 3.6+ that allows you to build and maintain a TODO list.

## Requirements

This program requirements can be found in the requirements.txt

## Usage
You can run `python app.py` in a virtual environment or use the docker commands `docker-compose build` and `docker-compose up`to run the app.

### Program options

#### Searching for a Stock
You can search for a stock in the input field found in the sidebar.
Simply typing in a stock (without hitting the button) will search for the stock - returning the historical closing price information in a graph, and the last day open/close change as a green/red indicator above the graph.

#### Add/Removing a Company Stock from your Holdings
Once you've searched for a stock, you are able to add or remove it to your holdings list by clicking the button `Add/Remove Company`.
This will add (or remove) it to the "My Holdings Table" section at the bottom.

#### Editing your Holdings Quantity
Once you've added a stock to your holdings table, you can edit the "Owned" column values to reflect the number of stocks you own of that stock.
This will automatically update the "Total Value" column of the stock, and update the pie graph representing your holdings.

#### Watchlist
The "Watchlist" tab (found on the sidebar menu) showcases all the stocks you've previously searched. They have been saved to disc to allow quick reference and offline view.

## Pros, cons and next steps

### Pros

- Great starting point for a financial dashboard
- Can see what a given portfolio would be worth today
- Simple and intuitive to use
- Exposure to Dash

### Cons

- Doesn't provide any value (yet :P)
- Clicking "add/remove company" while it hasn't finished loading the current ticker figures can bug out the entire application a bit. Likewise, clicking "add/remove" multiple times in quick succession.
- Doesn't save your Holdings between sessions
- Only reloads Watchlist stocks from memory - doesn't update with latest prices
- Cannot enter date/price you paid for a given stock so there's no actual holdings growth statistics
- Searches for stocks based on user input before clicking a button... so saves "G", "GO", "GOO", "GOOG" and "GOOGL" when searching for google stock.
- Likewise, searches for stocks with input field being empty, reporting back several errors to the user and saving all of those successful searches to disc - that then show up in the Watchlist graph (couldn't get `app.config['suppress_callback_exceptions']=True` to work)
- No way to delete stocks on Watchlist (files on disc)

### Next steps

- Throw it out and start again :P
- Create unit tests for Dash based sections of code
- Save Holdings perminantly
- Add buy in-price/date so you can see holdings growth
- Maybe find out next dividend payout date or total to-date dividends
- Sentiment analysis or even just search for company news quantities on twitter/reddit etc.

## License

This project is licensed under the terms of the MIT license.
