# Reflektionsdokument – obligatorisk leverabel

Svara kort men motiverat på samtliga frågor. Knyt svaren till vad du implementerade och observerade i laborationen; enstaka ja/nej-svar är inte tillräckliga. Ersätt instruktionstexten med dina svar före inlämning.

1. Varför ska sensorerna kommunicera med ett API i stället för direkt med PostgreSQL?
   - API:t fungerar som ett mellanlager mellan sensorerna och databasen. Det tar emot, validerar och filtrerar data så att endast korrekt formaterad data lagras i databasen. Detta gör också databasen säkrare, eftersom det bara är API:t som får kommunicera med databasen.

2. Varför ska felaktig sensordata stoppas innan den sparas?
   -  Man bara lagra relevant data som ger värde. Dessutom är det fördelaktigt att hålla databasen strukturerad, tydlig och ren. 

3. Varför passar PostgreSQL för historiska mätvärden?
   - Den lagrar data permanent och kan hantera stora mängder data. SQL gör det också effektivt och smidigt att söka efter och analysera historiska mätvärden.

4. Vad händer med lösningen om Redis försvinner?
   - Svaren blir lite långsammare då cache saknas, dessutom får databasen får jobba hårdare.

5. Vad händer med lösningen om PostgreSQL försvinner?
   - Om PostgresSQL försvinner kommer systemet i helhet inte fungera längre. Samtliga nya mätvärden kommer inte lagras och all historik blir oåtkomlig. De enda som kan läsas är cache.

6. Varför används Docker Compose lokalt?
   - För att kunna köra hela applikationen lokalt med alla tjänster och beroenden i en gemensam miljö.

7. Vad automatiserar din CI-pipeline?
   - ...

8. Vad observerade du när du tog bort en Kubernetes Pod?
   - ...

9.  Varför kan flera repliker ge högre tillgänglighet?
   - ...

10. När hade Kubernetes varit overkill för en lösning?
   - ...

Spara svaren i denna fil. Arkitekturdiagrammet lämnas separat enligt `docs/architecture.md`.
