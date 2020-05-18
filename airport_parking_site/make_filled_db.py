import sys
import generate_data as gd
from sqlalchemy import create_engine
import pandas as pd
import make_default_db as mddb

def make_filled_db(filename, num):
    mddb.make_default_db(filename)

    engine = create_engine('sqlite:///' + filename, echo=False)
    con = engine.connect()

    dg = gd.DataGenerator()
    dg.generate_data(int(num))

    tab_name = "Klient"
    dg.klient_df.to_sql(tab_name, con, if_exists='replace', index_label="id_klienta")

    tab_name = "Pojazd"
    dg.pojazd_df.to_sql(tab_name, con, if_exists='replace', index=False)

    tab_name = "Bilet"
    dg.bilet_df.to_sql(tab_name, con, if_exists='replace', index_label="id_biletu")

    tab_name = "Rezerwacja"
    dg.rezerwacja_df.to_sql(tab_name, con, if_exists='replace', index_label="id_rezerwacji")

    tab_name = "Bilet_dlugoterminowy"
    dg.bilet_dlugoterminowy_df.to_sql(tab_name, con, if_exists='replace', index=False)

    tab_name = "Oplata"
    dg.oplata_df.to_sql(tab_name, con, if_exists='replace', index_label="id_oplaty")


if __name__ == "__main__":
    make_filled_db(sys.argv[1], sys.argv[2])