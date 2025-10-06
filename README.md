# Tietokantaprojekti

## Tähän mennessä toteutettu toiminnallisuus:


 -Käyttäjä voi luoda tunnuksen sivustolle
 
 -Käyttäjä voi luoda myynti-ilmoituksen sivustolle, joita voi myös jälkeenpäin muokata ja poistaa

 -Käyttäjällä on oma sivu jossa kerrotaan myynti-ilmoitusten määrä, jotka ovat myös näkyvillä

 -myynti-ilmoituksille voi asettaa luokkia

 -Etusivulla on näkymä sovelluksessa olevista myynti-ilmoituksista

 -Myynti-ilmoituksilla on omat sivut, jossa on ilmoituksen informaatiota

 -Myynti-ilmoituksia voi hakea hakusanoilla

 -Myynti-ilmoituksiin voi laittaa huutoja

 ## Sovelluksen testaus:

 -Luo haluamaasi paikkaan hakemisto sovellusta varten ja aja hakemiston sisällä komentoikkunassa komento "git clone https://github.com/iironar/Tietokantaprojekti.git".
 
 -mene juuri kloonattuun hakemistoon komentoikkunalla ja tämän jälkeen aja komento "python3 -m venv venv", joka asentaa hakemistoon virtuaaliympäristön.
 
 -Tämän jälkeen aja komento "source venv/bin/activate" joka käynnistää virtuaaliympäristön, jonka jälkeen aja komento "pip install flask" käytettyä kirjastoa varten.
 
  -Tietokantojen alustus tapahtuu ajamalla ensin "sqlite3 database.db < schema.sql" ja tämän jälkeen
  "sqlite3 database.db < init.sql"

 -nyt sovelluksen pitäisi käynnistyä selaimen osoitteeseen 127.0.0.1:5000 ajamalla komento "flask run".

 
 
