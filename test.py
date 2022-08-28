from utils import load_data

df = load_data(nrow=100)

expected_columns = ['OBJECTID', 'FOD_ID', 'FPA_ID', 'SOURCE_SYSTEM_TYPE', 
    'SOURCE_SYSTEM', 'NWCG_REPORTING_AGENCY', 'NWCG_REPORTING_UNIT_ID', 
    'NWCG_REPORTING_UNIT_NAME', 'SOURCE_REPORTING_UNIT', 
    'SOURCE_REPORTING_UNIT_NAME', 'LOCAL_FIRE_REPORT_ID', 
    'LOCAL_INCIDENT_ID', 'FIRE_CODE', 
    'FIRE_NAME', 'ICS_209_INCIDENT_NUMBER',
    'ICS_209_NAME', 'MTBS_ID', 'MTBS_FIRE_NAME', 
    'COMPLEX_NAME', 'FIRE_YEAR', 
    'DISCOVERY_DATE', 'DISCOVERY_DOY', 
    'DISCOVERY_TIME', 'STAT_CAUSE_CODE', 
    'STAT_CAUSE_DESCR', 'CONT_DATE', 'CONT_DOY', 'CONT_TIME', 
    'FIRE_SIZE', 'FIRE_SIZE_CLASS', 'LATITUDE', 'LONGITUDE', 'OWNER_CODE',
    'OWNER_DESCR', 'STATE', 'COUNTY', 'FIPS_CODE', 'FIPS_NAME', 'DIS_DATETIME',
     'CON_DATETIME', 'DISC_YM']


def test_df_columns():
    df = load_data(nrow=100)
    df_column = list(df.columns)

    assert df_column == expected_columns

