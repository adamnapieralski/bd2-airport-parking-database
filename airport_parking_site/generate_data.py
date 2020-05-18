import sys, os
import pandas as pd
import numpy as np
import string
import datetime

## dane statyczne

def get_cennik_df():
    return pd.read_csv('dane/statyczne/bd2_cennik.csv')

def get_rodzaj_parkingu_df():
    return pd.read_csv('dane/statyczne/bd2_rodzaj_parkingu.csv')

def get_parking_df():
    return pd.read_csv('dane/statyczne/bd2_parking.csv')

def get_kara_df():
    return pd.read_csv('dane/statyczne/bd2_kara.csv')

def get_metoda_platnosci_df():
    return pd.read_csv('dane/statyczne/bd2_metoda_platnosci.csv')

def get_strefa_df():
    return pd.read_csv('dane/statyczne/bd2_strefa.csv')

def get_typ_pojazdu_df():
    return pd.read_csv('dane/statyczne/bd2_typ_pojazdu.csv')

def get_znizka_df():
    return pd.read_csv('dane/statyczne/bd2_znizka.csv')

def get_miejsce_parkingowe_df():
    strefa_df = get_strefa_df()
    parking_df = pd.DataFrame(columns=['nr_miejsca', 'strefa'])    
    for index, row in strefa_df.iterrows():
        pojemnosc = row['pojemnosc']
        temp = pd.DataFrame(np.array([np.arange(1, pojemnosc+1), np.full(pojemnosc, index)]).T, columns=['nr_miejsca', 'strefa'])    
        parking_df = parking_df.append(temp, ignore_index=True)
    return parking_df


## dane dynamiczne

class DataGenerator():
    def __init__(self):
        if not os.path.exists('dane/pobrane'):
            import download_data

        names_limit = 200
        
        self.female_names = pd.read_csv('dane/pobrane/lista_pierwszych_imion_%C5%BCe%C5%84skich_uwzgl_os_zmar%C5%82e_2020-01-21.csv').head(names_limit)["IMIĘ_PIERWSZE"]
        self.male_names = pd.read_csv('dane/pobrane/lista_pierwszych_imion_m%C4%99skich_uwzgl_os_zmar%C5%82e_2020-01-21.csv').head(names_limit)["IMIĘ_PIERWSZE"]
        self.female_surnames = pd.read_csv('dane/pobrane/Wykaz_nazwisk_%C5%BCe%C5%84skich_uwzgl_os__zmar%C5%82e_2020-01-22.csv').head(names_limit)["Nazwisko aktualne"]
        self.male_surnames = pd.read_csv('dane/pobrane/Wykaz_nazwisk_m%C4%99skich_uwzgl_os__zmar%C5%82e_2020-01-22.csv').head(names_limit)["Nazwisko aktualne"]

    def generate_data(self, tickets_num):
        print('Generating', tickets_num, 'tickets')
        
        # long_term_tickets_num = int(0.3*tickets_num)
        # short_term_tickets_num = tickets_num - long_term_tickets_num

        clients_num = int(0.24*tickets_num)
        clients_df = self._generate_klient_df(clients_num)
        print("KLIENCI\n", clients_df)
        vehicles_num = int(0.84*tickets_num)
        vehicles_df = self._generate_pojazd_df(clients_num, vehicles_num)
        print("POJAZDY\n", vehicles_df)
        strefa_df = get_strefa_df()
        miejsce_parkingowe_df = get_miejsce_parkingowe_df()
        print("MIEJSCA PARKINGOWE\n", miejsce_parkingowe_df)
        

        bilet_df, bilety_dlugo_ids = self._get_bilety_df(tickets_num, strefa_df)
        print("BILETY\n", bilet_df)

        rezerwacje_df = self._generate_rezerwacja_df(bilet_df, bilety_dlugo_ids, clients_num, vehicles_num, miejsce_parkingowe_df)
        print("REZERWACJE\n", rezerwacje_df)

        bilety_dlugo_df = self._get_bilety_dlugoterminowe_df(bilet_df, bilety_dlugo_ids)

        print("BILETY DLUGOTERMINOWE\n", bilety_dlugo_df)

        oplata_df = self._get_oplata_df(bilet_df, bilety_dlugo_ids)
        print("OPLATY\n", oplata_df)



    def _generate_license_numbers(self, num):
        signs = list(string.ascii_uppercase + string.digits)
        license_numbers_array = np.random.choice(signs, (num,8))
        license_numbers = np.array([''.join(x) for x in license_numbers_array])
        return license_numbers

    def _generate_pojazd_df(self, num, clients_num):
        df = pd.DataFrame(columns=['nr_rejestracyjny', 'typ_pojazdu', 'id_klienta'])
        df['nr_rejestracyjny'] = self._generate_license_numbers(num)
        df['id_klienta'] = np.random.randint(0, clients_num, num)
        #zakladam ze typy pojazdow to 0 - samochod, 1 - autokar, 2 - motocykl
        df['typ_pojazdu'] = np.random.choice([0,1,2], num, p=[0.9, 0.05, 0.05])    
        return df

    def _generate_klient_df(self, num):
        df = pd.DataFrame(columns=['imie', 'nazwisko', 'nr_telefonu'])
        female_num = int(0.5*num)
        male_num = num - female_num
        f_names = np.random.choice(self.female_names, female_num)    
        f_surnames = np.random.choice(self.female_surnames, female_num)    
        m_names = np.random.choice(self.male_names, male_num)    
        m_surnames = np.random.choice(self.male_surnames, male_num)  
        df['imie'] = np.concatenate((f_names, m_names))
        df['nazwisko'] = np.concatenate((f_surnames, m_surnames))
        df['nr_telefonu'] = np.random.randint(100000000, 999999999, num)
        return df.sample(frac=1).reset_index(drop=True)

    def _generate_rezerwacja_df(self, bilety_df, bilety_dlugo_ids, clients_num, vehicles_num, miejsce_parkingowe_df):
        df = pd.DataFrame(columns=['nr_rezerwacji', 'data_rozpoczecia', 'data_zakonczenia', 'klient',
                                    'bilet_dlugoterminowy', 'miejsce_parkingowe'])

        bilety_dlugo_df = bilety_df.iloc[bilety_dlugo_ids]
        num = bilety_dlugo_df['nr_biletu'].size
        df['nr_rezerwacji'] = np.arange(1, num+1)
        # begin_dates = [datetime.date(np.random.randint(2018, 2021), np.random.randint(1,13),
        #                         np.random.randint(1,29)) for x in range(num)]
        begin_dates = bilety_dlugo_df['czas_wjazdu'].to_numpy()
        # df['data_rozpoczecia'] = [d for d in begin_dates]
        df['data_rozpoczecia'] = [d.astype('M8[D]') for d in begin_dates]
        # time_deltas = [datetime.timedelta(days=np.random.randint(1,12)) for x in range(num)]    
        # end_dates = np.array(begin_dates) + np.array(time_deltas)
        end_dates = bilety_dlugo_df['czas_wyjazdu'].to_numpy()
        df['data_zakonczenia'] = [d.astype('M8[D]') for d in end_dates]
        df['klient'] = np.random.randint(0, clients_num, num)
        miejsca_parkingowe_dlugo_ids = self._get_miejsca_parkingowe_dlugo_ids(miejsce_parkingowe_df)
        df['miejsce_parkingowe'] = np.random.choice(miejsca_parkingowe_dlugo_ids, num, replace=False)
        df['bilet_dlugoterminowy'] = bilety_dlugo_ids
        return df

    # def _get_bilet_krotkookresowy_df(self, num, strefa_df):
    #     df = pd.DataFrame(columns=['nr_biletu', 'czas_wjazdu', 'czas_wyjazdu', 'wykupiony_czas', 'id_strefy'])    
    #     df['nr_biletu'] = np.arange(1, num+1)
    #     begin_datetimes = [datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
    #                     np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59)) for x in range(num)] 
    #     df['czas_wjazdu'] = [d for d in begin_datetimes]
    #     time_deltas = [datetime.timedelta(minutes=np.random.randint(10,600)) for x in range(num)]    
    #     end_datetimes = np.array(begin_datetimes) + np.array(time_deltas)
    #     df['czas_wyjazdu'] = [d for d in end_datetimes]    
    #     df['wykupiony_czas'] = [td.total_seconds() / 60 + int(np.random.normal(1) * 30) for td in time_deltas]

    #     typ_pojazdu = np.random.choice(['osobowy', 'motocykl', 'autokar'], num, p=[0.97, 0.02, 0.01])
    #     id_strefy = []
    #     for pojazd in typ_pojazdu:
    #         #id_parkingu < 3 znaczy ze strefa jest krotkoterminowa
    #         strefa = strefa_df[strefa_df['typ_pojazdu'] == pojazd][strefa_df['id_parkingu'] < 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
    #         index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
    #         id_strefy.append(index)
    #         strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1
    #     df['id_strefy'] = id_strefy
    #     return df

    # def _get_bilet_dlugookresowy_df(self, num, strefa_df):
    #     df = pd.DataFrame(columns=['nr_biletu', 'czas_wjazdu', 'czas_wyjazdu', 'wykupiony_czas', 'id_strefy'])    
    #     df['nr_biletu'] = np.arange(1, num+1)
    #     begin_datetimes = [datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
    #                     np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59)) for x in range(num)] 
    #     df['czas_wjazdu'] = [d for d in begin_datetimes]
    #     time_deltas = [datetime.timedelta(days=np.random.randint(1,20), minutes=np.random.randint(10,600)) for x in range(num)]    
    #     end_datetimes = np.array(begin_datetimes) + np.array(time_deltas)
    #     df['czas_wyjazdu'] = [d for d in end_datetimes]    
    #     df['wykupiony_czas'] = [(int(td.total_seconds() / 86400) + 1 + int(np.random.normal(1)))*1440 for td in time_deltas]

    #     typ_pojazdu = np.random.choice(['osobowy', 'motocykl', 'autokar'], num, p=[0.97, 0.02, 0.01])
    #     id_strefy = []
    #     for pojazd in typ_pojazdu:
    #         #id_parkingu >= 3 znaczy ze strefa jest dlugoterminowa
    #         strefa = strefa_df[strefa_df['typ_pojazdu'] == pojazd][strefa_df['id_parkingu'] >= 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
    #         index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
    #         id_strefy.append(index)
    #         strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1
    #     df['id_strefy'] = id_strefy
    #     return df

    def _get_bilety_df(self, num, strefa_df):
        bilety = pd.DataFrame(columns=['nr_biletu', 'czas_wjazdu', 'czas_wyjazdu', 'wykupiony_czas', 'id_strefy'])
        dlugo_ids = []

        nr_biletow = []
        czasy_wjazdow = []
        czasy_wyjazdow = []
        wykupione_czasy = []
        id_stref = []

        for i in range(num):
            nr_biletow.append(i+1)
            # stosunek liczby biletow krotko - dlugo
            typ_biletu = np.random.choice(["krotkookresowy", "dlugookresowy"], p=[0.8, 0.2])
            czas_wjazdu = None
            time_delta = None
            typ_pojazdu = np.random.choice(['osobowy', 'motocykl', 'autokar'], p=[0.97, 0.02, 0.01])
            if typ_biletu == "krotkookresowy":

                czas_wjazdu = datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13), 
                np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59))
                time_delta = datetime.timedelta(minutes=np.random.randint(10,600))

                strefa = strefa_df[strefa_df['typ_pojazdu'] == typ_pojazdu][strefa_df['id_parkingu'] < 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
                index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
                id_stref.append(index)
                strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1
            else:
                dlugo_ids.append(i)

                czas_wjazdu = datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
                        np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59))
                time_delta = datetime.timedelta(days=np.random.randint(1,20), minutes=np.random.randint(10,600))

                strefa = strefa_df[strefa_df['typ_pojazdu'] == typ_pojazdu][strefa_df['id_parkingu'] >= 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
                index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
                id_stref.append(index)
                strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1

            czasy_wjazdow.append(czas_wjazdu)
            czasy_wyjazdow.append(czas_wjazdu + time_delta)
            wykupione_czasy.append(time_delta.total_seconds() / 60 + int(np.random.normal(1) * 30))
        
        bilety['nr_biletu'] = nr_biletow
        bilety['czas_wjazdu'] = czasy_wjazdow
        bilety['czas_wyjazdu'] = czasy_wyjazdow
        bilety['wykupiony_czas'] = wykupione_czasy
        bilety['id_strefy'] = id_stref
        return bilety, dlugo_ids

    def _get_bilety_dlugoterminowe_df(self, bilet_df, bilety_dlugo_ids):
        bilet_dlugo_df = pd.DataFrame(columns=['id_biletu', 'id_rezerwacji'])
        bilet_dlugo_df['id_biletu'] = bilety_dlugo_ids
        bilet_dlugo_df['id_rezerwacji'] = np.arange(0, len(bilety_dlugo_ids))
        return bilet_dlugo_df


    def _get_oplata_df(self, bilet_df, bilety_dlugo_ids):
        df = pd.DataFrame(columns=['id_biletu', 'czas', 'kwota_podstawowa', 'kwota_ostateczna', 'status',
                                    'metoda_platnosci', 'id_znizki', 'id_kary'])
        num = bilet_df.shape[0]
        df['id_biletu'] = np.arange(0, num)    
        
        df['czas'] = [datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
                        np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59)) for x in range(num)]
        
        # czas powiazany z biletem
        czasy = []
        kwoty_podstawowe = []

        for i in range(num):
            if i in bilety_dlugo_ids:
                kwoty_podstawowe.append(np.random.randint(100, 1000))
                before_diff = datetime.timedelta(days=np.random.randint(1, 30), hours=np.random.randint(0, 23), minutes=np.random.randint(0, 59), seconds=np.random.randint(0, 59))
                czasy.append(bilet_df['czas_wjazdu'].values[i] - np.timedelta64(before_diff))
            else:
                kwoty_podstawowe.append(np.random.randint(10, 100))
                diff = np.timedelta64(datetime.timedelta(minutes=np.random.randint(2, 500), seconds=np.random.randint(0, 59)))
                pay_time = bilet_df['czas_wyjazdu'].values[i] - diff
                while pay_time <= bilet_df['czas_wjazdu'].values[i]:
                    diff = np.timedelta64(datetime.timedelta(minutes=np.random.randint(2, 500), seconds=np.random.randint(0, 59)))
                    pay_time = bilet_df['czas_wyjazdu'].values[i] - diff
                czasy.append(pay_time)
        df['kwota_podstawowa'] = kwoty_podstawowe
        df['czas'] = czasy
        # if czy_dlugoterminowy:
        #     df['kwota_podstawowa'] = np.random.randint(100, 1000, size=num)
        #     before_diff = np.array([datetime.timedelta(days=np.random.randint(1, 30), hours=np.random.randint(0, 23), minutes=np.random.randint(0, 59), seconds=np.random.randint(0, 59)) for x in range(num)])
        #     df['czas'] =  bilet_df['czas_wjazdu'] - before_diff

        # else:
        #     df['kwota_podstawowa'] = np.random.randint(10, 100, size=num)
        #     for i in range(num):
        #         diff = np.timedelta64(datetime.timedelta(minutes=np.random.randint(2, 500), seconds=np.random.randint(0, 59)))
        #         pay_time = bilet_df['czas_wyjazdu'].values[i]- diff
        #         while pay_time <= bilet_df['czas_wjazdu'].values[i]:
        #             diff = np.timedelta64(datetime.timedelta(minutes=np.random.randint(2, 500), seconds=np.random.randint(0, 59)))
        #             pay_time = bilet_df['czas_wyjazdu'].values[i] - diff
        #         df.loc[df.index[i], 'czas'] = pay_time
        znizka_df = get_znizka_df()
        kara_df = get_kara_df()

        df['id_znizki'] = np.random.choice([0, np.nan], num, p=[0.02, 0.98])
        df['id_kary'] = np.random.choice([0, np.nan], num, p=[0.02, 0.98])

        # wartosc ostateczna uwzgledniajaca znizki i kary
        znizki = df['id_znizki'].to_numpy().copy()
        kary = df['id_kary'].to_numpy().copy()
        for i in range(znizki.size):
            if np.isnan(znizki[i]):
                znizki[i] = 1
            else:
                znizki[i] = znizka_df['wartosc'].values[int(znizki[i])]
            if np.isnan(kary[i]):
                kary[i] = 1
            else:
                kary[i] = kara_df['wartosc'].values[int(kary[i])]
        df['kwota_ostateczna'] = df['kwota_podstawowa'] * znizki * kary
        df['status'] = np.random.choice([1,0], num, p=[0.9, 0.1])
        metoda_plat = get_metoda_platnosci_df()    
        df['metoda_platnosci'] = np.random.choice(metoda_plat['rodzaj'], num)

        return df

    def _get_miejsca_parkingowe_dlugo_ids(self, strefa_df):
        ids = strefa_df.index[strefa_df['strefa'] >= 3].tolist()
        return ids


if __name__ == "__main__":
    if len(sys.argv) == 2:
        dg = DataGenerator()
        dg.generate_data(int(sys.argv[1]))
    else:
        raise Exception('Wrong number of parameters. Number of tickets is required')