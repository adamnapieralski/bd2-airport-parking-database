import generate_data as gd
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('sqlite:///save_pandas.db', echo=True)
con = engine.connect()
sqltab = "Strefa"
strefa_df = gd.get_strefa_df()
strefa_df.to_sql(sqltab, con, if_exists='replace')

con.close()
