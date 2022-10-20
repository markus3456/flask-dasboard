import pandas as pd
from extract import extract

ptsbm, extra, giro ,ptsbc = extract()

#print(giro)

#filter a dataframe with all transactions of the desired month
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

#generate a dataframe with transactions
def dfgen(a):
    dfd = pd.date_range(start='1/1/2022', freq='MS', periods=7)
    dfd = pd.DataFrame(dfd, columns=['date'])
    print(dfd)
    df5 = pd.DataFrame()
    b = 0
    for i in range(0,7,1):
        b = b + a
        df5 = df5.append({'balance':b}, ignore_index=True)
    df5 = pd.concat([dfd,df5], axis=1)
    return df5

#merge two dataframes
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
#mask to selcet desired range/time period
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

    dft1 = pd.merge(df3, df1[["date", "balance"]], on="date", how="left", suffixes=('_a', '_b'))
    dft2 = pd.merge(df2, df4[["date", "balance"]], on="date", how="left", suffixes=('_c', '_d'))
    dft = pd.merge(dft1, dft2[["date",  "balance_c", "balance_d"]], on="date", how="left", )

    dft = dft.fillna(method='ffill')
    dft = dft.drop(columns=[ 'text','authority','value','reference'])
    dft = dft.fillna(0)
    dft.set_axis(['date', 'giro', 'ptsbm', 'ptsbc', 'extra'], axis=1, inplace=True)
    
    #dft['total'] = dft.apply(lambda x: x['giro'] + x['ptsbm'] + x['ptsbc'] + x['extra'], axis=1)
    #dft.columns = ['date', 'giro', 'ptsbm', 'ptsbc', 'extra','total']
    print(type(dft))
    return dft



def asset2(df1,df2):
    dft = pd.merge(df1, df2[["date",  "balance"]], on="date", how="left", )
    dft = dft.fillna(method='ffill')
    dft = dft.fillna(0)
    print(dft)
    print(type(dft))
    return dft

def total(df):
    cols = ['giro','ptsbm','ptsbc','extra','balance']
    df['total'] = df[cols].sum(axis=1)
    print(df)

df1 = assetb(giro,ptsbm,ptsbc,extra,2021,2022)


a = 10000
boi = dfgen(a)
print(type(df1))

df3 = asset2(df1,boi)
print(df3)
df3 = total(df3)
print(df3)