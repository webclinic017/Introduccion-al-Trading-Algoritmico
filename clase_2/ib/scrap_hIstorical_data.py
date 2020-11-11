from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import argparse
import pandas
from Dates import Dates
import time
import pdb


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle
        self.processing = False
        self.dataset_name = ""

    def historicalData(self, reqId, bar):
        # https: // interactivebrokers.github.io / tws - api / historical_bars.html
        # Open: Time average bid, High:	Max Ask, Low: Min Bid; Close: Time average ask
        print(f'Time: {bar.date} Open: {bar.open} High: {bar.high} Low: {bar.low} Close: {bar.close}')

        self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close])

    def historicalDataEnd(self, reqId, start, end):
        self.processing = False
        dataset = pandas.DataFrame(self.data, columns=['DateTime', 'Open', 'High', 'Low', 'Close'])
        dataset.to_csv(self.dataset_name)
        


def wait_for_request_expiration_limit(t1):
    # Check time
    t2 = time.time()
    time_since_first_request = t2 - t1

    while time_since_first_request < 650:
        time.sleep(30)
        t2 = time.time()
        time_since_first_request = t2 - t1
        print("Waiting... completed time is...", time_since_first_request)


def run_loop():
    app.run()


cmdLineParser = argparse.ArgumentParser("api tests")
cmdLineParser.add_argument("-p", "--port", action="store", type=int,
                           dest="port", default=7497, help="The TCP port to use")
args = cmdLineParser.parse_args()
print("Using args", args)

# IB allows a max of 30 requests / 10 minutes.
# If necessary, we wait for the time here
max_request_per_ten_minutes = 29

# NY Stock Exchange operates between 9:30 AM and 4:00 PM
dates = Dates()
day = '2020-07-18'
initial_date = day + 'T09:33'
final_date = day + 'T16:03'
frequency = '3T'
start_hour = '9:31'
final_hour = '16:00'
dates_list = dates.obtain_dates(initial_date, final_date, frequency, start_hour, final_hour)
print(dates_list)
print(len(dates_list))
# exit()

app = IBapi()
app.connect("127.0.0.1", args.port, 0)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(1)  # Sleep interval to allow time for connection to server

contract = Contract()
contract.symbol = "MSFT"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"
#Specify the Primary Exchange attribute to avoid contract ambiguity 
#(there is an ambiguity because there is also a MSFT contract with primary exchange = "AEB")
contract.primaryExchange = "ISLAND"

# Create contract object for FUTURES
# contract = Contract()
# contract.symbol = 'VIX'
# contract.secType = 'FUT'
# contract.exchange = 'CFE'
# contract.currency = 'USD'
# contract.LocalSymbol = "VXN0"
# contract.expiry = "20200722"
# contract.LastTradeDateOrContractMonth = "202007"
# contract.Multiplier = "1000"

whatToShow = "BID_ASK"  # "BID, ASK, MIDPOINT, TRADES"
output_name = contract.symbol + "_" + day + "_" + whatToShow + '.csv'

t1 = time.time()
app.dataset_name = output_name
for counter, date in enumerate(dates_list):
    app.processing = True
    print(date)
    app.reqHistoricalData(reqId=5001,
                          contract=contract,
                          endDateTime=date,
                          durationStr="180 S",
                          barSizeSetting="1 secs",
                          whatToShow=whatToShow,
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=["XYZ"])

    while app.processing is True:
        time.sleep(0.5)

    time.sleep(1)
    print(counter)

    if counter > 0 and counter % max_request_per_ten_minutes == 0:
        wait_for_request_expiration_limit(t1)
        t1 = time.time()


#%%
        
        
        
#%%
        
        

app.disconnect()

