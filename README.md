# aws-lamda-exploration
## Co to jest ?
AWS lambda to usługa Amazona polegająca, mniej wiecej, na możliwości uruchamiania kodu (funkcji) w zdalnym środowisku.
  
### Wartość usługi
Usługa koncentruje się na przygotowaniu/zapewnieniu środowiska do uruchomienia kodu, takiego jak:

* moc obliczeniowa (CPU & RAM)
* dostęp do Internetu
* dostęp do innych usług Amazon (popularnie: S3, DynamoDB, Redshift, itd)

Dzięki temu użytkownik Amazon lambda nie ma potrzeby dbać o posiadanie serwera, na którym działałby jego kod,
ani dbać o skalowalność swojej aplikacji ani dbać o inne elementy wymagane do działania kodu, może skupić się na 
przygotowaniu samej *funkcji* uzytkowej.

Rozwiązanie dobrze się skaluje (ponieważ Amazon dba o uruchomienie *funkcji* w momencie gdy jest to wymagane, czas 
działania i responsywność jest taka sama, tak samo przy obciążeniu 10 użytkowników/s jak 10mln użytkowników/s. Jest 
to zdaniem autora najbardziej wartościowa cecha usługi Amazon lambda).

### Plan kosztów

Amazon postanowił pobierać opłaty za:

* fakt uruchomienia funkcji (pierwsze 1mln free, kolejne $0.20 za milion) 
* czaso-ram
    * czas wykonania funkcji
    * ilość RAM użytego do wykonania funkcji
    * ceny $0.00001667 za GB*s (gigabajtosekundę)
    
Usługa dostępna w ramach Free Tier.

Więcej o cenniku [tutaj](https://aws.amazon.com/lambda/pricing/)

### Dostępne języki programowania *funkcji*
Obsługiwane języki to:

* Python
* java
* javascript  

### Uruchomienie *funkcji*
Funkcje zawierające logikę biznesową, po wysłaniu do repozytoriów Amazona, oczekują na wywołanie/uruchomienie, 
dostępne triggery wywołania *funkcji* to:

* działania usług Amazon, są to triggery, które możemy "wyklikać" w konsoli Amazon:
    * **S3** - dodanie/usunięcie pliku do bucket'a
    * **DynamoDB** - działania na bazie
* działania użytkownika:  
    * trigger polegający na wykonaniu zapytania HTTP pod specjalny endpoint

Jak można zauważyć, Amazon Lambda realizuje paradygmat [**event-driven**](https://en.wikipedia.org/wiki/Event-driven_programming).

## Konsola AWS Lambda
Projektanci AWS przygotowali konsolę, gdzie można ręcznie tworzyć, edytować i testować *funkcje*
### Dashboard
Po włączeniu **lambda dashboard** widać listę stworzonych funkcji

![Imgur](http://i.imgur.com/jMghNwf.png)
### Tworzenie i zarządzanie funkcjami
#### Tworzenie funkcji:
na pierwszym panelu możemy wybrać jakąś z przykładowych funkcji, ale autor poleca pominięcie tego kroku jako, że można
użyć funkcji z tego dokumentu

![Imgur](http://i.imgur.com/QUtl7D0.png)
    
klikamy **Skip**

#### Tworzenie funkcji
 
 Trzeba podać
  
 * nazwę dla funkcji (dowolną do identyfikacji)
 * opis
 * jezyk programowania (runtime)
 * kod funkcji
 * rolę z którą funkcja będzie wykonana: ponieważ w Amazonie cała autoryzacja przebiega z użyciem ról, które pozwalają
 na działania, np dostęp do usług (EC2, S3, DynamoDb, etc), lub szczegółowe zezwolenia (no zezwolenie
 na dodawanie obiektów do koszyka **test** w S3, ale bez innych praw), jesli nie ma potrzeby dodatkowych dostępów
 wystarczy użyć domyślnej roli **lambda_basic_execution** (jeśli jej nie mamy stworzonej w naszym koncie, wybranie jej 
 z rozwijanej listy przekieruje na stronę tworzenia roli) ([więcej tutaj](http://docs.aws.amazon.com/lambda/latest/dg/intro-permission-model.html) i [tutaj](http://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html))
 * uzupełnienie max RAM dla funkcji
 * uzupełnienie max czasu działania dla funkcji

![Imgur](http://i.imgur.com/SCUDYZC.png)

![Imgur](http://i.imgur.com/dd5V09s.png)


klikamy **Next**

#### Podsumowanie

![Imgur](http://i.imgur.com/UF9NCsu.png)

W oknie podsumowania nie ma wiele ciekawego, klikamy **Create function**

### Zarządzanie funkcją
Tutaj przydatne zakładki to:

* Event Sources - tam ustawiamy wydarzenie, po którym funkcja zostanie włączona, np nowy obiekt w koszyku S3
* Monitoring - tam widać monitoring funkcji + łatwy skok do logów z uruchomienia funkcji 

![Imgur](http://i.imgur.com/L8QMDkY.png)

#### Dodanie event source

Dla przykładu ustaimy event na wykonanie testowej funkcji po dodaniu pliku do koszyka S3 

1. Idzeimy do zakładki Event Sources
2. klikamy Add Event Source
3. wybieramy Event source type: S3
4. wybieramy bucket, którego będzie dotyczyło
5. wybieramy event type Object Created (all)
6. ewentualnie możemy ustawić 
    1. prefix (przydatne do zawężenia akcji do folderów w koszyku S3)
    2. postfix (przydatne do zawężenia akcji do rozszerzeń plików np ".jpg")
7. Klikamy submit

W ten sposób dodaliśmy wydarzenie, po którym funkcja zostanie uruchomiona, a szczegóły o tym wydarzeniu
zostaną przekazane do funkcji jako pierwszy argument (dane te są w postaci ~JSON).

### Testowanie funkcji

Zdaniem autora bardzo przydatna funkcja

![Imgur](http://i.imgur.com/ns1Iizt.png)

Testowanie polega na zmockowaniu danych o wydarzeniu (jako JSON), taki testowy event można zapisać i uruchamiać wielokrotnie.
Kliknięcie **Test** w lewym górnym rogu panelu uruchamia funkcję z danymi testowymi. Jesli wcześniej nie został zapisany żaden
mock z danymi wyświetli się okno do wprowadzenia dancyh (jak na obrazku poniżej). Dane te można w każdej chwili zmienić
z użyciem menu **Actions/Configure test event** w lewym górnym rogu.

Wynik działania testu funkcji pojawia się na dole ekranu.


### Monitoring

W zakładce monitoring znajdziemy różne statystyki odnośnie wykonania funkcji.
Znajdziemy również link **View logs in CloudWatch** gdzie można zobaczyć logi z działania funkcji

## Przykłady  

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
      
  
2. zapisanie danych do Amazon DynamoDB, cel: zobaczyć jak można wiązać dane z różnych usług Amazona w przejrzysty sposób

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

3. Micro Service
        
        dynamo = boto3.client('dynamodb')
        table_name = 'MicroServiceDB'
        
        def ensure_table_exists():
            try:
                dynamo.describe_table(TableName=table_name)
                return boto3.resource('dynamodb').Table(table_name)
            except ClientError as e:
                if e.message.startswith(
                        'An error occurred (ResourceNotFoundException) when calling the DescribeTable operation: Requested resource not found: Table'):
                    print "Creating table %s in DynamoDB" % table_name
                    dynamo.create_table(
                            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S',}, ],
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH',}],
                            ProvisionedThroughput={'ReadCapacityUnits': 123, 'WriteCapacityUnits': 123,},
                    )
                    return boto3.resource('dynamodb').Table(table_name)
                else:
                    raise
         
        def insert_item(data):
            table = ensure_table_exists()
            table.put_item(Item={
                'id': str(uuid4()),
                'data': data
            })
            return 'OK'
        
        def list_items(data):
            table = ensure_table_exists()
            result = table.scan()['Items']
            return result
        
        def lambda_handler(event, context):
            print "Event: %s" % json.dumps(event)
            try:
                operation = globals()[event['method']]
                result = operation(event['params'])
                return {'jsonrpc': '2.0', 'result': result, 'id': event.get('id', '-1')}
            except KeyError:
                return {'jsonrpc': '2.0', 'error': 'method %s not found' % event['method'], 'id': event.get('id', '-1')}


    Do nowej funkcji należy dodać endpoint http w zakładce API endpoints, większość opcji pozostawiamy domyślne, 
    metodę zmieniamy na POST, autoryzacja we własnym zakresie (można użyć api-key).
    Pełny adres do zapytań jest wyświetlany w zakładce API endpoints.
    
    Tak przygotowana funkcja jest możliwa do uruchomienia w ramach zapytania HTTP, co umożliwia zbudowanie swoistej aplikacji
    backendowej uzywając AWS Lambda, w powyższym przykładzie zrealizowano prosty mikroserwis udostępniający api jako JSON-RPC,
    dostępne są dwie metody, **insert_item** i **list_items**. Jako persystencja została użyta baza DynamoDB.
    
    Dane zwrócone z funkcji lambda stają się danymi zwracanymi jako body zapytania http.
    

## Podsumowanie

Usługa Amazon Lambda wydaje się bardzo ciekawą usługą Amazona służącą do reagowania na najróżniejsze wydarzenia. W odczuciu 
autora możę być całkiem dobrym narzędziem do bardzo łatwego łączenia działania usług Amazona odległych od siebie (np S3 i DynamoDB).

Może być również użyte do budowy prostych mikroserwisów, jednakże ze względu na ograniczone mozliwości współdzielenia kodu
nie będzie najwygodniejszym sposobem rozwijania zaawansowanej logiki aplikacji.