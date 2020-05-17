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
        
        long_term_tickets_num = int(0.3*tickets_num)
        short_term_tickets_num = tickets_num - long_term_tickets_num    

        clients_num = int(0.8*long_term_tickets_num)
        clients_df = self._generate_klient_df(clients_num)
        print(clients_df)
        vehicles_num = int(0.85*long_term_tickets_num)
        vehicles_df = self._generate_pojazd_df(clients_num, vehicles_num)
        print(vehicles_df)
        strefa_df = get_strefa_df()
        
        bilety_krotko_df = self._get_bilet_krotkookresowy_df(short_term_tickets_num, strefa_df)
        print(bilety_krotko_df)        

        bilety_dlugo_df = self._get_bilet_dlugookresowy_df(short_term_tickets_num, strefa_df)
        print(bilety_dlugo_df) 

        # reservations_df = self._generate_rezerwacja_df(ticket_ids, clients_num, vehicles_num, parkig_slots_num)
        # print(reservations_df)

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

    def _generate_rezerwacja_df(self, ticket_ids, clients_num, vehicles_num, parkig_slots_num):
        df = pd.DataFrame(columns=['nr_rezerwacji', 'data_rozpoczecia', 'data_zakonczenia', 'klient',
                                    'bilet_dlugoterminowy', 'miejsce_parkingowe'])
        num = ticket_ids.size
        df['nr_rezerwacji'] = np.arange(1, ticket_ids.size+1)
        begin_dates = [datetime.date(np.random.randint(2018, 2021), np.random.randint(1,13),
                                np.random.randint(1,29)) for x in range(num)] 
        df['data_rozpoczecia'] = [d.isoformat() for d in begin_dates]
        time_deltas = [datetime.timedelta(days=np.random.randint(1,12)) for x in range(num)]    
        end_dates = np.array(begin_dates) + np.array(time_deltas)
        df['data_zakonczenia'] = [d.isoformat() for d in end_dates]
        df['klient'] = np.random.randint(0, clients_num, num)
        parkins_slots = np.arange(0, parkig_slots_num)
        df['miejsce_parkingowe'] = np.random.choice(parkins_slots, num, replace=False)
        df['bilet_dlugoterminowy'] = ticket_ids   
        return df

    def _get_bilet_krotkookresowy_df(self, num, strefa_df):
        df = pd.DataFrame(columns=['nr_biletu', 'czas_wjazdu', 'czas_wyjazdu', 'wykupiony_czas', 'id_strefy'])    
        df['nr_biletu'] = np.arange(1, num+1)
        begin_datetimes = [datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
                        np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59)) for x in range(num)] 
        df['czas_wjazdu'] = [d.isoformat() for d in begin_datetimes]
        time_deltas = [datetime.timedelta(minutes=np.random.randint(10,600)) for x in range(num)]    
        end_datetimes = np.array(begin_datetimes) + np.array(time_deltas)
        df['czas_wyjazdu'] = [d.isoformat() for d in end_datetimes]    
        df['wykupiony_czas'] = [td.total_seconds() / 60 + int(np.random.normal(1) * 30) for td in time_deltas]

        typ_pojazdu = np.random.choice(['osobowy', 'motocykl', 'autokar'], num, p=[0.97, 0.02, 0.01])
        id_strefy = []
        for pojazd in typ_pojazdu:
            #id_parkingu < 3 znaczy ze strefa jest krotkoterminowa
            strefa = strefa_df[strefa_df['typ_pojazdu'] == pojazd][strefa_df['id_parkingu'] < 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
            index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
            id_strefy.append(index)
            strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1
        df['id_strefy'] = id_strefy
        return df

    def _get_bilet_dlugookresowy_df(self, num, strefa_df):
        df = pd.DataFrame(columns=['nr_biletu', 'czas_wjazdu', 'czas_wyjazdu', 'wykupiony_czas', 'id_strefy'])    
        df['nr_biletu'] = np.arange(1, num+1)
        begin_datetimes = [datetime.datetime(np.random.randint(2018, 2021), np.random.randint(1,13),
                        np.random.randint(1,29), np.random.randint(0,23), np.random.randint(0,59)) for x in range(num)] 
        df['czas_wjazdu'] = [d.isoformat() for d in begin_datetimes]
        time_deltas = [datetime.timedelta(days=np.random.randint(1,20), minutes=np.random.randint(10,600)) for x in range(num)]    
        end_datetimes = np.array(begin_datetimes) + np.array(time_deltas)
        df['czas_wyjazdu'] = [d.isoformat() for d in end_datetimes]    
        df['wykupiony_czas'] = [(int(td.total_seconds() / 86400) + 1 + int(np.random.normal(1)))*1440 for td in time_deltas]

        typ_pojazdu = np.random.choice(['osobowy', 'motocykl', 'autokar'], num, p=[0.97, 0.02, 0.01])
        id_strefy = []
        for pojazd in typ_pojazdu:
            #id_parkingu >= 3 znaczy ze strefa jest dlugoterminowa
            strefa = strefa_df[strefa_df['typ_pojazdu'] == pojazd][strefa_df['id_parkingu'] >= 3][strefa_df['liczba_wolnych_miejsc'] > 0].iloc[0]
            index = int(strefa['nazwa'][-1])-1 #glupie, ale nie mialem pomyslu jak to zrobic 
            id_strefy.append(index)
            strefa_df.loc[index, ('liczba_wolnych_miejsc')] -= 1
        df['id_strefy'] = id_strefy
        return df

if __name__ == "__main__":
    if len(sys.argv) == 2:
        dg = DataGenerator()
        dg.generate_data(int(sys.argv[1]))
    else:
        raise Exception('Wrong number of parameters. Number of tickets is required')