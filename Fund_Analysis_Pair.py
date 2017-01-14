# -*- coding: utf-8 -*-
"""
This is the main file to get all major financial ratio and rolling ratio and other important graph
"""
import os
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as put
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF


from pylab import rcParams
rcParams['figure.figsize'] = 18, 12
# pd.options.display.float_format = '{:.3f}%'.format


if __name__ == '__main__':
    ### Change working directory
    # Get working directory
    os.getcwd()
    # Set working director
    data_file_path = r'C:\Users\ZFang\Desktop\TeamCo\Pair Comparison\\'
    os.chdir(data_file_path)
    ### Read the file
    df_data = put.concat_data('portfolio_fund.xlsx')
    df_data_other = put.concat_data('other_fund.xlsx')
    ### Define constant variable
    # Initial value for static ratio calculation
    target_year = ['1_Year','3_Year','5_Year','7_Year','Since Inception']
    benchmark = 0.02 # Benchmark is the risk free return
    threshold = 0 # Threshold for downside deviation - also for sortino ratio
    MAR = 0 # Minimum Accept Return
    market_index = df_data.columns[-1] # For Beta and correlation
    summary_columns = ['Batting Average', 'Omega Ratio', 'Up Months', 'Down Months', 'Slugging Ratio', 'Up-Capture Russell', 'Down-Capture Russell']
    index_name = df_data.columns[1:-1] # No Date and Market Index
    index_name_2 = df_data.columns[0:-1] # No Market Index
    index_name_2_other = df_data_other.columns[0:-1] # No Market Index
    index_name_3 = df_data.columns[1:] # No Date
    columns_name = df_data.columns[1:] # No Date
    columns_name_other = df_data_other.columns[1:] # No Date
    # Initial value for rolling data calculation
    window_length = 36 # rolling window is 36 months
    min_periods = 36 # We only take complete 36 month period into consideration
    window_length_corr = 12
    min_periods_corr = 12
    
    ### Calculate Annulized Return
    Annulized_Return_df = r.annulized_return_table(df_data, index_name, target_year)
    ### Calculate Calendar Return
    Calendar_Return_df = r.calendar_return_table(df_data, index_name_2)
    Calendar_Return_df_other = r.calendar_return_table(df_data_other, index_name_2_other)
    ### Calculate Downside Deviation, given order of two
    Downside_Deviation_df = r.downside_std_table(df_data, index_name, threshold, target_year)
    ### Calculate Sortino ratio
    Sortino_df = r.sortino_ratio_table(df_data, index_name, MAR, threshold, target_year)
    ### Calculate Sharp ratio
    Sharpe_df=r.sharpe_ratio_table(df_data, index_name, benchmark, target_year)
    ### Standard Deviation
    Standard_deviation_df = r.standard_deviation_table(df_data, index_name, target_year)
    ### Beta matrix
    Beta_df = r.beta_table(df_data, index_name_3, target_year, condition = None)
    ### Positive Beta matrix
    Beta_df_p = r.beta_table(df_data, index_name_3, target_year, condition = 'Positive')
    ### Non Negative Beta matrix
    Beta_df_np = r.beta_table(df_data, index_name_3, target_year, condition = 'Non-positive')
    ### Omega Ratio
    Omega_df = r.omega_ratio_table(df_data, index_name, MAR, target_year)
    ### Correlation table
    Corr_df = r.corr_table(df_data, index_name_3, market_index, target_year, condition = None)
    ### Positive Correlation table
    Corr_df_p = r.corr_table(df_data, index_name_3, market_index, target_year, condition='Positive')
    ### Positive Correlation table
    Corr_df_np = r.corr_table(df_data, index_name_3, market_index, target_year, condition='Non-positive')    
    ### Summary table
    Summary_table_df = r.summary_table(df_data,index_name, summary_columns, market_index, MAR)

    ### Rolling beta
    rolling_beta_df = m.rolling_beta(df_data, columns_name, window_length, min_periods)
    ### Rolling annulized return
    rolling_annual_return_df = m.rolling_annulized_return(df_data, columns_name, window_length, min_periods)
    ### Cummulative return
    cum_return_df = m.cumulative_return(df_data, columns_name, window_length, min_periods)
    cum_return_df_other = m.cumulative_return(df_data_other, columns_name_other, window_length, min_periods)
    ### Rolling sortino ratio
    rolling_sortino_ratio_df = m.rolling_sortino_ratio(df_data, columns_name, window_length, min_periods, MAR, threshold)
    ### Rolling omega ratio
    rolling_omega_ratio_df = m.rolling_omega_ratio(df_data, columns_name, window_length, min_periods, MAR)
    ### Rolling sharp ratio
    rolling_sharpe_ratio_df = m.rolling_sharpe_ratio(df_data, columns_name, window_length, min_periods, benchmark)
    ### Rolling alpha
    rolling_alpha_df = m.rolling_alpha(df_data, columns_name, window_length, min_periods)
    ### Rolling correlation
    rolling_corr_df = m.rolling_corr(df_data, columns_name, market_index, window_length_corr, min_periods_corr)
   
    ### Calculate the correlation with other fund's mean return
    # Modify the market data, replace it with mean of other fund's return
    df_data_corr = df_data.copy()
    df_data_corr['Russell 3000'] = df_data_other.mean(axis=1) # replace with population mean    
    final_cum_return = cum_return_df_other.iloc[-1,:-1]
    
    quantile = pd.qcut(final_cum_return.T,4, labels=['Q1','Q2','Q3','Q4'])
    Q1 = quantile[quantile.values == 'Q1'].index
    Q2 = quantile[quantile.values == 'Q2'].index
    Q3 = quantile[quantile.values == 'Q3'].index
    Q4 = quantile[quantile.values == 'Q4'].index 
    df_data_Q1 = df_data.copy()
    df_data_Q1['Russell 3000'] = df_data_other[Q1].mean(axis=1)
    df_data_Q2 = df_data.copy()
    df_data_Q2['Russell 3000'] = df_data_other[Q2].mean(axis=1)
    df_data_Q3 = df_data.copy()
    df_data_Q3['Russell 3000'] = df_data_other[Q3].mean(axis=1)
    df_data_Q4 = df_data.copy()
    df_data_Q4['Russell 3000'] = df_data_other[Q4].mean(axis=1)
    
    # Calculate the Rolling Correlation with all funds and different quartile
    rolling_corr_df_other = m.rolling_corr(df_data_corr, columns_name, market_index, window_length_corr, min_periods_corr)
    rolling_corr_df_Q1 = m.rolling_corr(df_data_Q1, columns_name, market_index, window_length_corr, min_periods_corr)
    rolling_corr_df_Q2 = m.rolling_corr(df_data_Q2, columns_name, market_index, window_length_corr, min_periods_corr)
    rolling_corr_df_Q3 = m.rolling_corr(df_data_Q3, columns_name, market_index, window_length_corr, min_periods_corr)
    rolling_corr_df_Q4 = m.rolling_corr(df_data_Q4, columns_name, market_index, window_length_corr, min_periods_corr)
    
    
    ### Plotly Table ###
    py.sign_in('fzn0728', '1enskD2UuiVkZbqcMZ5K')
    ## py.sign_in('fzn07289', 'TMIrmI4FoHE7W5VHKgTQ')
    # Annual Return Table
    Annulized_Return_df = round(100*Annulized_Return_df,2)
    table_Annulized_Return = FF.create_table(Annulized_Return_df, index=True)
    py.plot(table_Annulized_Return, filename='Table 1 Annualized Return')
    # Annual Return Plot
    trace1 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=100*rolling_annual_return_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=100*rolling_annual_return_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=100*rolling_annual_return_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=100*rolling_annual_return_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Annual Return of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Annualized Return',
            ticksuffix='%')
        )
    fig_1 = go.Figure(data=data, layout=layout)
    plot_url_1 = py.plot(fig_1, filename='Figure 1 Rolling Annual Return of Portfolio Funds', sharing='public')
    # Annualized Return Plot #
    trace0=go.Box(
        y = 100*Annulized_Return_df.ix[:,'1_Year'].values,
        name = '1_Year',
        showlegend=False
                  )
    trace1=go.Box(
        y = 100*Annulized_Return_df.ix[:,'3_Year'],
        name = '3_Year',
        showlegend=False
              )    
    trace2=go.Box(
        y = 100*Annulized_Return_df.ix[:,'5_Year'],
        name = '5_Year',
        showlegend=False
                  )    
    trace3=go.Box(
        y = 100*Annulized_Return_df.ix[:,'7_Year'],
        name = '7_Year',
        showlegend=False
                  )    
    trace4=go.Box(
        y = 100*Annulized_Return_df.ix[:,'Since Inception'],
        name = 'Since Inception',
        showlegend=False
                  )
    trace10=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['A'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'A'
        )
    trace11=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['B'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'B'
        )
    trace12=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['C'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'C'
        )
    trace13=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['D'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'D'
        )
    trace14=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['E'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'E'
        )
    trace15=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['F'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'F'
        )
    trace16=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['G'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'G'
        )
    trace17=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['H'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'H'
        )
    trace18=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['I'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'I'
        )
    trace19=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['J'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'J'
        )
    trace20=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['I'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'X'
        )
    trace21=go.Scatter(
        x = Annulized_Return_df.T.index,
        y = 100*Annulized_Return_df.ix['J'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'XX'
        )
    data = [trace0,trace1,trace2,trace3,trace4,trace10,trace11,trace12,trace13,\
            trace14,trace15,trace16,trace17,trace18,trace19,trace20,trace21]
    layout = go.Layout(
        title='Annulized Return of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Annulized Return',
            ticksuffix='%')
        )
    fig_2 = go.Figure(data=data, layout=layout)
    plot_url_2 = py.plot(fig_2, filename='Figure 2 Annulized Return of Portfolio Funds')    

    # Calendar Return Table
    Calendar_Return_df = round(100*Calendar_Return_df,2)
    table_Calendar_Return = FF.create_table(Calendar_Return_df, index=True)
    py.plot(table_Calendar_Return, filename='Table 2 Calendar Return of Portfolio Funds')    
    # Calendar Return Plot #
    trace0=go.Box(
        y = 100*Calendar_Return_df.ix[:,2007].values,
        name = '2007',
        showlegend=False
                  )
    trace1=go.Box(
        y = 100*Calendar_Return_df.ix[:,2008],
        name = '2008',
        showlegend=False
              )    
    trace2=go.Box(
        y = 100*Calendar_Return_df.ix[:,2009],
        name = '2009',
        showlegend=False
                  )    
    trace3=go.Box(
        y = 100*Calendar_Return_df.ix[:,2010],
        name = '2010',
        showlegend=False
                  )    
    trace4=go.Box(
        y = 100*Calendar_Return_df.ix[:,2011],
        name = '2011',
        showlegend=False
                  )    
    trace5=go.Box(
        y = 100*Calendar_Return_df.ix[:,2012],
        name = '2012',
        showlegend=False
                  )    
    trace6=go.Box(
        y = 100*Calendar_Return_df.ix[:,2013],
        name = '2013',
        showlegend=False
                  )    
    trace7=go.Box(
        y = 100*Calendar_Return_df.ix[:,2014],
        name = '2014',
        showlegend=False
                  )
    trace8=go.Box(
        y = 100*Calendar_Return_df.ix[:,2015],
        name = '2015',
        showlegend=False
                  )
    trace9=go.Box(
        y = 100*Calendar_Return_df.ix[:,2016],
        name = '2016',
        showlegend=False
                  )
    trace10=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['A'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'A'
        )
    trace11=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['B'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'B'
        )
    trace12=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['C'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'C'
        )
    trace13=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['D'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'D'
        )
    trace14=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['E'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'E'
        )
    trace15=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['F'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'F'
        )
    trace16=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['G'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'G'
        )
    trace17=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['H'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'H'
        )
    trace18=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['I'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'I'
        )
    trace19=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = 100*Calendar_Return_df.ix['J'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'J'
        )
    data = [trace0,trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,\
            trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16,\
            trace17,trace18,trace19]
    layout = go.Layout(
        title='Calendar Return of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Calendar Return',
            ticksuffix='%')
        )
    fig_3 = go.Figure(data=data, layout=layout)
    plot_url_3 = py.plot(fig_3, filename='Figure 3 Calendar Return of Portfolio Funds')
    # Other Funds' Calendar Return
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, 10)]

    trace10=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2007].values,
        name = '2007',
        marker=dict(
                    color=c[0]
                    )
                  )
    trace11=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2008],
        name = '2008',
        marker=dict(
                    color=c[1]
                    )
              )    
    trace12=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2009],
        name = '2009',
        marker=dict(
                    color=c[2]
                    )
                  )    
    trace13=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2010],
        name = '2010',
        marker=dict(
                    color=c[3]
                    )
                  )    
    trace14=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2011],
        name = '2011',
        marker=dict(
                    color=c[4]
                    )
                  )    
    trace15=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2012],
        name = '2012',
        marker=dict(
                    color=c[5]
                    )
                  )    
    trace16=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2013],
        name = '2013',
        marker=dict(
                    color=c[6]
                    )
                  )    
    trace17=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2014],
        name = '2014',
        marker=dict(
                    color=c[7]
                    )
                  )
    trace18=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2015],
        name = '2015',
        marker=dict(
                    color=c[8]
                    )
                  )
    trace19=go.Box(
        y = 100*Calendar_Return_df_other.ix[:,2016],
        name = '2016',
        marker=dict(
                    color=c[9]
                    )
                  )
    data = [trace10,trace11,trace12,trace13,trace14,trace15,trace16,\
            trace17,trace18,trace19]
    layout = go.Layout(
        title='Calendar Return of Pair Funds',
        showlegend=False,
        yaxis=dict(
            title='Calendar Return',
            ticksuffix='%')
        )
    fig_4 = go.Figure(data=data, layout=layout)
    plot_url_4 = py.plot(fig_4, filename='Figure 4 Calendar Return of Pair Funds')    

    
    # Standard Deviation Table
    Standard_deviation_df = round(100*Standard_deviation_df,2)
    table_std = FF.create_table(Standard_deviation_df, index=True)
    py.plot(table_std, filename='Table 3 Standard Deviation of Portfolio Funds')      
    
    # Downside Deviation Table
    Downside_Deviation_df = round(100*Downside_Deviation_df,2)
    table_down_d = FF.create_table(Downside_Deviation_df, index=True)
    py.plot(table_down_d, filename='Table 4 Downside Deviation of Portfolio Funds')
    
    # Sharpe Ratio Table
    Sharpe_df = round(100*Sharpe_df,2)
    table_sharpe = FF.create_table(Sharpe_df, index=True)
    py.plot(table_sharpe, filename='Table 5 Sharpe Ratio of Portfolio Funds')    
    # Sharpe Ratio Plot
    trace1 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=100*rolling_sharpe_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=100*rolling_sharpe_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=100*rolling_sharpe_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=100*rolling_sharpe_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Sharpe Ratio of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Sharpe Ratio',
            ticksuffix='%')
        )
    fig_5 = go.Figure(data=data, layout=layout)
    plot_url_5 = py.plot(fig_5, filename='Figure 5 Rolling Sharpe Ratio of Portfolio Funds', sharing='public')    
    
    # Sortino Ratio Table
    Sortino_df = round(100*Sortino_df,2)
    table_sortino = FF.create_table(Sortino_df, index=True)
    py.plot(table_sortino, filename='Table 6 Sortino Ratio of Portfolio Funds')    
    # Sortino Ratio Plot
    trace1 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=100*rolling_sortino_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=100*rolling_sortino_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=100*rolling_sortino_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=100*rolling_sortino_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Sortino Ratio of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Sortino Ratio',
            ticksuffix='%')
        )
    fig_6 = go.Figure(data=data, layout=layout)
    plot_url_6 = py.plot(fig_6, filename='Figure 6 Rolling Sortino Ratio of Portfolio Funds', sharing='public')
    
    
    # Beta Table
    Beta_df = round(100*Beta_df,2)
    table_beta = FF.create_table(Beta_df, index=True)
    py.plot(table_beta, filename='Table 7 Beta with Russell 3000 of Portfolio Funds')    
    # Beta Plot
    trace1 = go.Scatter(
        x=rolling_beta_df.index,
        y=rolling_beta_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_beta_df.index,
        y=rolling_beta_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_beta_df.index,
        y=rolling_beta_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_beta_df.index,
        y=rolling_beta_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Beta of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Beta')
        )
    fig_7 = go.Figure(data=data, layout=layout)
    plot_url_7 = py.plot(fig_7, filename='Figure 7 Beta with Russell 3000 of Portfolio Funds', sharing='public')    
    # Alpha Plot
    trace1 = go.Scatter(
        x=rolling_alpha_df.index,
        y=rolling_alpha_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_alpha_df.index,
        y=rolling_alpha_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_alpha_df.index,
        y=rolling_alpha_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_alpha_df.index,
        y=rolling_alpha_df['D'],
        name='D'
        )
    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Alpha of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Alpha')
        )
    fig_8 = go.Figure(data=data, layout=layout)
    plot_url_8 = py.plot(fig_8, filename='Figure 8 Alpha of Portfolio Funds', sharing='public')   
    
    
    # Omega Ratio Table
    Omega_df = round(100*Omega_df,2)
    table_omega = FF.create_table(Omega_df, index=True)
    py.plot(table_omega, filename='Table 8 Omega Ratio of Portfolio Funds')    
    # Omega Ratio Plot
    trace1 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=100*rolling_omega_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=100*rolling_omega_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=100*rolling_omega_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=100*rolling_sortino_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Omega Ratio of Portfolio Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Omega Ratio',
            ticksuffix='%')
        )
    fig_9 = go.Figure(data=data, layout=layout)
    plot_url_9 = py.plot(fig_9, filename='Figure 9 Rolling Omega Ratio of Portfolio Funds', sharing='public')

    # Correlation Table
    Corr_df = round(100*Corr_df,2)
    table_corr = FF.create_table(Corr_df, index=True)
    py.plot(table_corr, filename='Table 9 Correlation of Portfolio Funds with Russell 3000')    
    # Correlation Plot
    trace1 = go.Scatter(
        x=rolling_corr_df.index,
        y=rolling_corr_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df.index,
        y=rolling_corr_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df.index,
        y=rolling_corr_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df.index,
        y=rolling_corr_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with Russell 3000',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_10 = go.Figure(data=data, layout=layout)
    plot_url_10 = py.plot(fig_10, filename='Figure 10 Rolling Correlation of Portfolio Funds with Russell 3000', sharing='public')


    # Correlation with Other Funds Mean Return
    trace1 = go.Scatter(
        x=rolling_corr_df_other.index,
        y=rolling_corr_df_other['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df_other.index,
        y=rolling_corr_df_other['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df_other.index,
        y=rolling_corr_df_other['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df_other.index,
        y=rolling_corr_df_other['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_11 = go.Figure(data=data, layout=layout)
    plot_url_11 = py.plot(fig_11, filename='Figure 11 Rolling Correlation of Pair Funds', sharing='public')    
    
    # Correlation with Q1 Funds Mean Return
    trace1 = go.Scatter(
        x=rolling_corr_df_Q1.index,
        y=rolling_corr_df_Q1['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df_Q1.index,
        y=rolling_corr_df_Q1['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df_Q1.index,
        y=rolling_corr_df_Q1['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df_Q1.index,
        y=rolling_corr_df_Q1['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with First Quartile Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_12 = go.Figure(data=data, layout=layout)
    plot_url_12 = py.plot(fig_12, filename='Figure 12 Rolling Correlation of First Quartile Pair Funds', sharing='public')    
    
    # Correlation with Q2 Funds Mean Return
    trace1 = go.Scatter(
        x=rolling_corr_df_Q2.index,
        y=rolling_corr_df_Q2['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df_Q2.index,
        y=rolling_corr_df_Q2['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df_Q2.index,
        y=rolling_corr_df_Q2['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df_Q2.index,
        y=rolling_corr_df_Q2['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with Second Quartile Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_13 = go.Figure(data=data, layout=layout)
    plot_url_13 = py.plot(fig_13, filename='Figure 13 Rolling Correlation of Second Quartile Pair Funds', sharing='public')
    
    
    # Correlation with Q3 Funds Mean Return
    trace1 = go.Scatter(
        x=rolling_corr_df_Q3.index,
        y=rolling_corr_df_Q3['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df_Q3.index,
        y=rolling_corr_df_Q3['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df_Q3.index,
        y=rolling_corr_df_Q3['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df_Q3.index,
        y=rolling_corr_df_Q3['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with Third Quartile Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_14 = go.Figure(data=data, layout=layout)
    plot_url_14 = py.plot(fig_14, filename='Figure 14 Rolling Correlation of Third Quartile Pair Funds', sharing='public')
    
    # Correlation with Q4 Funds Mean Return
    trace1 = go.Scatter(
        x=rolling_corr_df_Q4.index,
        y=rolling_corr_df_Q4['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_corr_df_Q4.index,
        y=rolling_corr_df_Q4['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_corr_df_Q4.index,
        y=rolling_corr_df_Q4['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_corr_df_Q4.index,
        y=rolling_corr_df_Q4['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Correlation of Portfolio Funds with Fourth Quartile Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_15 = go.Figure(data=data, layout=layout)
    plot_url_15 = py.plot(fig_15, filename='Figure 15 Rolling Correlation of Fourth Quartile Pair Funds', sharing='public')

