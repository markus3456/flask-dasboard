import pandas as pd
from extract import extract

ptsbm, extra, giro ,ptsbc = extract()

#print(giro)

def mon(df,month,year):

    mask = df['date'].map(lambda x: x.month) == month   
    b = df[mask]
    df = b[b['date'].dt.year == year]
    df = df.drop(columns=[ 'text','balance',])

    sum1 = round(sum(x for x in df["value"] if x < 0),2)
    count1 = len(df.index)

    print(count1)
    print(sum1)

    return df

def asset(df1, df2, start, end):

    #start = value[0]
    #end = value[1]

    mask2 = (df1['date'].dt.year >= start) & (df1['date'].dt.year <= end)
    df1 = df1.loc[mask2]
    mask2 = (df2['date'].dt.year >= start) & (df2['date'].dt.year <= end)
    df2 = df2.loc[mask2]
    df2 = df2[df2["reference"].str.contains("No Cash Earned") == False]
    # print(df1)
    # print(df2)
    
    df3 = pd.merge(df1, df2[["date", "balance"]], on="date", how="left")
    df3 = df3.fillna(method='ffill')
    df3 = df3.drop(columns=[ 'text','authority','value','reference'])
    df3 = df3.fillna(0)
    df3['total'] = df3['balance_x'] + df3['balance_y']


    print(df3)
    return df3

def mask(df,start, end):
    mask2 = (df['date'].dt.year >= start) & (df['date'].dt.year <= end)
    df = df.loc[mask2]
    return df
    
def assetb(df1,df2,df3,df4,start,end):
    df1 = mask(df1,start,end)
    df2 = mask(df2,start,end)
    df2 = df2[df2["reference"].str.contains("No Cash Earned") == False]
    df3 = mask(df3,start,end)
    df4 = mask(df4,start,end)

    dft = pd.merge(df1, df2[["date", "balance"]], on="date", how="left")
    dft = pd.merge(dft, df3[["date", "balance"]], on="date", how="left")
    dft = pd.merge(dft, df4[["date", "balance"]], on="date", how="left")

    dft = dft.fillna(method='ffill')
    dft = dft.drop(columns=[ 'text','authority','value','reference'])
    dft = dft.fillna(0)
    dft = dft.set_axis(['date', 'giro', 'ptsbm', 'ptsbc', 'extra'], axis=1, inplace=False)
    
    dft['total'] = dft['giro'] + dft['ptsbm'] + dft['ptsbc'] + dft['extra']
    print(dft)
 







df1 = assetb(giro,ptsbm,ptsbc,extra,2021,2022)
#df2 = asset(ptsbm,ptsbc,2021,2022)


#df_mon = mon(giro,4,2022)
#print(df_mon)
    


