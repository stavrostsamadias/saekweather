import time
import requests
from bs4 import BeautifulSoup
import json
from sqlalchemy import create_engine,ForeignKey,Column,String,Date,Time,Integer,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import schedule
from googletrans import Translator
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib


#-----------------------------------get methot for API sensor-----------------------------------------



#---------------------------------Model for database object ------------------------------------------
Base=declarative_base()

class thermokrasies(Base):

    __tablename__="thermokrasies"

    id=Column("id",Integer,primary_key=True,autoincrement=True)
    date=Column("date",String(80),autoincrement=True)
    time=Column("time",String(80),autoincrement=True)
    Temperature=Column("Temperature",String(80))
    Humidity=Column("Humidity",String(80))
    Dew_Point=Column("Dew_Point",String(80))
    Wind=Column("Wind",String(80))
    barometer=Column("barometer",String(80))
    rain=Column("rain",String(80))
    rain_rate=Column("rain_rate",String(80))
    storm_total=Column("storm_total",String(80))
    monthly_rain=Column("monthly_rain",String(80))
    yearly_rain=Column("yearly_rain",String(80))
    wind_chill=Column("wind_chill",String(80))
    heat_index=Column("heat_index",String(80))
    sunrise=Column("sunrise",String(80))
    Sunset=Column("Sunset",String(80))
    latitude=Column("latitude",String(80))
    longitude = Column("longitude", String(80))
    QUALITY_OF_AIR=Column("QUALITY OF AIR",String(80))
    PM25=Column("PM25",String(80))
    CO=Column("CO",String(80))
    NO2=Column("NO2",String(80))
    O3=Column("O3",String(80))
    PM10=Column("PM10",String(80))
    SO2=Column("SO2",String(80))
    IMAGE=Column("IMAGE",String(80))
    weather_now=Column("weather",String(80))
    fwi_value=Column("fwi_value",String(80))
    vegetation_density=Column("vegetation_density",String(80))
    fire_risk=Column("fire_risk",String(80))

    def __init__(self,date,time,Temperature,Humidity,Dew_Point,Wind,barometer,rain,rain_rate,storm_total,monthly_rain,yearly_rain,wind_chill,heat_index,
                 sunrise,Sunset,latitude,longitude,QUALITY_OF_AIR,PM25,CO,NO2,O3,PM10,SO2,IMAGE,weather_now,fwi_value,vegetation_density,fire_risk):
        self.date=date
        self.time=time
        self.Temperature = Temperature
        self.Humidity = Humidity
        self.Dew_Point = Dew_Point
        self.Wind = Wind
        self.barometer= barometer
        self.rain = rain
        self.rain_rate = rain_rate
        self.storm_total = storm_total
        self.monthly_rain = monthly_rain
        self.yearly_rain = yearly_rain
        self.wind_chill = wind_chill
        self.heat_index = heat_index
        self.sunrise = sunrise
        self.Sunset = Sunset
        self.latitude= latitude
        self.longitude = longitude
        self.QUALITY_OF_AIR = QUALITY_OF_AIR
        self.PM25 = PM25
        self.CO = CO
        self.NO2 = NO2
        self.O3 = O3
        self.PM10 = PM10
        self.SO2 = SO2
        self.IMAGE = IMAGE
        self.weather_now = weather_now
        self.fwi_value=fwi_value
        self.vegetation_density=vegetation_density
        self.fire_risk=fire_risk

    def __repr__(self):
        return f"{self.date},{self.time}, {self.Temperature},{self.Humidity},{self.Dew_Point},{self.Wind},{self.barometer},{self.rain},{self.rain_rate},{self.storm_total},{self.monthly_rain},{self.yearly_rain},{self.wind_chill},{self.heat_index},{self.sunrise},{self.Sunset},{self.latitude},{self.longitude},{self.QUALITY_OF_AIR},{self.PM25},{self.CO},{self.NO2},{self.O3},{self.PM10},{self.SO2},{self.IMAGE},{self.weather_now},{self.fwi_value},{self.vegetation_density},{self.fire_risk}"

class stasion_termokrasies(Base):
    __tablename__="stasion"
    id_stasion = Column("id", Integer, primary_key=True, autoincrement=True)
    date_stasion = Column("date", String(80), autoincrement=True)
    time_stasion = Column("time", String(80), autoincrement=True)
    Temperature_stasion = Column("Temperature_stasion", String(80))
    Humidity_stasion = Column("Humidity_stasion", String(80))
    QM2_stasion = Column("Qm2_stasion", String(80))
    windspeed_stasion = Column("Wind", String(80))
    co2_stasion = Column("Co2", String(80))

    def __init__(self,date_stasion,time_stasion,Temperature_stasion,Humidity_stasion,QM2_stasion,windspeed_stasion,co2_stasion):
        self.date_stasion = date_stasion
        self.time_stasion = time_stasion
        self.Temperature_stasion = Temperature_stasion
        self.Humidity_stasion = Humidity_stasion
        self.QM2_stasion = QM2_stasion
        self.windspeed_stasion = windspeed_stasion
        self.co2_stasion = co2_stasion

    def __repr__(self):
        return f"{self.date_stasion},{self.time_stasion},{self.Temperature_stasion},{self.Humidity_stasion},{self.QM2_stasion},{self.windspeed_stasion},{self.co2_stasion}"


engine = create_engine("sqlite:///mydb.db",echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session=Session()


class MyClass:
    def __init__(self):
        engine = create_engine("sqlite:///mydb.db", echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get(self):
        url_get_api = "https://stayrostsamadias.pythonanywhere.com/api/get"
        data_get_api = requests.get(url_get_api)

        data_transform_list = data_get_api.json()
        data_transform_dic = data_transform_list[0]

        self.co2 = data_transform_dic['co']
        self.humidity = data_transform_dic['humidity']
        self.qm2 = data_transform_dic['pm2']
        self.temp = data_transform_dic['temp']
        self.windspeed = data_transform_dic['windspeed']
        now = datetime.now()
        self.time_stasion=now.strftime("%H:%M:%S")
        self.date_stasion=now.strftime("%d-%m-%Y")
        print(self.co2)
        print(self.humidity)
        print(self.qm2)
        print(self.temp)
        print(self.windspeed)
        print(self.time_stasion)
        print(self.date_stasion)


        database_rec1=stasion_termokrasies(self.date_stasion,self.time_stasion,self.temp,self.humidity,self.qm2,self.windspeed,self.co2)
        self.session.add(database_rec1)
        self.session.commit()

        #--------------------------------webscraping -----------------------------------------------------------#
        url="https://penteli.meteo.gr/stations/aitoliko/"
        page=requests.get(url=url)
        soup=BeautifulSoup(page.text,'html.parser')
        #print(soup)
        ref=soup.findAll('div',class_='lright')
        ref1=soup.findAll('span')
        #print(ref1)
        b=0
        times={}
        for i in ref1:
            #print(b,":",i.text)
            times.update({b:i.text})
            b=b+1
        url3="https://weather.com/el-GR/forecast/air-quality/l/b72dab8a55d9dd12cc1ed34d15166ed4e79d8067377ef28e2b15a6b2179b55a1"
        page1=requests.get(url=url3)
        soup1=BeautifulSoup(page1.text,'html.parser')
        #print(soup)
        ref2=soup1.findAll('text',class_='DonutChart--innerValue--3_iFF AirQuality--extendedDialText--1kqIb')

        #ref1=soup.findAll('span')
        #print(ref2)
        self.poiothta=[]
        for i in ref2:
            #print(i.text)
            self.poiothta.append(i.text)


        ref3=soup1.findAll('text',class_='DonutChart--innerValue--3_iFF AirQuality--pollutantDialText--2Q5Oh')
        #print(ref3)

        for i in ref3:
            #print(i.text)
            self.poiothta.append(i.text)

        #print (times.values())

        url4="https://www.meteofarm.gr/%CF%80%CF%81%CF%8C%CE%B3%CE%BD%CF%89%CF%83%CE%B7-%CE%BA%CE%B1%CE%B9%CF%81%CE%BF%CF%8D/%CE%BC%CE%B5%CF%83%CE%BF%CE%BB%CF%8C%CE%B3%CE%B3%CE%B9"
        page5=requests.get(url=url4)
        soup5=BeautifulSoup(page5.text,'html.parser')
        #print(soup)
        ref5=soup5.findAll('img')
        #ref1=soup.findAll('span')
        #print(ref2)
        image=[]
        b=0
        for i in ref5:
            #print (b,":",i)
            image.append(i)
            b=b+1
        self.eikona=image[4].get("src")

        url6="https://www.meteoprog.com/el/weather/Mesolongi/"
        page6=requests.get(url=url6)
        soup6=BeautifulSoup(page6.text,'html.parser')
        #print(soup)
        ref6=soup6.findAll('h3')
        #ref1=soup.findAll('span')
        #print(ref2)
        kairos_is=[]
        b=0
        for i in ref6:
            #print (b,":",i)
            kairos_is.append(i.text)
            b=b+1

        self.kairos_einai=kairos_is[0]


        self.Temperature=times[13]
        self.Humidity=times[16]
        self.Dew_Point=times[19]
        self.Wind=times[22]
        self.barometre=times[25]
        self.rain=times[28]
        self.rain_rate=times[31]
        self.storm_total=times[34]
        self.monthly_rain=times[37]
        self.yearly_rain=times[40]
        self.wind_chill=times[43]
        self.heat_index=times[46]
        self.sunrise=times[49]
        self.Sunset=times[52]
        self.latitude=38.37011455642275
        self.longitude=21.429736211480577



        '''translator=Translator()
        text=self.kairos_einai
        translation=translator.translate(text,src="el",dest="en")
        self.kairos_einai=translation.text'''



        print("Θερμοκρασία:",self.Temperature[0:4])
        print("Υγρασία:",self.Humidity[0:3])
        print("Σημείο Δρόσου:",self.Dew_Point[0:3])
        print("Άνεμος:",self.Wind[0:3])
        print("Βαρόμετρο:",self.barometre[0:6])
        print("Σημερινός Υετός:",self.rain[0:3])
        print("Ραγδαιότητα:",self.rain_rate[0:3])
        print("Τρέχουσα κακοκαιρία:",self.storm_total[0:3])
        print("Μηνιαίος Υετός:",self.monthly_rain[0:4])
        print("Ετήσιος Υετός:",self.yearly_rain[0:4])
        print("Αίσθηση ψύχους:",self.wind_chill[0:4])
        print("Δείκτης δυσφορίας:",self.heat_index[0:4])
        print("Ανατολή:",self.sunrise)
        print("Δύση:",self.Sunset)
        print("ΣΥΝΤΕΤΑΓΜΕΝΕΣX:",self.latitude)
        print("ΣΥΝΤΕΤΑΓΜΕΝΕΣY:", self.longitude)
        print("Ποιότητα του αέρα:",self.poiothta[0])
        print("PM2.5:",self.poiothta[1])
        print("CO:",self.poiothta[2])
        print("NO2:",self.poiothta[3])
        print("O3:",self.poiothta[4])
        print("PM10:",self.poiothta[5])
        print("SO2:",self.poiothta[6])
        print ("ΕΙΚΟΝΑ link:",self.eikona)
        print("Ο ΚΑΙΡΟΣ ΕΙΝΑΙ:",self.kairos_einai)
        self.Temperature = self.Temperature[0:4]
        print(round(float(self.Temperature[0:4])))
        temperature=round(float(self.Temperature[0:4]))
        self.Humidity = self.Humidity[0:3]
        humidity=round(float(self.Humidity))
        self.Dew_Point = self.Dew_Point[0:4]
        self.Wind = self.Wind[0:4]
        wind=round(float(self.Wind))
        self.barometer = self.barometre[0:6]
        self.rain = self.rain[0:2]
        rain=round(float(self.rain))
        self.rain_rate = self.rain_rate[0:3]
        self.storm_total = self.storm_total[0:4]
        self.monthly_rain = self.monthly_rain[0:4]
        self.yearly_rain = self.yearly_rain[0:5]
        self.wind_chill = self.wind_chill[0:4]
        self.heat_index = self.heat_index[0:4]
        self.sunrise = self.sunrise
        self.Sunset = self.Sunset
        self.latitude = self.latitude
        self.longitude = self.longitude
        self.QUALITY_OF_AIR= self.poiothta[0]
        self.PM25a = self.poiothta[1]
        self.CO = self.poiothta[2]
        self.NO2 = self.poiothta[3]
        self.O3 = self.poiothta[4]
        self.PM10 = self.poiothta[5]
        self.SO2 = self.poiothta[6]
        self.IMAGE = self.eikona
        self.weather_now = self.kairos_einai


        # Υπολογισμός του FWI βασισμένος στις παραπάνω μεταβλητές
        fwi = 0.0272 * int(wind) * (1.77 * int(humidity) / 100.0) ** 0.61 * (int(temperature) - 32.0) / 1.8 - 0.0288 * int(rain) + 2.52


        self.fwi_value =fwi
        '''
        if area < 0.25:
        return "Χαμηλή Πυκνότητα"
    elif 0.25 <= area < 0.5:
        return "Μέτρια Πυκνότητα"
    elif 0.5 <= area < 0.75:
        return "Υψηλή Πυκνότητα"
    elif area >= 0.75:
        return "Πολύ Υψηλή Πυκνότητα"
    else:
        return "Άγνωστη Κατηγορία"
        '''
        self.vegetation_density=0.5
        # Υποθέτουμε ότι έχουμε ήδη τους παράγοντες για θερμοκρασία, υγρασία, ταχύτητα ανέμου και πυκνότητα βλάστησης
        self.fire_risk=(temperature * humidity * wind * self.vegetation_density)/100


        data_rec2=thermokrasies(self.date_stasion,self.time_stasion,self.Temperature,self.Humidity,self.Dew_Point,self.Wind,self.barometer,self.rain,self.rain_rate,self.storm_total,self.monthly_rain,self.yearly_rain,self.wind_chill,self.heat_index,self.sunrise,self.Sunset,self.latitude,self.longitude,self.QUALITY_OF_AIR,self.PM25a,self.CO,self.NO2,self.O3,self.PM10,self.SO2,self.IMAGE,self.weather_now,self.fwi_value,self.vegetation_density,self.fire_risk)
        session.add(data_rec2)
        session.commit()

        self.ai()

    def ai(self):
        #-----------------------------------------------------------------pretiction ------------------------------------------------------

        self.date_stasion = self.session.query(stasion_termokrasies.date_stasion).all()
        self.time_stasion = self.session.query(stasion_termokrasies.time_stasion).all()
        self.Temperature_stasion = self.session.query(stasion_termokrasies.Temperature_stasion).all()
        self.Humidity_stasion = self.session.query(stasion_termokrasies.Humidity_stasion).all()
        self.QM2_stasion = self.session.query(stasion_termokrasies.QM2_stasion).all()
        self.windspeed_stasion = self.session.query(stasion_termokrasies.windspeed_stasion).all()
        self.co2_stasion = self.session.query(stasion_termokrasies.co2_stasion).all()




        self.date = self.session.query(thermokrasies.date).all()
        self.time = self.session.query(thermokrasies.time).all()
        self.Temperature = self.session.query(thermokrasies.Temperature).all()
        self.Humidity = self.session.query(thermokrasies.Humidity).all()
        self.Dew_Point = self.session.query(thermokrasies.Dew_Point).all()
        self.Wind = self.session.query(thermokrasies.Wind).all()
        self.barometer = self.session.query(thermokrasies.barometer).all()
        self.rain = self.session.query(thermokrasies.rain).all()
        self.rain_rate = self.session.query(thermokrasies.rain_rate).all()
        self.storm_total = self.session.query(thermokrasies.storm_total).all()
        self.monthly_rain = self.session.query(thermokrasies.monthly_rain).all()
        self.yearly_rain = self.session.query(thermokrasies.yearly_rain).all()
        self.wind_chill = self.session.query(thermokrasies.wind_chill).all()
        self.heat_index = self.session.query(thermokrasies.heat_index).all()
        self.sunrise = self.session.query(thermokrasies.sunrise).all()
        self.Sunset = self.session.query(thermokrasies.Sunset).all()
        self.latitude = self.session.query(thermokrasies.latitude).all()
        self.longitude = self.session.query(thermokrasies.longitude).all()
        self.QUALITY_OF_AIR = self.session.query(thermokrasies.QUALITY_OF_AIR).all()
        self.PM25 = self.session.query(thermokrasies.PM25).all()
        self.CO = self.session.query(thermokrasies.CO).all()
        self.NO2 = self.session.query(thermokrasies.NO2).all()
        self.O3 = self.session.query(thermokrasies.O3).all()
        self.PM10 = self.session.query(thermokrasies.PM10).all()
        self.SO2 = self.session.query(thermokrasies.SO2).all()
        self.weather_now = self.session.query(thermokrasies.weather_now).all()
        self.fwi_value=self.session.query(thermokrasies.fwi_value).all()
        self.vegetation_density=self.session.query(thermokrasies.vegetation_density).all()
        self.fire_risk=self.session.query(thermokrasies.fire_risk).all()
        #-------------------------------------------------------------------------------------------------------


        # Αποθηκεύστε τα αποτελέσματα των ερωτημάτων σας σε μεταβλητές
        date_stasion = [result[0] for result in self.session.query(stasion_termokrasies.date_stasion).all()]
        time_stasion = [result[0] for result in self.session.query(stasion_termokrasies.time_stasion).all()]
        Temperature_stasion = [result[0] for result in
                               self.session.query(stasion_termokrasies.Temperature_stasion).all()]
        Humidity_stasion = [result[0] for result in self.session.query(stasion_termokrasies.Humidity_stasion).all()]
        QM2_stasion = [result[0] for result in self.session.query(stasion_termokrasies.QM2_stasion).all()]
        windspeed_stasion = [result[0] for result in self.session.query(stasion_termokrasies.windspeed_stasion).all()]
        co2_stasion = [result[0] for result in self.session.query(stasion_termokrasies.co2_stasion).all()]

        date = [result[0] for result in self.session.query(thermokrasies.date).all()]
        time = [result[0] for result in self.session.query(thermokrasies.time).all()]
        Temperature = [result[0] for result in self.session.query(thermokrasies.Temperature).all()]
        Humidity = [result[0] for result in self.session.query(thermokrasies.Humidity).all()]
        Dew_Point = [result[0] for result in self.session.query(thermokrasies.Dew_Point).all()]
        Wind = [result[0] for result in self.session.query(thermokrasies.Wind).all()]
        barometer = [result[0] for result in self.session.query(thermokrasies.barometer).all()]
        rain = [result[0] for result in self.session.query(thermokrasies.rain).all()]
        rain_rate = [result[0] for result in self.session.query(thermokrasies.rain_rate).all()]
        storm_total = [result[0] for result in self.session.query(thermokrasies.storm_total).all()]
        monthly_rain = [result[0] for result in self.session.query(thermokrasies.monthly_rain).all()]
        yearly_rain = [result[0] for result in self.session.query(thermokrasies.yearly_rain).all()]
        wind_chill = [result[0] for result in self.session.query(thermokrasies.wind_chill).all()]
        heat_index = [result[0] for result in self.session.query(thermokrasies.heat_index).all()]
        sunrise = [result[0] for result in self.session.query(thermokrasies.sunrise).all()]
        Sunset = [result[0] for result in self.session.query(thermokrasies.Sunset).all()]
        latitude = [result[0] for result in self.session.query(thermokrasies.latitude).all()]
        longitude = [result[0] for result in self.session.query(thermokrasies.longitude).all()]
        QUALITY_OF_AIR = [result[0] for result in self.session.query(thermokrasies.QUALITY_OF_AIR).all()]
        PM25 = [result[0] for result in self.session.query(thermokrasies.PM25).all()]
        CO = [result[0] for result in self.session.query(thermokrasies.CO).all()]
        NO2 = [result[0] for result in self.session.query(thermokrasies.NO2).all()]
        O3 = [result[0] for result in self.session.query(thermokrasies.O3).all()]
        PM10 = [result[0] for result in self.session.query(thermokrasies.PM10).all()]
        SO2 = [result[0] for result in self.session.query(thermokrasies.SO2).all()]
        weather_now = [result[0] for result in self.session.query(thermokrasies.weather_now).all()]
        fwi_value = [result[0] for result in self.session.query(thermokrasies.fwi_value).all()]
        vegetation_density = [result[0] for result in self.session.query(thermokrasies.vegetation_density).all()]
        fire_risk = [result[0] for result in self.session.query(thermokrasies.fire_risk).all()]

        # Τώρα δημιουργήστε το λεξικό data
        data = {
            "date_stasion": date_stasion,
            "time_stasion": time_stasion,
            "Temperature_stasion": Temperature_stasion,
            "Humidity_stasion": Humidity_stasion,
            "QM2_stasion": QM2_stasion,
            "windspeed_stasion": windspeed_stasion,
            "co2_stasion": co2_stasion,
            "date": date,
            "time": time,
            "Temperature": Temperature,
            "Humidity": Humidity,
            "Dew_Point": Dew_Point,
            "Wind": Wind,
            "barometer": barometer,
            "rain": rain,
            "rain_rate": rain_rate,
            "storm_total": storm_total,
            "monthly_rain": monthly_rain,
            "yearly_rain": yearly_rain,
            "wind_chill": wind_chill,
            "heat_index": heat_index,
            "sunrise": sunrise,
            "Sunset": Sunset,
            "latitude": latitude,
            "longitude": longitude,
            "QUALITY_OF_AIR": QUALITY_OF_AIR,
            "PM25": PM25,
            "CO": CO,
            "NO2": NO2,
            "O3": O3,
            "PM10": PM10,
            "SO2": SO2,
            "weather_now": weather_now,
            "fwi_value": fwi_value,
            "vegetation_density": vegetation_density,
            "fire_risk": fire_risk
            }

        # Δημιουργήστε το DataFrame από το λεξικό
        df = pd.DataFrame(data)

        # Τώρα μπορείτε να αποθηκεύσετε το DataFrame σε ένα αρχείο Excel
        df.to_excel('weather_data.xlsx', index=False)

        #-------------------------------------------------------------------ai-------------------------------------------------------------
        # Διαβάστε το αρχείο Excel με τα δεδομένα
        df = pd.read_excel('weather_data.xlsx')

        # Επιλέξτε τα χαρακτηριστικά που θέλετε να χρησιμοποιήσετε για την πρόβλεψη της θερμοκρασίας
        features = ['Temperature', 'Humidity', 'Dew_Point', 'Wind', 'barometer', 'rain', 'rain_rate',
                    'storm_total', 'monthly_rain', 'yearly_rain', 'wind_chill', 'heat_index',
                    'QUALITY_OF_AIR', 'PM25', 'CO', 'NO2', 'O3', 'PM10', 'SO2',
                    'fwi_value', 'vegetation_density', 'fire_risk']
        X = df[features]
        y = df['Temperature']  # Η θερμοκρασία είναι η στήλη που θέλουμε να προβλέψουμε

        # Διαχωρίστε τα δεδομένα σε σύνολα εκπαίδευσης και ελέγχου
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Δημιουργήστε ένα μοντέλο γραμμικής παλινδρόμησης
        model = LinearRegression()

        # Εκπαιδεύστε το μοντέλο στα δεδομένα εκπαίδευσης
        model.fit(X_train, y_train)

        # Αξιολογήστε το μοντέλο στα δεδομένα ελέγχου
        accuracy = model.score(X_test, y_test)
        print("Ακρίβεια του μοντέλου:", accuracy)

        # Κάντε προβλέψεις για τις επόμενες 4 ημέρες
        # Πρέπει να δημιουργήσετε το DataFrame με τα χαρακτηριστικά για αυτές τις ημέρες
        # Και μετά να καλέσετε τη μέθοδο predict() του μοντέλου για να προβλέψετε τις θερμοκρασίες

        # Αποθηκεύστε το μοντέλο σε ένα αρχείο για μελλοντική χρήση
        joblib.dump(model, 'temperature_prediction_model.pkl')



        #-----------------------------------------------------------------------------------------------------------------------------------
        """
        Διαχωρισμός των Δεδομένων: Διαχωρίστε τα δεδομένα σας σε ένα σύνολο εκπαίδευσης και ένα σύνολο ελέγχου. Το σύνολο εκπαίδευσης θα χρησιμοποιηθεί για την εκπαίδευση του μοντέλου, ενώ το σύνολο ελέγχου θα χρησιμοποιηθεί για την αξιολόγηση της απόδοσής του.

Εκπαίδευση του Μοντέλου: Εκπαιδεύστε το μοντέλο σας χρησιμοποιώντας το σύνολο εκπαίδευσης.

Αξιολόγηση του Μοντέλου: Χρησιμοποιήστε το σύνολο ελέγχου για να αξιολογήσετε την απόδοση του μοντέλου σας. Μπορείτε να χρησιμοποιήσετε μετρικές όπως η μέση απόκλιση, η μέση απόλυτη απόκλιση, το R^2 κλπ.

Διασταυρούμενη Επικύρωση (Cross-Validation): Εφαρμόστε τη διασταυρούμενη επικύρωση για να ελέγξετε την απόδοση του μοντέλου σε διαφορετικά υποσύνολα των δεδομένων. Αυτό μπορεί να σας δώσει μια πιο σταθερή εκτίμηση της απόδοσης.
        
        """
        # Διαβάζουμε τα δεδομένα από το αρχείο Excel
        df = pd.read_excel('weather_data.xlsx')

        # Μετατροπή των στηλών 'date' και 'time' σε μορφή datetime
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')

        # Τυπώνουμε το πρώτο χρονικό σημείο για επιβεβαίωση
        print("Πρώτη ημερομηνία:", df['date'].iloc[0])
        print("Πρώτη ώρα:", df['time'].iloc[0])

        # Χωρίζουμε τα δεδομένα σε χαρακτηριστικά (X) και στόχο (y)
        X = df[['Temperature', 'Humidity', 'Dew_Point', 'Wind', 'barometer', 'rain', 'rain_rate',
                    'storm_total', 'monthly_rain', 'yearly_rain', 'wind_chill', 'heat_index',
                    'QUALITY_OF_AIR', 'PM25', 'CO', 'NO2', 'O3', 'PM10', 'SO2',
                    'fwi_value', 'vegetation_density', 'fire_risk']]
        y = df['Temperature']

        # Διαχωρίζουμε τα δεδομένα σε σύνολο εκπαίδευσης και σύνολο ελέγχου (train-test split)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Δημιουργούμε και εκπαιδεύουμε το μοντέλο γραμμικής παλινδρόμησης
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Αξιολογούμε το μοντέλο στα δεδομένα ελέγχου
        accuracy = model.score(X_test, y_test)
        print("Ακρίβεια του μοντέλου στο σύνολο ελέγχου:", accuracy)

        # Εφαρμόζουμε διασταυρούμενη επικύρωση για πιο αξιόπιστη εκτίμηση της απόδοσης
        cv_scores = cross_val_score(model, X, y, cv=5)
        print("Διασταυρούμενη Επικύρωση (Cross-Validation) Αποτελέσματα:", cv_scores)
        print("Μέσος όρος Διασταυρούμενης Επικύρωσης (Cross-Validation Mean):", cv_scores.mean())


        #---------------------------προβλεψη----------------------------------------------------------------------------------------------------------
        # Προσδιορισμός της τελευταίας ημερομηνίας στα δεδομένα σου
        # Διαβάζετε τα ιστορικά δεδομένα από το Excel
        historical_data = pd.read_excel('weather_data.xlsx')

        # Υποθέτοντας ότι οι στήλες θερμοκρασίας και υγρασίας ονομάζονται 'Temperature' και 'Humidity' αντίστοιχα
        # Ανάλογα με τη δομή του αρχείου Excel σας, μπορεί να χρειαστεί να προσαρμόσετε αυτά τα ονόματα

        # Επιλέγετε τα τελευταία δεδομένα θερμοκρασίας και υγρασίας από το ιστορικό δεδομένων
        last_data = historical_data.tail(4)  # Υποθέτοντας ότι έχετε δεδομένα για τις τελευταίες 4 ημέρες

        # Δημιουργείτε το DataFrame new_data για τις προβλέψεις
        new_data = pd.DataFrame({
            'Temperature': last_data['Temperature'],  # Χρησιμοποιήστε τα τελευταία δεδομένα θερμοκρασίας
            'Humidity': last_data['Humidity'],  # Χρησιμοποιήστε τα τελευταία δεδομένα υγρασίας
            'Dew_Point': last_data['Dew_Point'],  # Χρησιμοποιήστε τα τελευταία δεδομένα σημείου δρόσου
            'Wind': last_data['Wind'],  # Χρησιμοποιήστε τα τελευταία δεδομένα ανέμου
            'barometer': last_data['barometer'],  # Χρησιμοποιήστε τα τελευταία δεδομένα βαρομετρικής πίεσης
            'rain': last_data['rain'],  # Χρησιμοποιήστε τα τελευταία δεδομένα βροχόπτωσης
            'rain_rate': last_data['rain_rate'],  # Χρησιμοποιήστε τα τελευταία δεδομένα ρυθμού βροχής
            'storm_total': last_data['storm_total'],
            # Χρησιμοποιήστε τα τελευταία δεδομένα συνολικής κατακρημνισμένης βροχόπτωσης
            'monthly_rain': last_data['monthly_rain'],  # Χρησιμοποιήστε τα τελευταία δεδομένα μηνιαίας βροχόπτωσης
            'yearly_rain': last_data['yearly_rain'],  # Χρησιμοποιήστε τα τελευταία δεδομένα ετήσιας βροχόπτωσης
            'wind_chill': last_data['wind_chill'],  # Χρησιμοποιήστε τα τελευταία δεδομένα ψύχους ανέμου
            'heat_index': last_data['heat_index'],  # Χρησιμοποιήστε τα τελευταία δεδομένα δείκτη θερμότητας
            'QUALITY_OF_AIR': last_data['QUALITY_OF_AIR'],  # Χρησιμοποιήστε τα τελευταία δεδομένα ποιότητας του αέρα
            'PM25': last_data['PM25'],  # Χρησιμοποιήστε τα τελευταία δεδομένα PM2.5
            'CO': last_data['CO'],  # Χρησιμοποιήστε τα τελευταία δεδομένα μονοξειδίου του άνθρακα
            'NO2': last_data['NO2'],  # Χρησιμοποιήστε τα τελευταία δεδομένα διοξειδίου του αζώτου
            'O3': last_data['O3'],  # Χρησιμοποιήστε τα τελευταία δεδομένα όζοντος
            'PM10': last_data['PM10'],  # Χρησιμοποιήστε τα τελευταία δεδομένα PM10
            'SO2': last_data['SO2'],  # Χρησιμοποιήστε τα τελευταία δεδομένα διοξειδίου του θείου
            'fwi_value': last_data['fwi_value'],  # Χρησιμοποιήστε τα τελευταία δεδομένα τιμής FWI
            'vegetation_density': last_data['vegetation_density'],
            # Χρησιμοποιήστε τα τελευταία δεδομένα πυκνότητας βλάστησης
            'fire_risk': last_data['fire_risk']  # Χρησιμοποιήστε τα τελευταία δεδομένα κινδύνου πυρκαγιάς
        })

        # Φορτώστε το εκπαιδευμένο μοντέλο από το αρχείο
        model = joblib.load('temperature_prediction_model.pkl')

        # Προβλέψτε τις θερμοκρασίες χρησιμοποιώντας το μοντέλο και τα δεδομένα new_data
        predictions = model.predict(new_data)

        # Εκτυπώστε τις προβλεπόμενες θερμοκρασίες
        print("Προβλεπόμενες θερμοκρασίες:")
        print(predictions)
        #------------------------------------------------------τελος προβλεψεις καιρου ------------------------------
        # Προσθήκη των ονομάτων των στηλών temp_day1, temp_day2, κλπ. στο DataFrame
        for i in range(1, 5):
            column_name = f'temp_day{i}'
            df[column_name] = np.nan  # Δημιουργία στήλης με NaN τιμές

        # Διαβάζουμε το αρχείο Excel με τα δεδομένα
        df = pd.read_excel('weather_data.xlsx')

        # Προσθέτουμε τις προβλεπόμενες τιμές στις αντίστοιχες στήλες
        df.loc[:, 'temp_day1'] = predictions[0]
        df.loc[:, 'temp_day2'] = predictions[1]
        df.loc[:, 'temp_day3'] = predictions[2]
        df.loc[:, 'temp_day4'] = predictions[3]

        # Αποθηκεύουμε το DataFrame στο αρχείο Excel, χωρίς να σβήσουμε τα υπάρχοντα δεδομένα
        df.to_excel('weather_data.xlsx', index=False)

    def execute_methods(self):
            # Καλέστε τις μεθόδους get και ai εδώ
            self.get()
            self.ai()

    def schedule_tasks(self):
        # Χρονοπρογραμματισμός εκτέλεσης των μεθόδων κάθε 10 λεπτά
        schedule.every(1).minutes.do(self.execute_methods)

        # Άλλες πιθανές εργασίες χρονοπρογραμματισμού μπορούν να προστεθούν εδώ

        # Επανάληψη του χρονοπρογράμματος
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    my_instance = MyClass()
    my_instance.schedule_tasks()


