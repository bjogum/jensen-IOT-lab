# Jensen IoT-Labb

## Beskrivning
- **Allmänt**
  - ...
- **Förutsättningar**
  - ...

## Hur applikationen används
- **Bygg**
  - ...
- **Starta**
  - ...
- **Kör tester**
  - ...
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