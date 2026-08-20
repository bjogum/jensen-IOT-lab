# Reflektionsdokument – obligatorisk leverabel

Svara kort men motiverat på samtliga frågor. Knyt svaren till vad du implementerade och observerade i laborationen; enstaka ja/nej-svar är inte tillräckliga. Ersätt instruktionstexten med dina svar före inlämning.

1. **Varför ska sensorerna kommunicera med ett API i stället för direkt med PostgreSQL?**
   - APIt fungerar som ett mellanlager mellan sensorerna och databasen. Det tar emot och validerar datan, så att endast giltig data lagras och att formatet är korrekt. Detta gör också databasen säkrare, eftersom all databashantering måste gå via APIt.

2. **Varför ska felaktig sensordata stoppas innan den sparas?**
   -  Man vill bara lagra relevant data som ger värde. Dessutom är det fördelaktigt att hålla databasen strukturerad, tydlig och ren. 

3. **Varför passar PostgreSQL för historiska mätvärden?**
   - Den lagrar data permanent och kan hantera stora mängder data. SQL gör det också effektivt och smidigt att söka och analysera historiska mätvärden, utifrån specifik data som sensor-ID eller datumstämpel etc.

4. **Vad händer med lösningen om Redis försvinner?**
   - Svaren blir lite långsammare då cache saknas. Alla frågor går då direkt mot databasen vilket innebär att den får databasen får jobba hårdare.

5. **Vad händer med lösningen om PostgreSQL försvinner?**
   - Om PostgresSQL försvinner kommer systemet i helhet inte fungera längre. Samtliga nya mätvärden kommer inte lagras och all historik blir oåtkomlig. De enda som kan läsas är cache.

6. **Varför används Docker Compose lokalt?**
   - För att kunna köra hela applikationen lokalt med alla tjänster och beroenden i en gemensam miljö.

7. **Vad automatiserar din CI-pipeline?**
   - CI-pipelinen automatiserar allt jag definierat i .github/workflows/ci.yml - vilket är:
     - Vid push eller pull-request triggas pipelinen
       1. Hämtar koden (via actions/checkout@v4)
       2. Installerar Python 3.12
       3. Installerar alla beroenden från 'requirements.txt' 
       4. Kör alla tester med Pytest (i api-mappen)
       5. Bygger Docker-image

8. **Vad observerade du när du tog bort en Kubernetes Pod?**
   - En ny pod skapades omedelbart för att ersätta den förlorade Pod:en, vilket är syftet med self-healing.

9.  **Varför kan flera repliker ge högre tillgänglighet?**
   - Om en Pod kraschar kan de andra replikerna fortsätta hantera trafik, vilket ger högre tillgänglighet.

10. **När hade Kubernetes varit overkill för en lösning?**
   - Kubernetes hade varit överflödigt för en liten lösning med få tjänster, där Docker Compose räcker.

Spara svaren i denna fil. Arkitekturdiagrammet lämnas separat enligt `docs/architecture.md`.
