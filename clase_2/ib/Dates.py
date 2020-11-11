import pandas as pd


class Dates:

    def obtain_dates(self, initial_date, final_date, frequency,
                     start_hour, final_hour):

        '''  Obtain a time series of dates
            initial_date: '2016-09-02T17:30:00Z'
            final_date: '2016-09-04T21:00:00Z'
            frequency: '15T'
            start_hour: '07:00'
            final_hour: '21:00' '''

        dates = (pd.DataFrame(columns=['NULL'],
                              index=pd.date_range(initial_date,
                                                  final_date,
                                                  freq=frequency))
                 .between_time(start_hour, final_hour)
                 .index.strftime('%Y%m%d %H:%M:%S EST')  # Format is 'YYYYMMDD{SPACE}hh:mm:ss[{SPACE}TMZ]'
                 .tolist())

        return dates


### Experimental

# EST is UTC - 5 hours. America/New_York is EST in the winter and
# E*D*T in the summer, so right now New York is UTC - 4 hours.
# timezone = pytz.timezone("America/New_York")
# utc = pytz.UTC
# epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)


   # # Localize datetime
    # date_time = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
    # print("The date is", date_time)
    # # convert to UTC timezone
    # date_time = date_time.astimezone(utc)
    # print("The date (UTC) is", date_time)
    #
    # timestamp = int((date_time - epoch).total_seconds())
    # print("The timestamp is ", timestamp)
