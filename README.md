# Edistynyt tiedonhallinta palautus oltp tietokannalla ja Fastapilla

## Ohjeet sovelluksen käynnistämiseen

1. Mukana on sqlworkbench file millä voi forward engineerata tietokanta, tässä tapauksessa käytämme Xampp ohjelmistoa.
   
2. Asenna requirementit jos ne eivät asennu automaattisesti python -m pip install -r requirements.txt

3. Tietokannan ollessa Xampissa voit käynnistää konsolisovelluksen main.py tiedostosta

4. Sovelluksessa lisätään tietoa fakerilla, muista lisätä tietoa oikeassa järjestyksessä, muuten ei tieto mene tietokantaan.

5. Kun tiedot on lisätty tietokantaan voit tehdä konsolisovelluksesta valmiita aggregointeja

# Ohje Fastapin käynnistykseen

1. Ohjelma käynnistyy komentoriviltä uvicorn main_api:app
2. Selaimesta voi apia käydä testaamassa osoitteesta http://localhost:8000/docs