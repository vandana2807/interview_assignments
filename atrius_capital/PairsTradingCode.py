import sys
import pandas as pd
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
import numpy as np
from statsmodels.tsa.stattools import coint

def zscore(series):
    return (series - series.mean()) / np.std(series)

# Enter your code here. Read input from STDIN. Print output to STDOUT
def calc_cointegration(data):
    # We will use Adj Close price
    data = data['Adj Close']
    n = data.shape[1] # dimension of the matrix
    #initiate your matrix here with value 1
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j]))
   
    
    # loop through symbols to get pairwise pvalue for cointegration test (you only need to calculate n*(n-1)/2 pvalues)
    # Please avoid hardcoding!
    return pvalue_matrix


def get_sample_data(data):
    # follow instruction and return the selected sample data
    data.set_index('Date', inplace=True)
    data=data.loc['2002-04-01':'2005-04-01']
    data=data['Adj Close'][['MSFT','JNPR']]
    return data

def signal_gen(row,data):
    #print(data['zscore'][0])
    if data['zscore'][0]<-1.0:
        return 1
    elif data['zscore'][0]>1.0:
        return -1
    else:
        return 0
def get_signal(data):
    data = get_sample_data(data)
    # You will build a new dataframe to display prices for two stocks, z_score and signals
    # check expected output for detail
    S1 = data['Adj Close']['MSFT']
    S2 = data['Adj Close']['JNPR']
    score, pvalue, _ = coint(S1, S2)
    #print(pvalue)
    ratios = S1 / S2
    z=zscore(ratios)
    # You will build a new dataframe to display prices for two stocks, z_score and signals
    # check expected output for detail
    df = pd.DataFrame(columns=['symbol1_price' ,'symbol2_price' ,'z_score' ,'signal'])
    df['symbol1_price']=data['Adj Close']['MSFT']
    df['symbol2_price']=data['Adj Close']['JNPR']
    df['zscore']=z
    df['signal']=data.apply(lambda row: signal_gen(data,row),axis=1)
    
    
    
    return df
def get_holdings(data):
    h=[]
    #print(data.loc[data.index[0],'signal'])
    for i in data.index:
        if data.loc[i,'signal'][0]==-1:
            h.append(data.loc[i,'Adj Close']['JNPR']-data.loc[i,'Adj Close']['MSFT'])
        elif data.loc[i,'signal'][0]==1:
            h.append(data.loc[i,'Adj Close']['MSFT']-data.loc[i,'Adj Close']['JNPR'])
        else:
            h.append(0)   
    return h 

def get_cash(data):
    c=[]
    ic=0
    for i in data.index:
        if data.loc[i,'signal_diff'][0]==-1:
            #print(ic-data.loc[i,'signal_diff'][0]*(data.loc[i,'Adj Close']['MSFT']-data.loc[i,'Adj Close']['JNPR']))
            c.append(ic-data.loc[i,'signal_diff'][0]*(data.loc[i,'Adj Close']['MSFT']-data.loc[i,'Adj Close']['JNPR']))
        elif data.loc[i,'signal_diff'][0]==1:
            #print(ic-data.loc[i,'signal_diff'][0]*(data.loc[i,'Adj Close']['MSFT']-data.loc[i,'Adj Close']['JNPR']))
            c.append(ic-data.loc[i,'signal_diff'][0]*(data.loc[i,'Adj Close']['MSFT']-data.loc[i,'Adj Close']['JNPR']))
        else:
            print(ic)
            c.append(ic)
        
        ic=c[-1]
        
            
    return c
def pnl(data):
    df = get_signal(data)
    # calculate performance
    df['signal_diff']=df['signal'].diff()
    
            
    
    h=get_holdings(data)
    df['holding']=h
    c=get_cash(data)
    df['cash']=c
    df['total']=df['holding']+df['cash']
    return df

    

def test_calc_cointegration(data):
    print(calc_cointegration(data))
def test_get_sample_data(data):
    print(get_sample_data(data))
def test_get_signal(data):
    print(get_signal(data))
def test_pnl(data):
    df = pnl(data)
    df['holding'] = np.where(df['holding']!=0,df['holding'],0)
    print(df)

if __name__ == '__main__':
    func_name = input().strip()
    data = pd.read_csv(sys.stdin, header=[0,1],index_col=0, parse_dates=True)
    globals()[func_name](data)
