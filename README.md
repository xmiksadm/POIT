# POIT
Záverečné zadanie z predmetu Pokročilé informačné technológie

Monitorovanie vlhkosti a teploty pomocou senzoru DHT11

## Potrebná knižnica
https://github.com/adafruit/Adafruit_Python_DHT

## Inštalovanie závislostí

Python 2:
```
sudo apt-get update
sudo apt-get install python-pip
sudo python -m pip install --upgrade pip setuptools wheel
sudo pip install Adafruit_DHT --install-option="--force-pi"
```


Python 3:
```
sudo apt-get update
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT --install-option="--force-pi"
```

## Možnosť 1: Inštalovanie cez pip
Python 2:
```
sudo pip install Adafruit_DHT
```
Python 3:
```
sudo pip3 install Adafruit_DHT
```

## Možnosť 2: Inštalovanie a kompilácia z repozitára
Najprv si stiahnite zdrojový kód knižnice zo [stránky vydaní](https://github.com/adafruit/Adafruit_Python_DHT/releases) GitHubu, rozbaľte archív a vykonajte:

Python 2:
```
cd Adafruit_Python_DHT
sudo python setup.py install
```
Python 3:
```
cd Adafruit_Python_DHT
sudo python3 setup.py install
```