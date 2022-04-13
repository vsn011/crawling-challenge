OVERVIEW
Ovaj program se sastoji iz dva dela:
1. Prvi deo je namenjen prikupljanju podataka sa sajta "" na osnovu zadatih parametara. Parametre pretrage poput distribition type, estate type and location ids je moguce promeniti u docker configuracionom fajlu. Url sajta za pristup (access token) i pretragu je moguce prebaciti u konfiguraction fajl, medjutim, kako je za vecinu sajtova drugacija struktura podataka koja se salje i prima, nije bilo potrebe za ovim korakom. Ovaj taks je implementiran kao python service sa 2 funkcionalnosti:
  1a Prva funkcionalnost je prikupljanje podataka sa zadatog sajta i upis u fajl samo prilikom pokretanja ovog programa
  1b Druga funkcionalnost je periodicno prikupljanje podataka u odredjenom periodu i upis u bazu.
  Izbor funkcionalnosti kao i period za drugu funkcionalnost se vrsi u docker config fajlovima.
  
  //Predlog za unapredjenje prvog dela je provera da li je token istekao ili ne
  
2. Drugi deo programa je namenjen ucitavanju big files i pretraga duplikata u istom ili razlicitim fajlovima. Fajlovi koji se ucitavaju se nalaze u folderu files (moguce je promeniti u konfiguraciji), dok se rezultat ispisuje u odvojenom fajlu - folder u kome se nalazi rezultat moze da se definise u konfiguraciji dockera.
Kako su trenutno ucitani jsonl fajlovi, without out of the box python functionalities, new function for reading these files have been implemented - first each row of the file will be read in list of strings, each list element will transform into dictionary object using out of the box python functionalities and transported into data frame with additional collumn - file name which shoudl represent platfrom from which data is comming.
After data analysis, currently only way that we can get some duplicate values is by getting duplicates based on the next columns (....) . Collumns can be changed in program configuration file if necessary. Since we don't want to get data with empty columns as duplicate, first these columns will be removed. New key from defined columns will be created and based on that key and out of the box python pandas funcitonalities subset of duplicate values have been generated.



Instructions:
There are two different dockers for each homework task.
Each docker should be started with commands:
`docker-compose build`
`docker-compose up`

