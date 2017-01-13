# -*- coding: utf-8 -*-
"""
This is the main file to get all major financial ratio and rolling ratio and other important graph
"""
import os
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as put
import mod_plot as p
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
    df_data = put.concat_data('test_data.xlsx')
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
    index_name_3 = df_data.columns[1:] # No Date
    columns_name = df_data.columns[1:] # No Date
    # Initial value for rolling data calculation
    window_length = 36 # rolling window is 36 months
    min_periods = 36 # We only take complete 36 month period into consideration

    ### Calculate Annulized Return
    Annulized_Return_df = r.annulized_return_table(df_data, index_name, target_year)
    ### Calculate Calendar Return
    Calendar_Return_df = r.calendar_return_table(df_data, index_name_2)
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
    ### Rolling sortino ratio
    rolling_sortino_ratio_df = m.rolling_sortino_ratio(df_data, columns_name, window_length, min_periods, MAR, threshold)
    ### Rolling omega ratio
    rolling_omega_ratio_df = m.rolling_omega_ratio(df_data, columns_name, window_length, min_periods, MAR)
    ### Rolling sharp ratio
    rolling_sharpe_ratio_df = m.rolling_sharpe_ratio(df_data, columns_name, window_length, min_periods, benchmark)
    ### Rolling alpha
    rolling_alpha_df = m.rolling_alpha(df_data, columns_name, window_length, min_periods)
    ### Rolling correlation
    rolling_corr_df = m.rolling_corr(df_data, columns_name, market_index, window_length, min_periods)
    ### Draw Down
    dd_df = 100* m.draw_down(df_data, columns_name)
    
    
    
    
    ### Plotly Table ###
    # Annual Return Table
    Annulized_Return_df = round(Annulized_Return_df,3)
    table_Annulized_Return = FF.create_table(Annulized_Return_df, index=True)
    py.plot(table_Annulized_Return, filename='Table 1 Annulized Return')
    # Annual Return Plot
    trace1 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=rolling_annual_return_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=rolling_annual_return_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=rolling_annual_return_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_annual_return_df.index,
        y=rolling_annual_return_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Annual Return of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Annualized Return')
        )
    fig_1 = go.Figure(data=data, layout=layout)
    plot_url_1 = py.plot(fig_1, filename='Figure 1 Rolling Annual Return of Pair Funds', sharing='public')
    

    # Calendar Return Table
    Calendar_Return_df = round(Calendar_Return_df,3)
    table_Calendar_Return = FF.create_table(Calendar_Return_df, index=True)
    py.plot(table_Calendar_Return, filename='Table 2 Calendar Return of Pair Funds')    
    
    # Standard Deviation Table
    Standard_deviation_df = round(Standard_deviation_df,3)
    table_std = FF.create_table(Standard_deviation_df, index=True)
    py.plot(table_std, filename='Table 3 Standard Deviation of Pair Funds')      
    
    # Downside Deviation Table
    Downside_Deviation_df = round(Downside_Deviation_df,3)
    table_down_d = FF.create_table(Downside_Deviation_df, index=True)
    py.plot(table_down_d, filename='Table 4 Downside Deviation of Pair Funds')
    
    # Sharpe Ratio Table
    Sharpe_df = round(Sharpe_df,3)
    table_sharpe = FF.create_table(Sharpe_df, index=True)
    py.plot(table_sharpe, filename='Table 5 Sharpe Ratio of Pair Funds')    
    # Sharpe Ratio Plot
    trace1 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=rolling_sharpe_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=rolling_sharpe_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=rolling_sharpe_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sharpe_ratio_df.index,
        y=rolling_sharpe_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Sharpe Ratio of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Sharpe Ratio')
        )
    fig_2 = go.Figure(data=data, layout=layout)
    plot_url_2 = py.plot(fig_2, filename='Figure 2 Rolling Sharpe Ratio of Pair Funds', sharing='public')    
    
    # Sortino Ratio Table
    Sortino_df = round(Sortino_df,3)
    table_sortino = FF.create_table(Sortino_df, index=True)
    py.plot(table_sortino, filename='Table 5 Sortino Ratio of Pair Funds')    
    # Sortino Ratio Plot
    trace1 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=rolling_sortino_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=rolling_sortino_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=rolling_sortino_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=rolling_sortino_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Sortino Ratio of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Sortino Ratio')
        )
    fig_3 = go.Figure(data=data, layout=layout)
    plot_url_3 = py.plot(fig_3, filename='Figure 3 Rolling Sortino Ratio of Pair Funds', sharing='public')
    
    
    # Beta Table
    Beta_df = round(Beta_df,3)
    table_beta = FF.create_table(Beta_df, index=True)
    py.plot(table_beta, filename='Table 6 Beta with Russell 3000 of Pair Funds')    
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
        title='Rolling Beta of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Beta')
        )
    fig_4 = go.Figure(data=data, layout=layout)
    plot_url_4 = py.plot(fig_4, filename='Figure 4 Beta with Russell 3000 of Pair Funds', sharing='public')    
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
        title='Rolling Alpha of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Alpha')
        )
    fig_5 = go.Figure(data=data, layout=layout)
    plot_url_5 = py.plot(fig_5, filename='Figure 5 Alpha of Pair Funds', sharing='public')   
    
    
    # Omega Ratio Table
    Omega_df = round(Omega_df,3)
    table_omega = FF.create_table(Omega_df, index=True)
    py.plot(table_omega, filename='Table 7 Omega Ratio of Pair Funds')    
    # Omega Ratio Plot
    trace1 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=rolling_omega_ratio_df['A'],
        name='A'
        )
    trace2 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=rolling_omega_ratio_df['B'],
        name='B'
        )
    trace3 = go.Scatter(
        x=rolling_omega_ratio_df.index,
        y=rolling_omega_ratio_df['C'],
        name='C'
        )
    trace4 = go.Scatter(
        x=rolling_sortino_ratio_df.index,
        y=rolling_sortino_ratio_df['D'],
        name='D'
        )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Rolling Omega Ratio of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Omega Ratio')
        )
    fig_6 = go.Figure(data=data, layout=layout)
    plot_url_6 = py.plot(fig_6, filename='Figure 6 Rolling Omega Ratio of Pair Funds', sharing='public')

    # Correlation Table
    Corr_df = round(Corr_df,3)
    table_corr = FF.create_table(Corr_df, index=True)
    py.plot(table_corr, filename='Table 8 Correlation of Pair Funds')    
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
        title='Rolling Correlation of Pair Funds',
        showlegend=True,
        yaxis=dict(
            title='Rolling Correlation')
        )
    fig_7 = go.Figure(data=data, layout=layout)
    plot_url_7 = py.plot(fig_7, filename='Figure 7 Rolling Correlation of Pair Funds', sharing='public')
    
    # Calendar Return Plot #
    trace0=go.Box(
        y = Calendar_Return_df.ix[:,2007].values,
        name = '2007',
        showlegend=False
                  )

    trace1=go.Box(
        y = Calendar_Return_df.ix[:,2008],
        name = '2008',
        showlegend=False
              )
    
    trace2=go.Box(
        y = Calendar_Return_df.ix[:,2009],
        name = '2009',
        showlegend=False
                  )
    
    trace3=go.Box(
        y = Calendar_Return_df.ix[:,2010],
        name = '2010',
        showlegend=False
                  )
    
    trace4=go.Box(
        y = Calendar_Return_df.ix[:,2011],
        name = '2011',
        showlegend=False
                  )
    
    trace5=go.Box(
        y = Calendar_Return_df.ix[:,2012],
        name = '2012',
        showlegend=False
                  )
    
    trace6=go.Box(
        y = Calendar_Return_df.ix[:,2013],
        name = '2013',
        showlegend=False
                  )
    
    trace7=go.Box(
        y = Calendar_Return_df.ix[:,2014],
        name = '2014',
        showlegend=False
                  )

    trace8=go.Box(
        y = Calendar_Return_df.ix[:,2015],
        name = '2015',
        showlegend=False
                  )
    trace8=go.Box(
        y = Calendar_Return_df.ix[:,2016],
        name = '2016',
        showlegend=False
                  )

    trace9=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['A'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'A'
        )

    trace10=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['B'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'B'
        )
    
    trace11=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['C'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'C'
        )
    
    trace12=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['D'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'D'
        )
    
    trace13=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['E'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'E'
        )
    
    trace14=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['F'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'F'
        )
    
    trace15=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['G'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'G'
        )
    trace16=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['H'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'H'
        )

    trace17=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['I'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'I'
        )
    
    trace18=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['J'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'J'
        )
    
    trace19=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['K'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'K'
        )
    
    trace20=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['L'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'L'
        )
    
    trace21=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['M'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'M'
        )
    
    trace22=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['N'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'N'
        )
        
    trace23=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['O'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'O'
        )

    trace24=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['P'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'P'
        )
    
    trace25=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['Q'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'Q'
        )
    
    trace26=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['R'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'R'
        )
    
    trace27=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['S'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'S'
        )
    
    trace28=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['T'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'T'
        )
    
    trace29=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['U'].values,
        mode = 'markers',
        marker = dict(size=15, opacity=0.3),
        name = 'U'
        )
    
    data = [trace0,trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,\
            trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16,\
            trace17,trace18,trace19,trace20,trace21,trace22,trace23,trace24,\
            trace25,trace26,trace27,trace28,trace29]
    py.plot(data)
    
