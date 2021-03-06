""" Get CSVs from https://www.kaggle.com/mczielinski/bitcoin-historical-data
Note there's a lot of nulls in there, see my empty-handling below & determine if right way to go.
"""

import pandas as pd
import numpy as np
from data.data import engine

conn = engine.connect()

column_renames = {
    'Timestamp': 'timestamp',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Volume_(BTC)': 'volume_btc',
    'Volume_(Currency)': 'volume_currency',
    'Weighted_Price': 'weighted_price'
}

filenames = {
    'bitstamp': 'bitstampUSD_1-min_data_2012-01-01_to_2018-01-08.csv',
    'coinbase': 'coinbaseUSD_1-min_data_2014-12-01_to_2018-01-08.csv',
    'coincheck': 'coincheckJPY_1-min_data_2014-10-31_to_2018-01-08.csv'
}

for k in ['coinbase', 'coincheck', 'bitstamp']:
    filename = filenames[k]
    df = pd.read_csv(f'./bitcoin-historical-data/{filename}.csv')
    df = df.rename(columns=column_renames)

    print(f'{filename}: saving to DB')
    df.to_sql(filename, conn, if_exists='replace', chunksize=200)

    print(f'{filename}: modifying columns')
    conn.execute(f"""
    ALTER TABLE {filename} ALTER timestamp TYPE TIMESTAMP WITH TIME ZONE USING to_timestamp(timestamp) AT TIME ZONE 'UTC';
    CREATE INDEX {filename}_timestamp ON {filename} (timestamp);
    """)
    print(f'{filename}: done')
