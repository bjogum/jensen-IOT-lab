# Jensen IoT-Labb

## Beskrivning
**Allmänt**

Projektet är en enkel IoT-plattform där tre simulerade sensorer skickar temperatur, luftfuktighet och batterinivå till ett REST API. API:t bygger på en Flask-applikation som validerar datan och lagrar mätningarna i PostgreSQL. Redis används som cache för den senaste mätningen.

API:t körs med Docker Compose tillsammans med PostgreSQL, Redis och simulatorn. Utöver det finns även en CI-pipeline med GitHub-Actions, som kör tester och bygger Docker-image.

Kubernetes används för containerorkestrering. API:t körs med tre Poddar (repliker) och en Service som fördelar trafiken mellan dem.

**Förutsättningar**

För att köra projektet behövs:
- Docker och Docker Compose
- Python 3.12
- Git
- Minikube och kubectl

## Hur applikationen används
**Klona repot**
```bash
git clone https://github.com/bjogum/jensen-IOT-lab.git
```

**Starta applikationen**
```bash
docker compose up --build -d
```

**Kontrollera status**
```bash
docker compose ps
```
Följande tjänster ska nu köras:
 - jensen-iot-redis 
 - jensen-iot-db
 - jensen-iot-api
 - jensen-iot-simulator

**Kontrollera simulator-loggen**

För live övervakning (avsluta med `ctrl+c`):
```bash
docker compose logs -f api simulator
```
För senaste 50 loggarna:
```bash
docker compose logs --tail=50 api simulator
```

## API-dashboard
För att visa `API dashboarden` - öppna adressen nedan i din webbläsare:
```bash
http://localhost:5001/
```

**Implementerade endpoints**

Dessa endpoints går att använda för att hämta specifik data från API:t
- `/health`
- `/devices`
- `/measurements`
- `/statistics`
- `/devices/<device-ID>/latest` (ersätt `<device-ID>` med specifik sensor)

**Kontrollera cache**

Redis lagrar cache för de senaste mätvärdet för respektive sensor. Kontrollera vilka sensorer som finns lagrade i cache:

```bash
docker compose exec redis redis-cli KEYS "latest:*"
```
Töm Redis helt och prova gör en ny kontroll
```bash
docker compose exec redis redis-cli FLUSHDB
```



## Kör tester

Projektets tester körs med pytest och kontrollerar valideringen av inkommande sensordata. För att köra testerna använd:
```bash
docker compose exec api python -m pytest -q
```
Resultatet ska bli '7 passed' - vilket betyder att samtliga tester har genomförts med lyckat resultat.


## CI-pipeline
CI-piplinen är definierad med samtliga instruktioner i "ci.yml". Vid push eller pull-request triggas GitHub-actions. Alla beroenden installeras, tester körs och docker-image skapas. Grön markering visar att körningene gått igenom med lyckat resultat.  

Flödet mer i detalj: 
- Vid push eller pull-request triggas pipelinen
- Hämtar koden (via actions/checkout@v4)
- Installerar Python 3.12
- Installerar alla beroenden från 'requirements.txt'
- Kör alla tester med Pytest (i api-mappen)
- Bygger Docker-image

## Kubernetes
Kubernetes-delen körs med Minikube. API:t distribueras med tre Pod-repliker och en Service. Starta minikube och bygg imagen:
```bash
minikube start --driver=docker
minikube status
minikube image build -t jensen-iot-api:lab ./api
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
```

Vänta tills alla tre poddar är aktiva `READY` & `1/1`. För att sen nå tjänsten använd:
```bash
minikube service jensen-iot-api
```
Webbläsaren bör nu öppnas automatiskt, om inte - hämta aktuell URL här:
```bash
minikube service jensen-iot-api --url
```
Se samtliga Poddar:
```bash
kubectl get pods
```
Radera en valfri pod:
```bash
kubectl delete pod <podnamn>
```
För att verifiera att deplyment ersätter den raderade med en ny (målet är tre aktiva replikor):
```bash
kubectl get pods -w
```
Avsluta minikube med:
```bash
minikube stop
```

## Kända begränsningar
Kubernetes-delen är en introducerande demo där endast API:t distribueras. PostgreSQL, Redis och sensorsimulatorn körs fortfarande med Docker Compose och ingår inte i Kubernetes-deployen.


## Svar från: "Grundläggande SQL-uppgifter"
#### Tre SQL frågor
- SELECT COUNT(*) FROM measurements;
  - Visar antal mätningar (totalt)

- SELECT AVG("temperature") FROM measurements;
  - Visar medeltemperaturen från samtliga mätningar

- SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';
  - Visar alla mätningar som skapats senaste 24h