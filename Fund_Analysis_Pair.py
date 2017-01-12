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
    
   
    ### Output all static dataframe into excel file
    dfs = [Annulized_Return_df,Calendar_Return_df,Sharpe_df,Sortino_df,\
           Standard_deviation_df,Downside_Deviation_df,Beta_df,Beta_df_p,\
           Beta_df_np,Omega_df,Corr_df,Corr_df_p,Corr_df_np,Summary_table_df]
    put.multiple_dfs(dfs, 'Financial Ratio', 'Financial Ratio Result.xlsx', 1)
    
    ### Output all rolling data to seperated sheet in excel file
    rolling_df_list = [rolling_beta_df,rolling_annual_return_df,cum_return_df,\
                       rolling_sortino_ratio_df,rolling_omega_ratio_df,rolling_sharpe_ratio_df,\
                       rolling_alpha_df,rolling_corr_df]
    put.multiple_sheets(rolling_df_list, 'Rolling Result.xlsx')
    
    
    
    ### Plotly Table ###
    Annulized_Return_df = round(Annulized_Return_df,3)
    table_Annulized_Return = FF.create_table(Annulized_Return_df, index=True)
    py.plot(table_Annulized_Return, filename='Annulized_Return_df')
    
    
    
    
    
    
    
    
    
    
    

    ### Plotly ###
    trace0=go.Box(
        y = Calendar_Return_df.ix[:,2007],
        boxpoints='all',
        jitter=0.5,
        pointpos=0
                  )

    trace1=go.Box(
        y = Calendar_Return_df.ix[:,2008],
        boxpoints='all',
        jitter=0.9,
        pointpos=1.8
              )
    
    trace2=go.Box(
        y = Calendar_Return_df.ix[:,2009],
        boxpoints='all',
        jitter=0.9,
        pointpos=1.5,
        visible=True
                  )
    
    trace3=go.Box(
        y = Calendar_Return_df.ix[:,2010],
        boxpoints='all',
        jitter=0.9,
        pointpos=1.5,
        visible=True,
        hoverinfo=True
                  )
    
    trace4=go.Box(
        y = Calendar_Return_df.ix[:,2011],
        boxpoints='all',
        jitter=0.9,
        pointpos=1.5,
        visible=True,
        hoverinfo=True,
        name='Test Name'
                  )
    
    trace5=go.Box(
        y = Calendar_Return_df.ix[:,2012]
                  )
    
    trace6=go.Box(
        y = Calendar_Return_df.ix[:,2013]
                  )
    
    trace7=go.Box(
        y = Calendar_Return_df.ix[:,2014]
                  )

    trace8=go.Box(
        y = Calendar_Return_df.ix[:,2015]
                  )

    
    trace9=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['A'].values,
        mode = 'markers',
        name = 'A'
        )

    trace10=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['B'].values,
        mode = 'markers',
        name = 'B'
        )
    
    trace11=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['C'].values,
        mode = 'markers',
        name = 'C'
        )
    
    trace12=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['D'].values,
        mode = 'markers',
        name = 'D'
        )
    
    trace13=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['E'].values,
        mode = 'markers',
        name = 'E'
        )
    
    trace14=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['F'].values,
        mode = 'markers',
        name = 'F'
        )
    
    trace15=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['G'].values,
        mode = 'markers',
        name = 'G'
        )
    trace9=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['H'].values,
        mode = 'markers',
        name = 'H'
        )

    trace10=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['I'].values,
        mode = 'markers',
        name = 'I'
        )
    
    trace11=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['J'].values,
        mode = 'markers',
        name = 'J'
        )
    
    trace12=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['K'].values,
        mode = 'markers',
        name = 'K'
        )
    
    trace13=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['L'].values,
        mode = 'markers',
        name = 'L'
        )
    
    trace14=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['M'].values,
        mode = 'markers',
        name = 'M'
        )
    
    trace15=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['N'].values,
        mode = 'markers',
        name = 'N'
        )
        
    trace9=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['O'].values,
        mode = 'markers',
        name = 'O'
        )

    trace10=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['P'].values,
        mode = 'markers',
        name = 'P'
        )
    
    trace11=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['Q'].values,
        mode = 'markers',
        name = 'Q'
        )
    
    trace12=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['R'].values,
        mode = 'markers',
        name = 'R'
        )
    
    trace13=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['S'].values,
        mode = 'markers',
        name = 'S'
        )
    
    trace14=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['T'].values,
        mode = 'markers',
        name = 'T'
        )
    
    trace15=go.Scatter(
        x = Calendar_Return_df.T.index,
        y = Calendar_Return_df.ix['U'].values,
        mode = 'markers',
        name = 'U'
        )
    
    data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8,trace9]
    py.plot(data)
    
    
    
    
    
    
    trace1 = {
      "y": Calendar_Return_df.ix[:,2007].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2007", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "10e105"
    }
    trace2 = {
      "y": Calendar_Return_df.ix[:,2008].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2008", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "14599d"
    }
    trace3 = {
      "y": Calendar_Return_df.ix[:,2009].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2009", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "b43551"
    }
    trace4 = {
      "y": Calendar_Return_df.ix[:,2010].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2010", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "af4eb5"
    }
    trace5 = {
      "y": Calendar_Return_df.ix[:,2011].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2011", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "6606e4"
    }
    trace6 = {
      "y": Calendar_Return_df.ix[:,2012].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2012", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "649f3e"
    }
    trace7 = {
      "y": Calendar_Return_df.ix[:,2013].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2013", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "c9e8c9"
    }
    trace8 = {
      "y": Calendar_Return_df.ix[:,2014].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2014", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "830707"
    }
    trace9 = {
      "y": Calendar_Return_df.ix[:,2015].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2015", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "383b5f"
    }
    trace10 = {
      "y": Calendar_Return_df.ix[:,2016].values, 
      "boxpoints": False, 
      "fillcolor": "rgb(221, 126, 107)", 
      "line": {"color": "rgb(204, 65, 37)"}, 
      "marker": {"line": {"color": "rgb(204, 65, 37)"}}, 
      "name": "2016", 
      "opacity": 0.5, 
      "showlegend": False, 
      "type": "box", 
      "uid": "524bf3"
    }

    trace11 = {
      "x": Calendar_Return_df.T.index, 
      "y": Calendar_Return_df.T.values, 
      "line": {"color": "rgb(166, 28, 0)"}, 
      "marker": {"line": {"color": "rgb(166, 28, 0)"}}, 
      "name": "Highs (2014 YTD)", 
      "type": "scatter", 
      "uid": "0077fc"
    }

    data = Data([trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11])
    layout = {
      "annotations": [
        {
          "x": 0.555051813472, 
          "y": 0.0858364762931, 
          "align": "center", 
          "arrowcolor": "", 
          "arrowhead": 1, 
          "arrowsize": 1, 
          "arrowwidth": 0, 
          "ax": 52, 
          "ay": 25.828125, 
          "bgcolor": "rgba(0,0,0,0)", 
          "bordercolor": "", 
          "borderpad": 1, 
          "borderwidth": 1, 
          "font": {
            "color": "", 
            "family": "", 
            "size": 0
          }, 
          "opacity": 1, 
          "showarrow": False, 
          "text": "Box & whisker plots refer to average highs/lows from 1945-2013.", 
          "textangle": 0, 
          "xanchor": "center", 
          "xref": "paper", 
          "yanchor": "middle", 
          "yref": "paper"
        }, 
        {
          "x": 0.545984455959, 
          "y": 0.0427330280172, 
          "align": "center", 
          "arrowcolor": "", 
          "arrowhead": 1, 
          "arrowsize": 1, 
          "arrowwidth": 0, 
          "ax": -10, 
          "ay": -28.171875, 
          "bgcolor": "rgba(0,0,0,0)", 
          "bordercolor": "", 
          "borderpad": 1, 
          "borderwidth": 1, 
          "font": {
            "color": "", 
            "family": "", 
            "size": 0
          }, 
          "opacity": 1, 
          "showarrow": False, 
          "text": "YTD data current through 14 August 2014.", 
          "textangle": 0, 
          "xanchor": "center", 
          "xref": "paper", 
          "yanchor": "middle", 
          "yref": "paper"
        }, 
        {
          "x": 0.0874587458746, 
          "y": -0.123866421569, 
          "align": "center", 
          "arrowcolor": "", 
          "arrowhead": 1, 
          "arrowsize": 1, 
          "arrowwidth": 0, 
          "ax": -10, 
          "ay": -28.171875, 
          "bgcolor": "rgba(0,0,0,0)", 
          "bordercolor": "", 
          "borderpad": 1, 
          "borderwidth": 1, 
          "font": {
            "color": "", 
            "family": "", 
            "size": 0
          }, 
          "opacity": 1, 
          "showarrow": False, 
          "text": "Graph by Nate Johnson @nsj / Data source: SERCC", 
          "textangle": 0, 
          "xanchor": "center", 
          "xref": "paper", 
          "yanchor": "middle", 
          "yref": "paper"
        }
      ], 
      "autosize": True, 
      "bargap": 0.2, 
      "bargroupgap": 0, 
      "barmode": "group", 
      "boxgap": 0.3, 
      "boxgroupgap": 0.3, 
      "boxmode": "overlay", 
      "dragmode": "pan", 
      "font": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 12
      }, 
      "height": 690, 
      "hidesources": False, 
      "hovermode": "x", 
      "legend": {
        "x": 0.458549222798, 
        "y": 0.209051724138, 
        "bgcolor": "#fff", 
        "bordercolor": "#444", 
        "borderwidth": 0, 
        "font": {
          "color": "", 
          "family": "", 
          "size": 0
        }, 
        "traceorder": "normal", 
        "xanchor": "left", 
        "yanchor": "top"
      }, 
      "margin": {
        "r": 80, 
        "t": 100, 
        "autoexpand": True, 
        "b": 80, 
        "l": 80, 
        "pad": 0
      }, 
      "paper_bgcolor": "#fff", 
      "plot_bgcolor": "#fff", 
      "separators": ".,", 
      "showlegend": True, 
      "smith": False, 
      "title": "Monthly Average Temperatures at RDU", 
      "titlefont": {
        "color": "", 
        "family": "", 
        "size": 0
      }, 
      "width": 1142, 
      "xaxis": {
        "anchor": "y", 
        "autorange": True, 
        "autotick": True, 
        "domain": [0, 1], 
        "dtick": 1, 
        "exponentformat": "B", 
        "gridcolor": "#eee", 
        "gridwidth": 1, 
        "linecolor": "#444", 
        "linewidth": 1, 
        "mirror": False, 
        "nticks": 0, 
        "overlaying": False, 
        "position": 0, 
        "range": [-0.605263157895, 11.5], 
        "rangemode": "normal", 
        "showexponent": "all", 
        "showgrid": False, 
        "showline": False, 
        "showticklabels": True, 
        "tick0": 0, 
        "tickangle": "auto", 
        "tickcolor": "#444", 
        "tickfont": {
          "color": "", 
          "family": "", 
          "size": 0
        }, 
        "ticklen": 5, 
        "ticks": "", 
        "tickwidth": 1, 
        "title": "Months", 
        "titlefont": {
          "color": "", 
          "family": "", 
          "size": 0
        }, 
        "type": "category", 
        "zeroline": False, 
        "zerolinecolor": "#444", 
        "zerolinewidth": 1
      }, 
      "yaxis": {
        "anchor": "x", 
        "autorange": True, 
        "autotick": True, 
        "domain": [0, 1], 
        "dtick": 10, 
        "exponentformat": "B", 
        "gridcolor": "#eee", 
        "gridwidth": 1, 
        "linecolor": "#444", 
        "linewidth": 1, 
        "mirror": False, 
        "nticks": 0, 
        "overlaying": False, 
        "position": 0, 
        "range": [11.2388888889, 100.461111111], 
        "rangemode": "normal", 
        "showexponent": "all", 
        "showgrid": True, 
        "showline": False, 
        "showticklabels": True, 
        "tick0": 0, 
        "tickangle": "auto", 
        "tickcolor": "#444", 
        "tickfont": {
          "color": "", 
          "family": "", 
          "size": 0
        }, 
        "ticklen": 5, 
        "ticks": "", 
        "tickwidth": 1, 
        "title": "Monthly Average Temperatures", 
        "titlefont": {
          "color": "", 
          "family": "", 
          "size": 0
        }, 
        "type": "linear", 
        "zeroline": True, 
        "zerolinecolor": "#444", 
        "zerolinewidth": 1
      }
    }
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)