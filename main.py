import users
import categories
import rental_items
import selections


#python -m pip install -r requirements.txt





while True:
    _choice=input("Mitä haluat tehdä? (1=Lisää roolit\n"
                   "2=lisää käyttäjiä\n"
                    "3=lisää kategoriat\n" 
                    "4=lisää ominaisuudet\n" 
                    "5=lisää tuotteet\n"
                    "6=lisää ominaisuuksia tuotteisiin\n"
                    "7=vuokraa\n"
                    "8=Lainauksien määrä valitulta kuukaudelta viikottain\n"
                    "9=Lainauksien märää valitulta kuukaudelta päivittäin\n"
                    "10=Lainauksien määrä valitulta vuodelta kuukausittain\n"
                    "11=Kaikkien aikojen top 10. lainatuimmat tavarat\n"
                    "12=Top 10. lainatut tavarat valitulta vuodelta kuukausittain\n"
                    "13=Selvitä missä kuussa tavaroita lisätään järjestelmään eniten valittuna vuonna\n"
                    "q=lopeta):")
    if _choice == 'q':
        break

    elif _choice == "1":
        print("Lisätään roolit")
        users.insert_roles()

    elif _choice == "2":
        num_of_rows = input("Kuinka monta käyttäjää? (oletuksena 10):")
        if num_of_rows == "":
            num_of_rows = 10
        else:
            num_of_rows=int(num_of_rows)
        users.insert_users(num_of_rows)
    
    elif _choice == "3":
        categories.insert_categories()

    elif _choice == "4":
        rental_items.insert_features()

    elif _choice == "5":
        rental_items.insert_items()

    elif _choice == "6":
        rental_items.mix_features_and_items()

    elif _choice == "7":
        rental_items.rent_items()

    elif _choice == "8":
        year=input("Anna vuosi:")
        month=(input("Anna kuukausi:"))
        selections.query_1(year,month)

    elif _choice == "9":
        year=input("Anna vuosi:")
        month=(input("Anna kuukausi:"))
        selections.query_2(year,month)

    elif _choice == "10":
        year=input("Anna vuosi:")
        selections.query_3(year)
    
    elif _choice == "11":
        selections.allthetimeTop10()

    elif _choice == "12":
        year=input("Anna vuosi:")
        selections.query2_top10(year)
    
    elif _choice == "13":
        year=input("Anna vuosi:")
        selections.query3_top10(year)