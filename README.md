# aws-lamda-exploration
## Co to jest ?
AWS lambda to usługa amazona polegająca, mniej w wiecej, na możliwości uruchamiania kodu (funkcji) w zdalnym środowisku.
  
#### Wartość usługi
Usługa koncentruje się na przygotowaniu/zapewnieniu środowiska do uruchomienia kodu, takich jak:

* moc obliczeniowa (CPU & RAM)
* dostęp do Internetu
* dostęp do innych usług Amazon (popularnie: S3, DynamoDB, Redshift, itd)

Dzięki czemu użytkownik takiej usługi nie ma potrzeby dbać o posiadanie serwera, na którym działałby jego kod, dbać o skalowalność swojej aplikacji. Rozwiązanie dobrze się skaluje (ponieważ amazon dba o uruchomienie *funkcji* w momencie gdy jest to wymagane, czas działania i responsywność jest taka sama, tak samo przy obciążeniu 10 użytkowników/s jak 10mln użytkowników/s. Jest to zdaniem autora najwartościowsza cecha usługi amazon lambda).

#### Dostępne języki programowania *funkcji*
Obsługiwane języki to:

* Python
* java
* javascript  

#### Uruchomienie *funkcji*
Funkcje zawierające logikę biznsesową po wysłaniu do repozytoriów Amazona, oczekują ich wywołanie/uruchomienie, dostępne triggery wywołania *funkcji* to:

* działania usług amazon, są to triggery, które możemy "wyklikać" w konsoli amazon:
* * **S3** - dodanie/usunięcie pliku do bucket'a
* * **DynamoDB** - działania na bazie
* dziania użytkownika:  
* * trigger polegający na wykonaniu zapytania HTTP pod specjalny endpoint


#### Przykłady

1. wylogowanie nazwy i typu pliku dodanego do koszyka S3:  
        
        from __future__ import print_function
        import json
        import urllib
        import boto3
    
        s3 = boto3.client('s3')
    
        def lambda_handler(event, context):
            # Get the object from the event and show some its informations
            # get bucket name
            bucket = event['Records'][0]['s3']['bucket']['name']
            # get file name
            file_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
            # check content type
            response = s3.get_object(Bucket=bucket, Key=file_name)
            print("Watching bucket %s: new file %s has content type %s." % (bucket, file_name, response['ContentType']))
            # return important values from function for future use
            return (bucket, file_name, response['ContentType'])

    log z działania funkcji:
    ![Imgur](http://i.imgur.com/KHsnDir.png)
      
  
2. fdsgfd