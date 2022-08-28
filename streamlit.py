import streamlit as st

from utils import (
    load_data, subdata, trend_plot, 
    view_county, bar_plot, year_filter,
    filter_df_by_year
)

st.title('1.88 Million US Wildfires')


data_load_state = st.text('Loading data...')
df = load_data(nrows='all')

cause_counts, year_counts, month_year_counts, county_counts = subdata(df)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df.head(20))


trend_fig = trend_plot(month_year_counts)
least_county_fig  = view_county(county_counts, count=50, tail=True)

yearly_summary = bar_plot(year_counts,
            x='FIRE_YEAR',
            y='count',
            labels={'count':'Total Count', 'FIRE_YEAR': 'Year'}, 
            title="Yearly summary of wildfire")



with st.container():
    st.header("County Analysis")
    st.write("""
    The visualization reports below show the wildfire distribution across each county and 
    can be filtered by years.
    """)

    years = year_filter()
    # st.markdown("#### Top Fire-prone County")

    if len(years) == 0:
        top_county_fig = bar_plot(county_counts.head(30),
            x='FIPS_NAME',
            y='count',
            color='count',
            labels={"count": "Number of wildfires", "FIPS_NAME": "County Name"},
            title="Top Fire-prone Counties")
        st.plotly_chart(top_county_fig, use_container_width=True)
        
    else:
        county_data_filterd_by_year =  filter_df_by_year(df, years, 'county')    
        county_year_fig = bar_plot(county_data_filterd_by_year.head(30),
            x='FIPS_NAME',
            y='count',
            color='FIRE_YEAR',
            labels={"count": "Number of wildfires", "FIPS_NAME": "County Name"},
            title="Top Fire-prone Counties")        
        st.plotly_chart(county_year_fig, use_container_width=True)

    st.plotly_chart(least_county_fig, use_container_width=True)


with st.container():
    st.header("Fire Distribution by cause event")
    # st.write("""
    # The visualization reports below show the wildfire distribution across each county and can be filtered by years 
    # """)
    
    years = year_filter(" ")
    st.markdown("### Top Fire-prone Counrty")
    if len(years) == 0:
        fire_cause_fig = bar_plot(cause_counts,
            x='STAT_CAUSE_DESCR',
            y='count',
            color='STAT_CAUSE_DESCR',
            labels={'count':'Total Count', 'STAT_CAUSE_DESCR': 'Causes'}, 
            title="Distribution of the fire events")
        st.plotly_chart(fire_cause_fig, use_container_width=False)
        
    else:
        cause_data_filterd_by_year =  filter_df_by_year(df, years, 'cause')    
        county_year_fig = bar_plot(cause_data_filterd_by_year,
            x='STAT_CAUSE_DESCR',
            y='count',
            color='FIRE_YEAR',
            labels={'count':'Total Count', 'STAT_CAUSE_DESCR': 'Causes'}, 
            title="Distribution of the fire events")       
        st.plotly_chart(county_year_fig, use_container_width=True)
    




# if len(years) == 0:
#     st.plotly_chart(top_county_fig, use_container_width=True)
# else:
#     county_year_fig =  filter_df_by_year(df, years)          
#     st.plotly_chart(county_year_fig, use_container_width=True)

st.plotly_chart(trend_fig, use_container_width=True)
st.plotly_chart(yearly_summary, use_container_width=False)




# a = df.rename(columns={'LATITUDE':"latitude", 'LONGITUDE':"longitude"})[["latitude", "longitude"]]
# st.map(a)

st.markdown('''
# header
Streamlit is **_really_ cool**.''')