import streamlit as st
import plotly.express as px
import datetime

from utils import (
    load_data, subdata, trend_plot, 
    view_county, bar_plot, year_filter,
    filter_df_by_year, slider, cause_filter,
    get_class
)
from predict import predict_cause

st.title('1.88 Million US Wildfires')


data_load_state = st.text('Loading data...')
df = load_data()

cause_counts, year_counts, month_year_counts, county_counts, month_year_couse_counts = subdata(df)

if st.checkbox('Show raw data'):
    st.subheader('Raw data') 
    st.write(df.head(20))

with st.container():
    st.subheader("Predict Cause")
    st.write('The model accuracy is quite low')

    input_size = st.number_input('FIZE SIZE', min_value=0.0, value=10.0)
    size_class = get_class(input_size)

    input_date = st.date_input( "DATE", datetime.date(2015, 7, 6))

    st.write('LOCATION')
    col0, col1 = st.columns(2)
    with col0:
        latitude = st.number_input('latitude', min_value=-90.0,  max_value=90.0, value=10.0)
    with col1:
        longitude = st.number_input('longitude', min_value=-180.0,  max_value=180.0, value=-30.0)

    input_list = [input_size, size_class, latitude, longitude, input_date]
    print(input_list)

    col0, col1 = st.columns(2)
    with col0:
        if st.button('Predict Result'):
            result = predict_cause(input_list)
            with col1:
                st.write(f'### Predicted Cause: `{result}`')


with st.container():
    st.subheader("County Analysis")
    st.write("""
    The visualization reports below show the wildfire distribution across each county and 
    can be filtered by years.
    """)

    st.markdown("##### Top Fire-prone County")
    st.write("""
    The record shows that the top 5 fire incidents happened in `Washington`, `Lincoln`, `Jackson`, 
    `Marion` and `Cherokee`.
    """)

    years = year_filter()
    x = slider(text='x', min_value=10, max_value=100, default_value=30, info="Filter top record using slider") 
    if len(years) == 0:
        top_county_fig = bar_plot(county_counts.head(x),
            x='FIPS_NAME',
            y='count',
            color='count',
            labels={"count": "Number of wildfires", "FIPS_NAME": "County Name"},
            width=1000,
            title=""
            )
        st.plotly_chart(top_county_fig, use_container_width=False)
        
    else:
        county_data_filterd_by_year =  filter_df_by_year(df, years, 'county')    
        county_year_fig = bar_plot(county_data_filterd_by_year.head(30),
            x='FIPS_NAME',
            y='count',
            color='FIRE_YEAR',
            labels={"count": "Number of wildfires", "FIPS_NAME": "County Name"},
            title="Top Fire-prone Counties",
            width=1000)        
        st.plotly_chart(county_year_fig, use_container_width=False)

    least_county_fig  = view_county(county_counts, width=1000, count=50, tail=True)
    st.plotly_chart(least_county_fig, use_container_width=False)


with st.container():
    st.subheader("Fire Distribution by cause event")
    st.write("""
    In the chart below, the cause event was observed and it is seen that the major KNOWN cause of 
    wildfire is `Debris Burning`, `Arson` and `Lightening`. 
    """)
    
    years = year_filter(" ")
    if len(years) == 0:
        fire_cause_fig = bar_plot(cause_counts,
            x='STAT_CAUSE_DESCR',
            y='count',
            color='STAT_CAUSE_DESCR',
            labels={'count':'Total Count', 'STAT_CAUSE_DESCR': 'Causes'}, 
            title="Distribution of the fire events",
            width=1000)
        st.plotly_chart(fire_cause_fig, use_container_width=False)
        
    else:
        cause_data_filterd_by_year =  filter_df_by_year(df, years, 'cause')    
        county_year_fig = bar_plot(cause_data_filterd_by_year,
            x='STAT_CAUSE_DESCR',
            y='count',
            color='FIRE_YEAR',
            labels={'count':'Total Count', 'STAT_CAUSE_DESCR': 'Causes'}, 
            title="Distribution of the fire events",
            width=1000)       
        st.plotly_chart(county_year_fig, use_container_width=False)


with st.container():
    st.subheader("Time Analysis of Wildfire")
    st.write("""
    The time analysis in the chart below shows how the fire incident happen over the years. Each point of 
    the chart represent months for a particular year. The flltering button is used to filter and compare 
    wildfire trend (awesome discovery when filtered by `Arson` and `Fireworks`) 
    """)

    filters_cause = cause_filter()

    if len(filters_cause) == 0:
        trend_fig = trend_plot(month_year_counts, 1000)
        st.plotly_chart(trend_fig, use_container_width=False)
    else:
        filter_cause_df = month_year_couse_counts[month_year_couse_counts["STAT_CAUSE_DESCR"].isin(filters_cause)]
        filter_cause_fig = px.line(filter_cause_df, x="DISC_YM", y="count", 
                            color="STAT_CAUSE_DESCR", 
                            width=1000,
                            labels={'count':'Total Count', 'STAT_CAUSE_DESCR': 'Causes'}, )
        st.plotly_chart(filter_cause_fig)

    yearly_summary = bar_plot(year_counts,
                x='FIRE_YEAR',
                y='count',
                labels={'count':'Total Count', 'FIRE_YEAR': 'Year'}, 
                width=1000,
                title="Yearly summary of wildfire")
    st.plotly_chart(yearly_summary, use_container_width=False)


with st.container():
    st.subheader("Map")
    if st.checkbox('Show Map'):

        x = slider(text='y', 
            min_value=100, 
            max_value=500000, 
            default_value=10000, 
            info=("""To make the map interactive and responsive, the map default loaded 
            record was set to 1000. Use the slider to load more data, 
            however, note that as the record increase, the map becomes slow and irresponsive""")
        )

        st.map(df.head(x).rename(columns={'LATITUDE':"latitude", 'LONGITUDE':"longitude"})[["latitude", "longitude"]])
