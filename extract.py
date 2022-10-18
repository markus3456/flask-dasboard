import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def extract():
    alchemyEngine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/finance', pool_recycle=3600);
    dbConnection = alchemyEngine.connect();

    # Read data from PostgreSQL database table and load into a DataFrame instance
    df1 = pd.read_sql("select * from \"acc1\"", dbConnection);
    df2 = pd.read_sql("select * from \"acc2\"", dbConnection);
    df3 = pd.read_sql("select * from \"acc3\"", dbConnection);
    df4 = pd.read_sql("select * from \"acc4\"", dbConnection);
    pd.set_option('display.expand_frame_repr', False);

    # Print the DataFrame
    df1 = df1.sort_values(by="date")
    df2 = df2.sort_values(by="date")
    df3 = df3.sort_values(by="date")
    df4 = df4.sort_values(by="date")

    # print(df1)
    # print(df2)
    # print(df3)
    # print(df4)

    return df1, df2 , df3 , df4

