# Jensen IoT-Labb

## Beskrivning
- **Allmänt**
Projektet är en enkel IoT-plattform där tre simulerade sensorer skickar temperatur, luftfuktighet och batterinivå till ett REST API. API:t validerar datan och lagrar mätningarna i PostgreSQL. Redis används som cache för den senaste mätningen och senaste förfrågan.

API:t körs med Docker Compose tillsammans med PostgreSQL, Redis och simulatorn. Utöver det finns även en CI-pipeline med GitHub-Actions, som kör tester och bygger Docker-image.

Kubernetes används till containerorkestrering. API:t körs med tre Poddar (repliker) och en Service som fördelar trafiken mellan dem.

- **Förutsättningar**
För att köra projektet behövs:
- Docker och Docker Compose
- Python 3.12
- Git
- Minikube och kubectl

## Hur applikationen används
- **Klona repot**
- git clone https://github.com/bjogum/jensen-IOT-lab.git

- **Starta**
  - docker compose up --build -d

- **Kör tester**
  - docker compose exec api python -m pytest -q

- **Begränsningar**
  - ...



## Svar från: "Grundläggande SQL-uppgifter"
#### Tre SQL frågor
- SELECT COUNT(*) FROM measurements;
  - Visar antal mätningar (totalt)

- SELECT AVG("temperature") FROM measurements;
  - Visar medeltemperaturen från samtliga mätningar

- SELECT * FROM measurements WHERE created_at >= NOW() - INTERVAL '24 hours';
  - Visar alla mätningar som skapats senaste 24h