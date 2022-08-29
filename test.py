from utils import load_data


expected_columns = ['OBJECTID', 'FIRE_CODE', 
    'FIRE_NAME', 'FIRE_YEAR', 'DISCOVERY_DOY', 
    'DISCOVERY_TIME', 'STAT_CAUSE_CODE', 
    'STAT_CAUSE_DESCR', 'CONT_DATE', 'CONT_DOY', 'CONT_TIME', 
    'FIRE_SIZE', 'FIRE_SIZE_CLASS', 'LATITUDE', 'LONGITUDE', 'OWNER_CODE',
    'STATE', 'COUNTY', 'FIPS_CODE', 'FIPS_NAME',
    'DIS_DATETIME','CON_DATETIME', 'DISC_YM']


def test_df_columns():
    df = load_data(nrows=100)
    df_column = list(df.columns)

    assert df_column == expected_columns

