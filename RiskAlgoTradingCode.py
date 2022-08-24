import os
import pandas as pd
import numpy as np
from statistics import stdev, mean




def histogram_weekly_losses(results):
    # create histogram for the weekly losses
    # use the folloing functions with bins=50
    weekly_losses=[]
    num_days = len(results.index)
    pnl = results['Pnl'] # depends on the column name 
    for i in range(0, num_days):
        if i >= 5 and pnl[i - 5] > pnl[i]:
            weekly_losses.append(pnl[i] - pnl[i - 5])
    weekly_losses,_= np.histogram(weekly_losses,bins=50)
    return weekly_losses




def histogram_monthly_losses(results):
    # create histogram for the monthly losses
    # use the folloing functions with bins=50
    monthly_losses=[]
    num_days = len(results.index)
    pnl = results['Pnl']
    for i in range(0, num_days):
        if i >= 20 and pnl[i - 20] > pnl[i]:
             monthly_losses.append(pnl[i] - pnl[i - 20])
    monthly_losses,_=np.histogram(monthly_losses,bins=50)
    return monthly_losses
    


def max_draw_down(results):
    #calculate max drawdown
    max_pnl = 0
    max_drawdown = 0
    drawdown_max_pnl = 0
    drawdown_min_pnl = 0
    num_days = len(results.index)
    pnl = results['Pnl']


    for i in range(num_days):
        max_pnl = max(max_pnl, pnl[i])
        drawdown = max_pnl - pnl[i]


        if drawdown > max_drawdown:
            max_drawdown = drawdown
            drawdown_max_pnl = max_pnl
            drawdown_min_pnl = pnl[i]
    return round(drawdown_max_pnl,2)




def histogram_position_holding_times(results):
    #calculate histogram for the position holding times
    position_holding_times = []
    current_pos = 0
    current_pos_start = 0
    num_days = len(results.index)
    for i in range(0, num_days):
        pos = results['Position'].iloc[i]


      # flat and starting a new position
        if current_pos == 0:
            if pos != 0:
                current_pos = pos
                current_pos_start = i
            continue


      # going from long position to flat or short position or
      # going from short position to flat or long position
        if current_pos * pos <= 0:
            current_pos = pos
            position_holding_times.append(i - current_pos_start)
            current_pos_start = i
    histogram_position_holding_times,ht=np.histogram(position_holding_times,bins=50)
    pdf=pd.DataFrame(histogram_position_holding_times,
                     index=ht[:-1],columns=["count"])
    pdf.index.name="bins"
    return pdf




def volatility_summary(results):
    # give the volatlity summary for:
    last_week = 0
    weekly_pnls = []
    weekly_losses = []
    num_days = len(results.index)
    pnl=results['Pnl']
    for i in range(0, num_days):
        if i - last_week >= 5:
            pnl_change = pnl[i] - pnl[last_week]
            weekly_pnls.append(pnl_change)
            if pnl_change < 0:
                weekly_losses.append(pnl_change)
            last_week = i
    print('PnL Standard Deviation:', stdev(weekly_pnls))
    sharpe_ratio = mean(weekly_pnls) / stdev(weekly_pnls)
    sortino_ratio = mean(weekly_pnls) / stdev(weekly_losses)
    print('Sharpe ratio:', sharpe_ratio)
    print('Sortino ratio:', sortino_ratio)
    pdf=pd.DataFrame([stdev(weekly_pnls),sharpe_ratio,sortino_ratio],
                     index=['PnL Standard Deviation','Sharpe ratio:','Sortino ratio:'],columns=['Summary'])
    return pdf




def traded_volume_summary(results):
    # calculate the total traded volume
    traded_volume = 0
    num_days = len(results.index)
    for i in range(0, num_days):
        if results['Trades'].iloc[i] != 0:
            traded_volume += abs(results['Position'].iloc[i] - results['Position'].iloc[i-1])




    print('Total traded volume:', traded_volume)
    return traded_volume


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    test_function_name = input()
    rows_num = int(input().strip())
    data = []
    colnames = list(map(str, input().rstrip().split(',')))
    for i in range(rows_num):
        line = list(map(str, input().split(',')))
        line[0] = line[0]
        line[1] = float(line[1])
        line[2] = float(line[2])
        line[3] = float(line[3])
        line[4] = float(line[4])
        line[5] = float(line[5])
        line[6] = float(line[6])
        line[7] = float(line[7])
        line[8] = float(line[8])
        line[9] = float(line[9])
        line[10] = float(line[10])
        line[11] = float(line[11])
        line[12] = float(line[12])
        line[13] = float(line[13])
        
        data.append(line)    


    results = pd.DataFrame(data, columns = colnames)
    results.index=results['Date']


    
    res=globals()[test_function_name](results)
    fptr.write(str(res))
