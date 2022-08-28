import streamlit as st
import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine

import plotly.express as px
import plotly.graph_objects as go



@st.cache
def load_data(path: str='FPA_FOD_20170508.sqlite', nrows: int=10000) -> pd.DataFrame:
    connect = f'sqlite:///{path}'
    engine = create_engine(connect)

    if nrows != 'all':
        data = pd.read_sql_query(f"""
            SELECT
                *, 
                datetime(DISCOVERY_DATE) as DIS_DATETIME,
                datetime(CONT_DATE) as CON_DATETIME
            FROM 
                Fires 
            LIMIT {nrows};
            """ , engine)
    else:
        data = pd.read_sql_query(f"""
            SELECT
                *, 
                datetime(DISCOVERY_DATE) as DIS_DATETIME,
                datetime(CONT_DATE) as CON_DATETIME
            FROM 
                Fires 
            """ , engine)
    data['DISC_YM'] = data['DIS_DATETIME'].str.extract(r'(\d{4}-\d{2})')

    return data


@st.cache
def subdata(df: pd.DataFrame) -> pd.DataFrame:
    cause_counts = df["STAT_CAUSE_DESCR"].value_counts()\
                        .to_frame()\
                        .reset_index()\
                        .rename(columns={'STAT_CAUSE_DESCR':"count", "index":'STAT_CAUSE_DESCR'})\
                        .sort_values(by='STAT_CAUSE_DESCR',)

    month_year_counts = df[["DISC_YM", "FIRE_YEAR", "OBJECTID"]]\
                        .groupby(["DISC_YM", "FIRE_YEAR"])\
                        .count()\
                        .rename(columns={'OBJECTID':"count"})\
                        .reset_index()
    
    year_counts = df[["FIRE_YEAR", "OBJECTID"]]\
                .groupby(["FIRE_YEAR"])\
                .count()\
                .rename(columns={'OBJECTID':"count"})\
                .reset_index()
                    
    county_counts = df['FIPS_NAME'].value_counts()\
                        .to_frame()\
                        .reset_index()\
                        .rename(columns={'FIPS_NAME':"count", "index":'FIPS_NAME'})\
                        .sort_values(by='count', ascending=False)

    return cause_counts, year_counts, month_year_counts, county_counts


def trend_plot(month_year_counts: pd.DataFrame):
    trend_fig = go.Figure()

    trend_fig.add_trace(
                    go.Scatter(
                        x=month_year_counts['DISC_YM'], 
                        y=month_year_counts['count'], 
                        line_color='#83C9FF',
                        )
                    )

    trend_fig.update_layout(
                    {
                        "title": "Trend of Wildfire over time",
                        "yaxis": {"title":"Number of Wildfires"},
                        "xaxis": {"title":"Date(Month-Year)"}
                    },
                    height=600,
                    width=1000,
                    )

    trend_fig.update_traces(texttemplate = "%{x} | %{y}")
    trend_fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))

    return trend_fig


def view_county(county_counts: pd.DataFrame, tail: bool=False, count: int=50):

    if tail:
        title = "Least Fire-prone Counties"
        slice_county = county_counts.tail(count)
    else:
        title = "Top Fire-prone Counties"
        slice_county = county_counts.head(count)
    fig = go.Figure()
    fig.add_trace(
                    go.Bar(
                            x=slice_county['FIPS_NAME'], 
                            y=slice_county['count'], 
                            texttemplate = "%{y}",
                            marker=dict(color = "#1db820", colorscale='viridis')
                        )
                    )

    fig.update_layout({
                        "title": title,
                        "yaxis": {"title":"Number of Wildfires"},
                        "xaxis": {"title":"County Names"}
                    },
                    width=1000,
                    )
    if count > 30:
        # add slider
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
    return fig


def bar_plot(df: pd.DataFrame,
            x: str,
            y: str,
            labels: dict,
            title=None,
            color=None):

    fig = px.bar(df, x=x, y=y,
                color=color,
                labels=labels, 
                text_auto='.2s',
                height=500,
                width=800,
                title=title)
    return fig


def year_filter(check=""):
    col0, col1, col2, col3, col4, col5 = st.columns(6)
    years = []
    with col0:
        st.markdown("#### `Filter`") 
    with col1:
        if st.checkbox('2015' + check):
            years.append(2015)
    with col2:
        if  st.checkbox('2014' + check):
            years.append(2014)
    with col3:
        if  st.checkbox('2013' + check):
            years.append(2013)
    with col4:
        if  st.checkbox('2012' + check):
            years.append(2012)
    with col5:
        if st.checkbox('2011' + check):
            years.append(2011)
    return years


def filter_df_by_year(df, years, data):
    df_filter = df[df["FIRE_YEAR"].isin(years) ]
    df_filter["FIRE_YEAR"] = df_filter["FIRE_YEAR"].astype(str)

    if data == 'county':
        filter_data = df_filter[["FIPS_NAME", "FIRE_YEAR", "OBJECTID"]]\
                            .groupby(["FIPS_NAME", "FIRE_YEAR"])\
                            .count()\
                            .rename(columns={'OBJECTID':"count"})\
                            .reset_index()\
                            .sort_values(['count', 'FIRE_YEAR'] , ascending=False)
    elif data == "cause":
        filter_data = df_filter[["STAT_CAUSE_DESCR", "FIRE_YEAR", "OBJECTID"]]\
                        .groupby(["STAT_CAUSE_DESCR", "FIRE_YEAR"])\
                        .count()\
                        .rename(columns={'OBJECTID':"count"})\
                        .reset_index()

    return filter_data