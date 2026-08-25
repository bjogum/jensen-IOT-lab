# Jensen IoT-Labb

## Beskrivning

Projektet är en enkel IoT-plattform där tre simulerade sensorer skickar temperatur, luftfuktighet och batterinivå till ett REST API. API:t bygger på en Flask-applikation som validerar datan och lagrar mätningarna i PostgreSQL. Redis används som cache för den senaste mätningen.

API:t körs med Docker Compose tillsammans med PostgreSQL, Redis och simulatorn. Utöver det finns även en CI-pipeline med GitHub-Actions, som kör tester och bygger Docker-image.

Kubernetes används för containerorkestrering. API:t körs med tre Poddar (repliker) och en Service som fördelar trafiken mellan dem.

[**Länk till projektets arkitektur**](https://github.com/bjogum/jensen-IOT-lab/blob/main/docs/architecture.md)


## Förutsättningar

För att köra projektet behövs:
- Docker och Docker Compose
- Python 3.12
- Git
- Minikube och kubectl

## Hur applikationen används
**Klona repot och starta projektet**
```bash
git clone https://github.com/bjogum/jensen-IOT-lab.git
cd jensen-IOT-lab
docker compose up --build -d
```

**Kontrollera status**
```bash
docker compose ps
```
Följande tjänster ska nu köras:
 - jensen-iot-api
 - jensen-iot-db
 - jensen-iot-redis
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
sensor-003 skickar emellanåt korrupt data (genererade fel med flit), vilket resulterar i status "400". Korrekta värden som accepteras, retunerar status "201". 

## API-dashboard
För att visa `API dashboarden` - öppna adressen nedan i din webbläsare:
```bash
http://localhost:5001/
```

**Implementerade endpoints**

`/health`
```bash
http://localhost:5001/health
```
`/devices`
```bash
http://localhost:5001/devices
```
`/measurements`
```bash
http://localhost:5001/measurements
```
`/statistics` - visar statistik över mätningarna:

- Medelvärde, fukt
- Medelvärde, temperatur
- Sensorn med högst medeltemperatur
- Sensorn med flest mätningar (mest aktiva) 
- Totalt antal sensorer
- Totalt antal mätningar

```bash
http://localhost:5001/statistics
```
`/devices/<device-ID>/latest` (ersätt `<device-ID>` med specifik sensor). Exempelvis:
```bash
http://localhost:5001//devices/sensor-002/latest
```

**Databas och cache**

PostgreSQL används som permanent lagring av sensorer och mätningar. Redis används som cache för den senaste mätningen per sensor. Vid en cache miss hämtas värdet från PostgreSQL och skrivs tillbaka till Redis.


## Kör tester
Projektets tester körs med pytest och kontrollerar valideringen av inkommande sensordata. För att köra testerna använd:
```bash
docker compose exec api python -m pytest -q
```
Resultatet ska bli `7 passed` - vilket betyder att samtliga tester har genomförts med lyckat resultat. Dessa tester kör CI-piplinen automatiskt vid push och pull request.


## CI-pipeline
CI-piplinen är definierad med samtliga instruktioner i `ci.yml`. Vid push eller pull-request triggas GitHub-actions. Alla beroenden installeras, tester körs och docker-image skapas. Grön markering visar att körningen gått igenom med lyckat resultat.  

Flödet mer i detalj: 
- Vid push eller pull-request triggas pipelinen
- Hämtar koden (via actions/checkout@v4)
- Installerar Python 3.12
- Installerar alla beroenden från 'requirements.txt'
- Kör alla tester med Pytest (i api-mappen)
- Bygger Docker-image

## Kubernetes
API:t distribueras lokalt med Minikube. Kubernetes-konfigurationen består av en Deployment och en Service. Starta minikube och bygg imagen:
```bash
minikube start --driver=docker
minikube image build -t jensen-iot-api:lab ./api
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Kontrollera Pods:
```bash
kubectl get pods
```
En lista med tre repliker (Pods) ska nu visas och vara `RUNNING`

Öppna APIt med:
```bash
minikube service jensen-iot-api
```

**Scaling och self-healing**

Deploymenten kör tre repliker. Om en Pod kraschar ersätter Kubernetes den automatiskt, så att det önskade antalet repliker upprätthålls. Antalet repliker kan även ändras genom att uppdatera Deploymentens `replicas`-värde.

Öka antalet repliker till fem stycken:
```bash
kubectl scale deployment jensen-iot-api --replicas=5
```

Kontrollera att antal Pods har ökat från tre till fem:
```bash
kubectl get pods
```

Återställ till tre  repliker genom:
```bash
kubectl scale deployment jensen-iot-api --replicas=3
```
Kontrollera att antal Pods återställts till tre (de överflödiga står som `Terminating` ett tag innan de raderas):
```bash
kubectl get pods
```

## Avsluta projektet

```bash
minikube stop
docker compose down -v
```

## Kända begränsningar
- Sensorerna som skickar data till API:t är simulerade (via `simulator.py`). Inga fysiska sensorer används i projektet.

- Kubernetes-delen är en förenklad lösning där endast API:t distribueras. PostgreSQL, Redis och simulatorn körs fortfarande med Docker Compose och distribueras inte till Kubernetes.


## Övrigt komplettering för labben
#### Grundläggande SQL-uppgifter - tre SQL frågor
Visar antal mätningar (totalt):
```bash
SELECT COUNT(*) FROM measurements;
```

Visar medeltemperaturen från samtliga mätningar
```bash
SELECT AVG("temperature") FROM measurements;
``` 

Visar alla mätningar som skapats senaste 24h
```bash
SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';
```

#### Fördjupande SQL-analyser
I projektet har jag även implementerat två olika SQL-analyser enligt nedan:

-   Vilken sensor som är mest aktiv (flest mätpunkter).
    ```sql
        SELECT device_id, AVG(temperature) AS avg_temperature
        FROM measurements
        GROUP BY device_id
        ORDER BY avg_temperature DESC
        LIMIT 1;
-   Vilken sensor som har den högsta medeltemperaturen.
    ```sql
        SELECT device_id, COUNT(*) AS measurement_count
        FROM measurements
        GROUP BY device_id
        ORDER BY measurement_count DESC
        LIMIT 1;
Båda dessa SQL-analyser grupperar mätningarna per sensor med `GROUP BY device_id` och används i API-endpointen `/statistics`.

#### Reflektioner

[**Länk till reflektioner**](https://github.com/bjogum/jensen-IOT-lab/blob/main/docs/reflection.md)