#!/opt/python2.7/bin/python2.7
# -*- coding: utf-8 -*-

import yaml
import MySQLdb as mdb
import numpy as np
import sys
import re
import random
import subprocess
import os
import string
import pandas as pd
import datetime as dt
import time

from collections import deque
import itertools

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker

def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    resMA = []
    for i in np.arange(n-1):
        resMA.append(0.0)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        ma = s / float(n)
        resMA.append(ma)
    return resMA


def my_float_representer(dumper, value):
    text = '{0:.4f}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)

def add_mons(dt1, aMonths):
    aMons = dt1.year *12 + dt1.month - 1
    aMons = aMons + aMonths
    newdt = dt1.replace(year=aMons/12, month=aMons%12 + 1)
    return newdt

def diff_mons(dt1, dt2):
    aMons = dt1.year*12 + dt1.month - 1
    bMons = dt2.year*12 + dt2.month - 1
    return aMons - bMons

def postfix(s,*endstring):
    array = map(s.endswith,endstring)
    if True in array:
        return True
    else:
        return False

def cfg_copy(cfgFileNameIn, glb='n'):
    cfgVec = cfgFileNameIn.split("/")
    cfgFileNameVec = cfgVec[-1].split(".")
    if len(cfgFileNameVec) == 3 or len(cfgFileNameVec) == 2 or len(cfgFileNameVec) == 4:
        cfgFileName = cfgFileNameVec[-2] + "." + cfgFileNameVec[-1]
    else:
        print("The Config file name err, which should be RandHead.Datatable-cfg.yaml, Datatable-cfg.yaml or GLB.RandHead.Datatable-cfg.yaml")
        exit(-1)
    cfgDir = "output/backtest/" + cfgFileName
    mkDirStr = "[ -d " + cfgDir + " ] || mkdir " +  cfgDir
    subprocess.call(mkDirStr, shell=True)
    fileHead = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
    bktCfgFileName = fileHead + '.' + cfgFileName
    if glb == 'y' :
        bktCfgFileName = "GLB." + fileHead + '.' + cfgFileName
    newCfgFileName = cfgDir + '/' + bktCfgFileName
    cpStr = "cp -f " + cfgFileNameIn + ' ' + newCfgFileName
    subprocess.call(cpStr, shell=True)
    return [newCfgFileName, cfgDir, fileHead]

def wfo_result_analysis(fileName):
    fileSize = os.path.getsize(fileName)
    result = {"NP":0.0, "MDD":0.0, "PF":0.0, "PpT":0.0, "WR":0.0, "ShR": 0.0}
    if fileSize > 0:
        eps = 0.000001
        df = pd.read_csv(fileName, header=None, names=['date', 'time', 'price',
        'position', 'fnormpos', 'fnetreturn', 'normpos', 'netreturn'])
        df = df.dropna(how="any")

        df['netreturn'] = df['netreturn'] - df['netreturn'][0]

        numtrade = df.shape[0]
        datenum = df['date'].apply(lambda d: int(d))

        numday = len(datenum.unique())

        hands = df["normpos"].max()
        if 0 == hands:
            return result
        profits = df["netreturn"] / hands
        drawdown = profits - profits.cummax()

        # trade
        pos = df["normpos"] - df["normpos"].shift(1)
        pos[0] = df["normpos"][0]
        tradetimes = np.sum(np.abs(pos.values))
        tradetimes = tradetimes/hands

        tradeprofit = profits.diff()
        tradeprofit.iloc[0] = profits.iloc[0]
        winrate = float((tradeprofit > 0).sum()) / numtrade
        pf = tradeprofit[tradeprofit > 0].sum() / -tradeprofit[tradeprofit < 0].sum()

        # day
        dailyprofitcum = profits.groupby(datenum).last()
        dailyprofit = dailyprofitcum.diff()
        dailyprofit.iloc[0] = dailyprofitcum.iloc[0]
        dailywinrate = float((dailyprofit > 0).sum()) / numday
        dailysharpe = dailyprofit.mean() / dailyprofit.std() * (242**0.5)

        # year
        yearidx = (datenum / 10000).astype(int)
        yearlist = yearidx.unique()
        yearprofit = tradeprofit.groupby(yearidx).sum()

        netProfit = profits.iloc[-1] # net profit
        maxDrawDown = drawdown.min() # max drawdown
        numDay = numday # days
        winRate = winrate * 100 # winrate trade
        dailyWr = dailywinrate * 100 # day winrate
        dailyShr = dailysharpe # annualized daily sharpe
        PF = pf
        profitpertrade  = netProfit / tradetimes

        myDecimalNumStr = ".3f"
        netProfit       = float(format(netProfit, myDecimalNumStr))
        maxDrawDown     = float(format(maxDrawDown, myDecimalNumStr))
        PF              = float(format(PF, myDecimalNumStr))
        profitpertrade  = float(format(profitpertrade, myDecimalNumStr))
        winRate         = float(format(winrate, myDecimalNumStr))
        dailyShr        = float(format(dailyShr, myDecimalNumStr))

        result = {"NP":netProfit, "MDD":maxDrawDown, "PF":PF, "PpT":profitpertrade, "WR":winRate, "ShR": dailyShr}

    return result

def plot_wfo_result(fileName):
    fileSize    = os.path.getsize(fileName)
    monBaseTen  = 100
    yearBaseTen = 10000
    if fileSize > 0:
        df = pd.read_csv(fileName, header=None, names=['date', 'time', 'price',
        'position', 'fnormpos', 'fnetreturn', 'normpos', 'netreturn'])
        df = df.dropna(how="any")

        df['netreturn'] = df['netreturn'] - df['netreturn'][0]

        numtrade = df.shape[0]
        datenum  = df['date'].apply(lambda d: int(d))
        numday   = len(datenum.unique())
        mon_df   = datenum/100
        mon_df   = mon_df.apply(lambda d: int(d))
        num_mons = len(mon_df.unique()) 
        
        hands = df["normpos"].max()
        if 0 == hands:
            print("None of trade record")
            return -2
        profits = df["netreturn"] / hands
        drawdown = profits - profits.cummax()
        drawdown_range = np.array(profits < profits.cummax())
        close = np.array((df["price"]))
        drawdown_close = np.zeros(close.shape)
        drawdown_init_close = np.zeros(close.shape)
        min_close  = close[0]
        init_close = min_close
        for ii in np.arange(1, drawdown_range.shape[0]):
            if drawdown_range[ii] and close[ii] < min_close:
                min_close = close[ii]
                
            elif not(drawdown_range[ii]):
                min_close  = close[ii]
                init_close = min_close
            
            drawdown_close[ii] = min_close
            drawdown_init_close[ii] = init_close
        drawdown_d_close =  -drawdown / drawdown_close
        drawdown_d_init_close =  -drawdown / drawdown_init_close
        
        # trade
        pos = df["normpos"] - df["normpos"].shift(1)
        pos[0] = df["normpos"][0]
        tradetimes = np.sum(np.abs(pos.values))
        tradetimes = int(tradetimes/hands/2)
        
        tradeprofit = profits.diff()
        tradeprofit.iloc[0] = profits.iloc[0]
        #winrate = float((tradeprofit > 0).sum()) / numtrade
        #pf = tradeprofit[tradeprofit > 0].sum() / -tradeprofit[tradeprofit < 0].sum()

        # day
        dailyprofitcum      = profits.groupby(datenum).last()
        dailyprofit         = dailyprofitcum.diff()
        dailyprofit.iloc[0] = dailyprofitcum.iloc[0]
        
        dailywinrate = float((dailyprofit > 0).sum()) / numday
        dailysharpe  = dailyprofit.mean() / dailyprofit.std() * (242**0.5)
        
        isnewhigh    = dailyprofit > (dailyprofit.cummax() - 0.001)
        
        maxwindays = 0
        maxlossdays = 0
        nowdays = 0
        for x in dailyprofit.values:
            if x > 0:
                if nowdays > 0:
                    nowdays += 1
                else:
                    nowdays = 1
            if x < 0:
                if nowdays < 0:
                    nowdays -= 1
                else:
                    nowdays = -1
            maxwindays = max(maxwindays, nowdays)
            maxlossdays = min(maxlossdays, nowdays)
        daystonewhigh = 0
        nowdays = 0
        for x in isnewhigh.values:
            if x:
                nowdays = 0
            else:
                nowdays += 1
            daystonewhigh = max(daystonewhigh, nowdays + 1)
        
        # month
        monIdx = (datenum / monBaseTen).astype(int)

        # year
        yearIdx = (datenum / yearBaseTen).astype(int)

        netProfit   = profits.iloc[-1] # net profit
        maxDrawDown = drawdown.min() # max drawdown
        tradeTimes  = tradetimes
        numDay      = numday # days
        dailyWr     = dailywinrate * 100 # day winrate
        dailyShr    = dailysharpe # annualized daily sharpe
        dailyStd    = dailyprofit.std()
        PpT         = netProfit / tradetimes
        dailyMaxProfit = dailyprofit.max()
        dailyMinProfit = dailyprofit.min()
        maxWinDays     = int(maxwindays)
        maxLossDays    = int(-maxlossdays)
        daysToNewHigh  = int(daystonewhigh)
        
        ind1 = 'NP = {}'.format('%.1f'%(netProfit))
        ind2 = 'MDD = {}'.format('%.1f'%(maxDrawDown))
        ind3 = 'PpT = {}'.format('%.1f'%(PpT))
        ind4 = 'TT = {}'.format('%.0f'%(tradeTimes))
        ind5 = 'ShR = {}'.format('%.1f'%(dailyShr))
        ind6 = 'Days = {}'.format('%.0f'%(numDay))
        ind7 = 'D_WR = {}'.format('%.1f'%(dailyWr))
        ind8 = 'D_STD = {}'.format('%.1f'%(dailyStd))
        ind9 = 'D_MaxNP = {}'.format('%.1f'%(dailyMaxProfit))
        ind10 = 'D_MinNP = {}'.format('%.1f'%(dailyMinProfit))
        ind11 = 'maxW_Days = {}'.format('%.0f'%(maxWinDays))
        ind12 = 'maxL_Days = {}'.format('%.0f'%(maxLossDays))
        
        ind13 = 'mDD_mC = {}'.format('%.2f'%(drawdown_d_close.max()))
        ind14 = 'mDD_iC = {}'.format('%.2f'%(drawdown_d_init_close.max()))
        
        max_drawdown_d_close_id = drawdown_d_close[drawdown_d_close == drawdown_d_close.max()]
        max_drawdown_d_init_close_id = drawdown_d_init_close[drawdown_d_init_close == drawdown_d_init_close.max()]
               
        fig = plt.figure(figsize=(44,20))
        #title = fileName.split('/')
        #plt.title(title[-1])
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        plt.fill_between(df.index, 0, drawdown, facecolor='red',   color='red')
        plt.fill_between(df.index, 0, profits,  facecolor='green', color='green')
        
        fsize = 20
        monIdxDiff = monIdx.diff()
        monIdxDiff[0] = 1
        monIdxDiff.iloc[df.index[-1]] = 1
        xind = monIdxDiff[monIdxDiff > 0].index
        nowsum  = 0
        xT = []
        yT = []
        ymax = profits.values.max()
        ymin = profits.values.min()
        for x in xind.values :
            ptd = profits.values[x]
            y = ptd - nowsum
            
            if y > 0:
                bbox_props = dict(boxstyle='round', ec='none', fc='#F4F4F4', alpha=0.7)
                plt.text(x, profits.values[x]/2, float(format(y, '.2f')), size=fsize, bbox=bbox_props, color='#000000')
            else:
                bbox_props = dict(boxstyle='round', ec='none', fc='#F4F4F4', alpha=0.7)
                plt.text(x, drawdown.values[x]/2, float(format(y, '.2f')), size=fsize, bbox=bbox_props, color='#000000')
            
            xT.append(x)
            yT.append(str(datenum.values[x]))
            nowsum = ptd
        plt.xticks(xT, yT)
        plt.tick_params(labelsize=fsize)
        
        for ii in np.arange(max_drawdown_d_close_id.index.shape[0]):
            x = max_drawdown_d_close_id.index[ii]
            bbox_props = dict(boxstyle='round', ec='none', fc='r', alpha=0.5)
            plt.text(x, profits.max()/2, "mDD_mC", size=fsize, bbox=bbox_props, color='#000000')
            
        for ii in np.arange(max_drawdown_d_init_close_id.index.shape[0]):
            x = max_drawdown_d_init_close_id.index[ii]
            bbox_props = dict(boxstyle='round', ec='none', fc='b', alpha=0.5)
            plt.text(x, profits.max()/2, "mDD_iC", size=fsize, bbox=bbox_props, color='#000000')
            
        fsize = 20
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box1 = TextArea(ind1, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box2 = TextArea(ind2, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='b', fc='none')
        box3 = TextArea(ind3, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='c', fc='none')
        box4 = TextArea(ind4, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='m', fc='none')
        box5 = TextArea(ind5, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='y', fc='none')
        box6 = TextArea(ind6, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box7 = TextArea(ind7, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box8 = TextArea(ind8, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='b', fc='none')
        box9 = TextArea(ind9, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='c', fc='none')
        box10 = TextArea(ind10, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='m', fc='none')
        box11 = TextArea(ind11, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='y', fc='none')
        box12 = TextArea(ind12, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box13 = TextArea(ind13, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box14 = TextArea(ind14, textprops=dict(size=fsize, bbox=bbox_props))
        
        box = HPacker(children=[box1, box2, box13, box14, box3, box4, box5, box6,
                                box7, box8, box9, box10, box11, box12],
                          pad=0, sep=fsize-5)
        
        ax = plt.gca()
        anchored_box = AnchoredOffsetbox(loc=2, child=box, pad=0.2, frameon=False)
        ax.add_artist(anchored_box)

        ax.grid(True)
        ax.autoscale_view()
        fig.autofmt_xdate()

        figname = fileName + '.png'
        plt.savefig(figname)
        plt.close()

        return 0
    else :
        print("The %s Backtest result is empty!"%(fileName))
        return -1

def plot_wfo_leverage_result(fileName, stop_loss, point_value):
    fileSize    = os.path.getsize(fileName)
    monBaseTen  = 100
    yearBaseTen = 10000
    indicator_list = []
    if fileSize > 0:
        df = pd.read_csv(fileName, header=None, names=['date', 'time', 'price',
        'position', 'fnormpos', 'fnetreturn', 'normpos', 'netreturn'])
        df = df.dropna(how="any")

        df['netreturn'] = df['netreturn'] - df['netreturn'][0]

        numtrade = df.shape[0]
        datenum = df['date'].apply(lambda d: int(d))
        numday = len(datenum.unique())
        mon_df   = datenum/100
        mon_df   = mon_df.apply(lambda d: int(d))
        num_mons = len(mon_df.unique()) 
        
        hands = df["normpos"].max()
        if 0 == hands:
            print("None of trade record")
            return -2
        profits = df["netreturn"] / hands
        drawdown = profits - profits.cummax()
        drawdown_range = np.array(profits < profits.cummax())
        close = np.array((df["price"]))
        drawdown_close = np.zeros(close.shape)
        drawdown_init_close = np.zeros(close.shape)
        min_close  = close[0]
        init_close = min_close
        for ii in np.arange(1, drawdown_range.shape[0]):
            if drawdown_range[ii] and close[ii] < min_close:
                min_close = close[ii]
                
            elif not(drawdown_range[ii]):
                min_close  = close[ii]
                init_close = min_close
            
            drawdown_close[ii] = min_close
            drawdown_init_close[ii] = init_close
        drawdown_d_close = -drawdown / (drawdown_close * point_value)
        drawdown_d_init_close = -drawdown / (drawdown_init_close * point_value)
        leverage = stop_loss / drawdown_d_init_close.max()
        # trade
        pos = df["normpos"] - df["normpos"].shift(1)
        pos[0] = df["normpos"][0]
        tradetimes = np.sum(np.abs(pos.values))
        tradetimes = int(tradetimes/hands/2)
        
        tradeprofit = profits.diff()
        tradeprofit.iloc[0] = profits.iloc[0]
        #winrate = float((tradeprofit > 0).sum()) / numtrade
        #pf = tradeprofit[tradeprofit > 0].sum() / -tradeprofit[tradeprofit < 0].sum()

        # day
        dailyprofitcum      = profits.groupby(datenum).last()
        dailyprofit         = dailyprofitcum.diff()
        dailyprofit.iloc[0] = dailyprofitcum.iloc[0]
        
        dailywinrate = float((dailyprofit > 0).sum()) / numday
        dailysharpe  = dailyprofit.mean() / dailyprofit.std() * (242**0.5)
        
        isnewhigh    = dailyprofit > (dailyprofit.cummax() - 0.001)
        
        maxwindays = 0
        maxlossdays = 0
        nowdays = 0
        for x in dailyprofit.values:
            if x > 0:
                if nowdays > 0:
                    nowdays += 1
                else:
                    nowdays = 1
            if x < 0:
                if nowdays < 0:
                    nowdays -= 1
                else:
                    nowdays = -1
            maxwindays = max(maxwindays, nowdays)
            maxlossdays = min(maxlossdays, nowdays)
        daystonewhigh = 0
        nowdays = 0
        for x in isnewhigh.values:
            if x:
                nowdays = 0
            else:
                nowdays += 1
            daystonewhigh = max(daystonewhigh, nowdays + 1)
        
        # month
        monIdx = (datenum / monBaseTen).astype(int)
        monIdxDiff = monIdx.diff()
        monIdxDiff.loc[0]  = 1
        monIdxDiff.loc[df.index[-1]] = 1
        xind = monIdxDiff[monIdxDiff > 0].index
        # year
        yearIdx = (datenum / yearBaseTen).astype(int)

        netProfit   = profits.iloc[-1] # net profit
        maxDrawDown = drawdown.min() # max drawdown
        tradeTimes  = tradetimes
        numDay      = numday # days
        dailyWr     = dailywinrate * 100 # day winrate
        dailyShr    = dailysharpe # annualized daily sharpe
        dailyStd    = dailyprofit.std()
        PpT         = netProfit / tradetimes
        dailyMaxProfit = dailyprofit.max()
        dailyMinProfit = dailyprofit.min()
        maxWinDays     = int(maxwindays)
        maxLossDays    = int(-maxlossdays)
        daysToNewHigh  = int(daystonewhigh)
        
        ind1 = 'NP = {}'.format('%.1f'%(netProfit))
        ind2 = 'MDD = {}'.format('%.1f'%(maxDrawDown))
        ind3 = 'PpT = {}'.format('%.1f'%(PpT))
        ind4 = 'TT = {}'.format('%.0f'%(tradeTimes))
        ind5 = 'ShR = {}'.format('%.1f'%(dailyShr))
        ind6 = 'Days = {}'.format('%.0f'%(numDay))
        ind7 = 'D_WR = {}'.format('%.1f'%(dailyWr))
        ind8 = 'D_STD = {}'.format('%.1f'%(dailyStd))
        ind9 = 'D_MaxNP = {}'.format('%.1f'%(dailyMaxProfit))
        ind10 = 'D_MinNP = {}'.format('%.1f'%(dailyMinProfit))
        ind11 = 'maxW_Days = {}'.format('%.0f'%(maxWinDays))
        ind12 = 'maxL_Days = {}'.format('%.0f'%(maxLossDays))
        
        ind13 = 'mDD_mC = {}'.format('%.2f'%(drawdown_d_close.max()))
        ind14 = 'mDD_iC = {}'.format('%.2f'%(drawdown_d_init_close.max()))
        ind15 = 'LVRG = {}'.format('%.2f'%(leverage))
        ind16 = 'LVRG_Mon_NP = {}'.format('%.2f'%(leverage * netProfit / num_mons))
        ####
        indicator_list.append(fileName.split('/')[-1])
        indicator_list.append(netProfit)
        indicator_list.append(maxDrawDown)
        indicator_list.append(PpT)
        indicator_list.append(drawdown_d_init_close.max())
        indicator_list.append(leverage)
        indicator_list.append((leverage * netProfit / num_mons))
        indicator_list.append(tradeTimes)
        indicator_list.append(dailyShr)
        indicator_list.append(numDay)
        ####
        max_drawdown_d_close_id = drawdown_d_close[drawdown_d_close == drawdown_d_close.max()]
        max_drawdown_d_init_close_id = drawdown_d_init_close[drawdown_d_init_close == drawdown_d_init_close.max()]
               
        fig = plt.figure(figsize=(44,20))
        #title = fileName.split('/')
        #plt.title(title[-1])
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        plt.fill_between(df.index, 0, drawdown, facecolor='red',   color='red')
        plt.fill_between(df.index, 0, profits,  facecolor='green', color='green')
        
        fsize = 20
        nowsum = 0
        xT = []
        yT = []
        ymax = profits.values.max()
        ymin = profits.values.min()
        for x in xind.values :
            ptd = profits.values[x]
            y = ptd - nowsum
            
            if y > 0:
                bbox_props = dict(boxstyle='round', ec='none', fc='#F4F4F4', alpha=0.7)
                plt.text(x, profits.values[x]/2, float(format(y, '.2f')), size=fsize, bbox=bbox_props, color='#000000')
            else:
                bbox_props = dict(boxstyle='round', ec='none', fc='#F4F4F4', alpha=0.7)
                plt.text(x, drawdown.values[x]/2, float(format(y, '.2f')), size=fsize, bbox=bbox_props, color='#000000')
            
            xT.append(x)
            yT.append(str(datenum.values[x]))
            nowsum = ptd
        plt.xticks(xT, yT)
        plt.tick_params(labelsize=fsize)
        
        for ii in np.arange(max_drawdown_d_close_id.index.shape[0]):
            x = max_drawdown_d_close_id.index[ii]
            bbox_props = dict(boxstyle='round', ec='none', fc='r', alpha=0.5)
            plt.text(x, profits.max()/2, "mDD_mC", size=fsize, bbox=bbox_props, color='#000000')
            
        for ii in np.arange(max_drawdown_d_init_close_id.index.shape[0]):
            x = max_drawdown_d_init_close_id.index[ii]
            bbox_props = dict(boxstyle='round', ec='none', fc='b', alpha=0.5)
            plt.text(x, profits.max()/2, "mDD_iC", size=fsize, bbox=bbox_props, color='#000000')
            
        fsize = 20
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box1 = TextArea(ind1, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box2 = TextArea(ind2, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='b', fc='none')
        box3 = TextArea(ind3, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='c', fc='none')
        box4 = TextArea(ind4, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='m', fc='none')
        box5 = TextArea(ind5, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='y', fc='none')
        box6 = TextArea(ind6, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box7 = TextArea(ind7, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box8 = TextArea(ind8, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='b', fc='none')
        box9 = TextArea(ind9, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='c', fc='none')
        box10 = TextArea(ind10, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='m', fc='none')
        box11 = TextArea(ind11, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='y', fc='none')
        box12 = TextArea(ind12, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='g', fc='none')
        box13 = TextArea(ind13, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='r', fc='none')
        box14 = TextArea(ind14, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='b', fc='none')
        box15 = TextArea(ind15, textprops=dict(size=fsize, bbox=bbox_props))
        bbox_props = dict(boxstyle='round', ec='c', fc='none')
        box16 = TextArea(ind16, textprops=dict(size=fsize, bbox=bbox_props))
        
        box = HPacker(children=[box1, box2, box13, box14, box15, box16, box3, box4, box5, box6,
                                box7, box8, box9, box10, box11, box12],
                          pad=0, sep=fsize-5)
        
        ax = plt.gca()
        anchored_box = AnchoredOffsetbox(loc=2, child=box, pad=0.2, frameon=False)
        ax.add_artist(anchored_box)

        ax.grid(True)
        ax.autoscale_view()
        fig.autofmt_xdate()

        figname = fileName + '.png'
        plt.savefig(figname)
        plt.close()

        return indicator_list
    else :
        print("The %s Backtest result is empty!"%(fileName))
        return indicator_list

def pbs_wfo_workload_submit(cfgFileNameIn, numP):

    [newCfgFileName, cfgDir, fileHead] = cfg_copy(cfgFileNameIn)

    if numP < 2:
        numP = 2
        print("The num of strategies run in parallel less than 1, \nwhich should Greater than or Equal to 1\n")
        print("It's has been assigned 1")

    if numP > 16:
        numP = 16
    np    = 4
    nodes = (numP-1)/np+1
    ppn   = (numP-1)/nodes+1

    pbsStr  = "#!/bin/bash \n"
    pbsStr += "#PBS -N WFO_job \n"
    pbsStr += "#PBS -o " + cfgDir + "/" + fileHead + ".job.log \n"
    pbsStr += "#PBS -e " + cfgDir + "/" + fileHead + ".job.err \n"
    pbsStr += "#PBS -q TianGou \n"
    pbsStr += "#PBS -l nodes=" + str(nodes) + ":ppn=" + str(ppn) + "\n"
    pbsStr += "cd " + os.getcwd() + "\n"

    pbsStr += "NPROCS=`wc -l < $PBS_NODEFILE`" + "\n"
    pbsStr += "/usr/lib64/mpich/bin/mpiexec.hydra -hostfile $PBS_NODEFILE -n $NPROCS ./optimization_parallel " + newCfgFileName + "\n"
    pbsStr += "./backtest " + newCfgFileName + "\n"
    pbsStr += "./yamlDump.py " + newCfgFileName + "\n"

    pbsFile = "input/batch_submit" + "/" + fileHead + ".PBS_wfo.pbs"
    pbsStream = open(pbsFile, "w")
    pbsStream.write(pbsStr)
    pbsStream.close()

    subprocess.call("qsub %s"%(pbsFile) , shell=True)

def srun_wfo_workload_submit(cfgFileNameIn, numP):

    [newCfgFileName, cfgDir, fileHead] = cfg_copy(cfgFileNameIn)

    if numP < 2:
        numP = 2
        print("The num of strategies run in parallel less than 1, \nwhich should Greater than or Equal to 1\n")
        print("It's has been assigned 1")
    ntasks             = numP
    core_per_task      = 4
    max_tasks_per_node = 6
    nnodes             = (ntasks-1)/max_tasks_per_node + 1
    ntasks             = nnodes * max_tasks_per_node

    partnStr  = " PAC "
    optSH     = "TH_opt_wfo.sh"
    bktSH     = "TH_bkt_wfo.sh"

    #outStr = cfgDir + "/" + fileHead + ".$SLURM_JOB_ID" + ".opt.log "
    #errStr = cfgDir + "/" + fileHead + ".$SLURM_JOB_ID" + ".opt.err "
    #
    #oSrunStr  = "#!/bin/bash \n"
    #oSrunStr += "#SBATCH -p " + partnStr + "\n"
    #oSrunStr += "#SBATCH -o " + "output/log/" + fileHead + ".log" + "\n"
    #oSrunStr += "#SBATCH -e " + "output/log/" + fileHead + ".err" + "\n"
    #oSrunStr += "#SBATCH -D " + os.getcwd() + "\n"
    #oSrunStr += "#SBATCH -N " + str(nnodes) + "\n"
    #oSrunStr += "yhbatch -d afterok:$SLURM_JOB_ID " + bktSH + "\n"
    #
    #oSrunStr += "cd " + os.getcwd() + "\n"
    #oSrunStr += "yhrun " + " -n " + str(ntasks) + " -c " + str(core_per_task) + " -o " + outStr + " -e " + errStr
    #oSrunStr += " ./optimization_parallel " + newCfgFileName + "\n"
    #
    #srunStream = open(optSH, "w")
    #srunStream.write(oSrunStr)
    #srunStream.close()
    #
    #outStr = cfgDir + "/" + fileHead + ".$SLURM_JOB_ID" + ".bkt.log "
    #errStr = cfgDir + "/" + fileHead + ".$SLURM_JOB_ID" + ".bkt.err "
    #
    #bSrunStr  = "#!/bin/bash \n"
    #bSrunStr += "#SBATCH -p " + partnStr + "\n"
    #bSrunStr += "#SBATCH -o " + "output/log/" + fileHead + ".log" + "\n"
    #bSrunStr += "#SBATCH -e " + "output/log/" + fileHead + ".err" + "\n"
    #bSrunStr += "#SBATCH -D " + os.getcwd() + "\n"
    #bSrunStr += "#SBATCH -N " + str(1) + "\n"
    #bSrunStr += "yhrun " + " -n 1 " + " -o " + outStr + " -e " + errStr
    #bSrunStr += " ./backtest " + newCfgFileName + "\n"
    #bSrunStr += "yhrun " + " -n 1 " + " -o " + outStr + " -e " + errStr
    #bSrunStr += " python ./yamlDump.py " + newCfgFileName + "\n"
    #
    #srunStream = open(bktSH, "w")
    #srunStream.write(bSrunStr)
    #srunStream.close()

    outStr = cfgDir + "/" + fileHead + ".$SLURM_JOB_ID"

    oSrunStr  = "#!/bin/bash \n"
    oSrunStr += "#SBATCH -p " + partnStr + "\n"
    oSrunStr += "#SBATCH -o " + cfgDir + "/" + fileHead + ".log" + "\n"
    oSrunStr += "#SBATCH -e " + cfgDir + "/" + fileHead + ".err" + "\n"
    oSrunStr += "#SBATCH -D " + os.getcwd() + "\n"
    oSrunStr += "#SBATCH -N " + str(1) + "\n"
    oSrunStr += "touch " + outStr + "\n"
    oSrunStr += "cd " + os.getcwd() + "\n"
    oSrunStr += "yhrun " + " -n " + str(6) + " -c " + str(core_per_task)
    oSrunStr += " ./optimization_parallel " + newCfgFileName + "\n"

    oSrunStr += "yhrun " + " -n 1 "
    oSrunStr += " ./backtest " + newCfgFileName + "\n"
    oSrunStr += "yhrun " + " -n 1 "
    oSrunStr += " python ./yamlDump.py " + newCfgFileName + "\n"

    srunOptFile = "input/batch_submit" + "/" + fileHead + "." + optSH
    srunStream = open(srunOptFile, "w")
    srunStream.write(oSrunStr)
    srunStream.close()

    exeStr = "yhbatch %s"%(srunOptFile)

    subprocess.call(exeStr , shell=True)
