#!/bin/python3

import math
import os
import random
import re
import sys
import pandas as pd
from abc import ABC
from collections import deque
from sklearn.neural_network import MLPClassifier

class DIRECTION:
    BUY=1
    SELL=-1
    HOLD = 0

class base_strategy(ABC):
    def predict(self):
        pass
    def fit(self,price):
        pass


#All the class strategy you will need to define will inherit from the class base_strategy
#You will need to use the inheritance for each class declaration
#Please DO NOT forget to call the constructor of the base class
#You will need to define at least 3 methods
# The constructor __init__
# The predict function
# The fit function
# The function predict will need to return either
    # DIRECTION.BUY
    # DIRECTION.SELL
    # DIRECTION.HOLD

# In all the strategies, do not forget that you will always need to start by buying

class strategy1(base_strategy):
    def __init__(self):
        self.status = DIRECTION.HOLD
        self.position = 0
        self.data = {}
    def fit(self,price):
        self.data[price['date']] = self.position
        self.position += 1
    def predict(self,price):
        if self.data[price['date']] == 0:
            self.status = DIRECTION.BUY
            return self.status
        elif self.data[price['date']] % 6 == 0 and self.status == DIRECTION.BUY:
            self.status = DIRECTION.SELL
            return self.status
        elif self.data[price['date']] % 6 == 0 and self.status == DIRECTION.SELL:
            self.status = DIRECTION.BUY
            return self.status
            
        


class strategy2(base_strategy):
    def __init__(self):
        self.mavg = deque(maxlen=20)
        self.position = 0
        self.buy = False
    def fit(self,price):
        self.mavg.append(price['price'])
        self.position += 1
     def predict(self,price):
        if self.position == 1:    
            return DIRECTION.BUY
        if self.mavg > 580 and not self.buy:
            self.buy = True
            return DIRECTION.SELL
        elif self.mavg < 579 and self.buy:
            self.buy = False
            return DIRECTION.BUY
#%%
class strategy3(base_strategy):
    def __init__(self):
        self.historical_data = pd.DataFrame(columns=['Trade','Price','OpenClose','HighLow'])
        self.prev_price = 0
        self.buy = False
    def fit(self,price_update):
        if len(self.historical_data.index)>500:
            clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
            clf.fit(X = self.historical_data[['OpenClose','HighLow']],y=self.historical_data['Trade'])
            return clf
        self.historical_data.loc[len(self.historical_data.index)] = [1 if price_update['price'] > self.prev_price else -1,
 price_update['price'],
 price_update['open']-price_update['close'],
 price_update['high'] - price_update['low']]
        self.prev_price  = price_update['price']
        
    def predict(self,price_update):
        if len(self.historical_data.index)>500:
            clf = self.fit(price_update)
            pre = clf.predict([[
 price_update['open']-price_update['close'],
 price_update['high'] - price_update['low']]])
            pre = int(pre)
            if pre == 1:
                if not self.buy:
                    self.buy = True
                    return DIRECTION.BUY
                else:
                    return DIRECTION.HOLD
            else:
                if  self.buy:
                    self.buy = False
                    return DIRECTION.SELL
                else:
                    return DIRECTION.HOLD
                




class ForLoopBackTester:
    def __init__(self,strat=None):
        self.list_position=[]
        self.list_cash=[]
        self.list_holdings = []
        self.list_total=[]

        self.long_signal=False
        self.position=0
        self.cash=100000
        self.total=0
        self.holdings=0

        self.market_data_count=0
        self.prev_price = None
        self.statistical_model = None
        self.historical_data = pd.DataFrame(columns=['Trade','Price','OpenClose','HighLow'])
        self.strategy = strat



    def onMarketDataReceived(self,price_update):
        if self.strategy:
            self.strategy.fit(price_update)
            predicted_value = self.strategy.predict(price_update)
        else:
            predicted_value = DIRECTION.HOLD

        if predicted_value==DIRECTION.BUY:
            return 'buy'
        if predicted_value==DIRECTION.SELL:
            return 'sell'
        return 'hold'

    def buy_sell_or_hold_something(self,price_update,action):
        if action == 'buy':
            cash_needed = 10 * price_update['price']
            if self.cash - cash_needed >=0:
                print(str(price_update['date']) +
                      " send buy order for 10 shares price=%.2f" % (price_update['price']))
                self.position += 10
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')


        if action == 'sell':
            position_allowed=10
            if self.position-position_allowed>=-position_allowed:
                print(str(price_update['date'])+
                      " send sell order for 10 shares price=%.2f" % (price_update['price']))
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update['price']
            else:
                print('sell impossible because not enough position')

        self.holdings = self.position * price_update['price']
        self.total = (self.holdings + self.cash)
        # print('%s total=%d, holding=%d, cash=%d' %
        #       (str(price_update['date']),self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings+self.cash)


naive_backtester = None
nb_of_rows = 0

def test1():
    global naive_backtester
    global nb_of_rows
    nb_of_rows=10
    naive_backtester = ForLoopBackTester(strategy1())

def test2():
    global naive_backtester
    global nb_of_rows
    nb_of_rows=50
    naive_backtester = ForLoopBackTester(strategy1())

def test3():
    global naive_backtester
    global nb_of_rows
    nb_of_rows=10
    naive_backtester = ForLoopBackTester(strategy2())

def test4():
    global naive_backtester
    global nb_of_rows
    nb_of_rows=150
    naive_backtester = ForLoopBackTester(strategy2())

def test5():
    global naive_backtester
    global nb_of_rows
    nb_of_rows=522
    naive_backtester = ForLoopBackTester(strategy3())



if __name__ == '__main__':
    func_name = sys.stdin.readline().strip()
    test_func = globals()[func_name]
    test_func()
    market_data_header = input().strip()
    for _ in range(nb_of_rows):
        row = input().strip().split(',')

        date=row[0]
        high=row[1]
        low = row[2]
        closep=row[4]
        openp = row[3]
        volume = row[5]
        price=row[6]

        price_information={'date' : date,
                          'price' : float(price),
                           'high' : float(high),
                           'low': float(low),
                           'close' : float(closep),
                           'open' : float(openp),
                           'volume' : float(volume)}
        action = naive_backtester.onMarketDataReceived(price_information)
        naive_backtester.buy_sell_or_hold_something(price_information,action)



    print("PNL:%.2f" % (naive_backtester.list_total[-1] - 10000))  
                
    
