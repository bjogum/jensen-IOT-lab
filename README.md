# Jensen IoT-Labb

## Beskrivning
**Allmänt**

Projektet är en enkel IoT-plattform där tre simulerade sensorer skickar temperatur, luftfuktighet och batterinivå till ett REST API. API:t validerar datan och lagrar mätningarna i PostgreSQL. Redis används som cache för den senaste mätningen och senaste förfrågan.

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


**Kör tester**
```bash
docker compose exec api python -m pytest -q
```
Resultatet ska bli '7 passed' - vilket betyder att samtliga tester har genomförts med lyckat resultat.


## CI-pipeline
CI-piplinen är definierad med samtliga instruktioner i "ci.yml". Vid push eller pull-request triggas GitHub-actions. Alla beroenden installeras, tester körs och docker-image skapas. Grön markering visar att körningene gått igenom med lyckat resultat.  


## Kubernetes
Kubernetes-delen körs med Minikube. API:t distribueras med tre Pod-repliker och en Service.

...
...

```bash
kubectl get pods
```
...

## Kända begränsningar
Kubernetes-delen är en introducerande demo där endast API:t distribueras. PostgreSQL, Redis och sensorsimulatorn körs fortfarande med Docker Compose och ingår inte i Kubernetes-deployen.


## Begränsningar
...
...


## Svar från: "Grundläggande SQL-uppgifter"
#### Tre SQL frågor
- SELECT COUNT(*) FROM measurements;
  - Visar antal mätningar (totalt)

- SELECT AVG("temperature") FROM measurements;
  - Visar medeltemperaturen från samtliga mätningar

- SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';
  - Visar alla mätningar som skapats senaste 24h