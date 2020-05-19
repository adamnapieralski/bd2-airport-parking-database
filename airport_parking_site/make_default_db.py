import sys
import generate_data as gd
from sqlalchemy import create_engine
import pandas as pd


def make_default_db(filename):
    engine = create_engine('sqlite:///' + filename, echo=True)
    con = engine.connect()

    tab_name = "Strefa"
    strefa_df = gd.get_strefa_df()
    strefa_df.to_sql(tab_name, con, if_exists='replace', index_label="id_strefy")

    tab_name = "Cennik"
    cennik_df = gd.get_cennik_df()
    cennik_df.to_sql(tab_name, con, if_exists='replace', index_label="id_cennika")

    tab_name = "Parking"
    parking_df = gd.get_parking_df()
    parking_df.to_sql(tab_name, con, if_exists='replace', index_label="id_parkingu")

    tab_name = "Rodzaj_parkingu"
    rodzaj_parkingu_df = gd.get_rodzaj_parkingu_df()
    rodzaj_parkingu_df.to_sql(tab_name, con, if_exists='replace', index=False)

    tab_name = "Miejsce_parkingowe"
    miejsce_parkingowe_df = gd.get_miejsce_parkingowe_df()
    miejsce_parkingowe_df.to_sql(tab_name, con, if_exists='replace', index_label="id_mp")

    tab_name = "Typ_pojazdu"
    typ_pojazdu_df = gd.get_typ_pojazdu_df()
    typ_pojazdu_df.to_sql(tab_name, con, if_exists='replace', index=False)

    tab_name = "Metoda_platnosci"
    metoda_platnosci_df = gd.get_metoda_platnosci_df()
    metoda_platnosci_df.to_sql(tab_name, con, if_exists='replace', index=False)

    tab_name = "Znizka"
    znizka_df = gd.get_znizka_df()
    znizka_df.to_sql(tab_name, con, if_exists='replace', index_label="id_znizki")

    tab_name = "Kara"
    kara_df = gd.get_kara_df()
    kara_df.to_sql(tab_name, con, if_exists='replace', index_label="id_kary")

    con.close()

if __name__ == "__main__":
    make_default_db(sys.argv[1])
