# aws-lamda-exploration
## Co to jest ?
AWS lambda to usługa amazona polegająca, mniej w wiecej, na możliwości uruchamiania kodu (funkcji) w zdalnym środowisku.
  
### Wartość usługi
Usługa koncentruje się na przygotowaniu/zapewnieniu środowiska do uruchomienia kodu, takich jak:

* moc obliczeniowa (CPU & RAM)
* dostęp do Internetu
* dostęp do innych usług Amazon (popularnie: S3, DynamoDB, Redshift, itd)

Dzięki czemu użytkownik amazon lambda nie ma potrzeby dbać o posiadanie serwera, na którym działałby jego kod, ani dbać o skalowalność swojej aplikacji ani dbać o inne elementy wymagane do działania kodu, może skupić się na przygotowaniu samej *funkcji* uzytkowej.

Rozwiązanie dobrze się skaluje (ponieważ amazon dba o uruchomienie *funkcji* w momencie gdy jest to wymagane, czas działania i responsywność jest taka sama, tak samo przy obciążeniu 10 użytkowników/s jak 10mln użytkowników/s. Jest to zdaniem autora najwartościowsza cecha usługi amazon lambda).

### Dostępne języki programowania *funkcji*
Obsługiwane języki to:

* Python
* java
* javascript  

### Uruchomienie *funkcji*
Funkcje zawierające logikę biznsesową po wysłaniu do repozytoriów Amazona, oczekują ich wywołanie/uruchomienie, dostępne triggery wywołania *funkcji* to:

* działania usług amazon, są to triggery, które możemy "wyklikać" w konsoli amazon:
    * **S3** - dodanie/usunięcie pliku do bucket'a
    * **DynamoDB** - działania na bazie
* dziania użytkownika:  
    * trigger polegający na wykonaniu zapytania HTTP pod specjalny endpoint

Jak można zauważyć Amazon Lambda realizuje paradygmat [**event-driven**](https://en.wikipedia.org/wiki/Event-driven_programming).

## Konsola AWS Lambda
Projektanci AWS przygotowali konsolę, gdzie można ręcznie tworzyć, edytować i testować *funkcje*

Opis:

Dashboard

    ![Imgur](http://i.imgur.com/jMghNwf.png)
    Po włączeniu **lambda dashboard** widać listę stworzonych funkcji


### Tworzenie i zarządzanie funkcjami

#### Tworzenie funkcji:

na pierwszym panelu możemy wybrać jakąś z przykładowych funkcji, ale polecam pominięcie tego kroku jako, że mamy przykłady funkcji w tym dokumencie

![Imgur](http://i.imgur.com/QUtl7D0.png)
    
klikamy **Skip**
    




#### Przykłady  

1. wylogowanie nazwy i typu pliku dodanego do koszyka S3, trywialny przypadek użycia, trochę lepszy hello world:

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
    
    ![Imgur](http://i.imgur.com/w6iQ9ih.png)
      
  
2. zapisanie danych do Amazon DynamoDB, cel: zobaczyć jak można wiązać dane z różnych usług amazona w przejrzysty sposób

        s3 = boto3.client('s3')
        dynamo = boto3.client('dynamodb')
        
        
        def lambda_handler(event, context):
            # Get the object from the event and get some its informations
            print "Received event: " + json.dumps(event, indent=3)
            bucket = event['Records'][0]['s3']['bucket']['name']
            file_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
            response = s3.get_object(Bucket=bucket, Key=file_name)
            content_type = response['ContentType']
        
            # create table UploadedFiles in dynamodb if not exists
            table_name = 'UploadedFiles'
            try:
                dynamo.describe_table(TableName=table_name)
            except Exception as e:
                dynamo.create_table(
                        AttributeDefinitions=[{'AttributeName': 'UUID', 'AttributeType': 'S',}, ],
                        TableName=table_name,
                        KeySchema=[{'AttributeName': 'UUID', 'KeyType': 'HASH',}],
                        ProvisionedThroughput={'ReadCapacityUnits': 123, 'WriteCapacityUnits': 123,},
                )
        
            # save data to dynamodb
            boto3.resource('dynamodb').Table(table_name).put_item(Item={
                'UUID': str(uuid4()),
                'bucket': bucket,
                'name': file_name,
                'content': content_type,
                'event': event,
                'context': str(context),
            })

    wynik z działania funkcj, dokument w bazie DynamoDB:
    
    ![Imgur](http://i.imgur.com/UE9aF8l.png) 


### setup environment

create user as:
http://docs.aws.amazon.com/lambda/latest/dg/setting-up.html

http://docs.aws.amazon.com/lambda/latest/dg/with-dynamodb-create-function.html