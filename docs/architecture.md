# Arkitekturdiagram

## API-systemet
Diagrammet visar arkitekturen för APIt som helhet, där klienten kan fråga efter specifik data (GET request) och få svar tillbaka från APIt. Underst i diagrammet visas samtlig sensorer (som via simulatorn) postas och därmed hanteras av API som i sin tur distrubuerar vidare till databas och cache.
![Arkitektur](api.png)

## Kubernetes
När en klient skickar en request hanteras den av Kubernetes service, som fördelar trafiken över de tre Poddana. Deployment ser till att Poddarna körs och att det finns tre repliker. Detta gör att systemet blir mer driftsäkert om någon Pod skulle kracha.
![Kubernetes](kub.png)

## CI-pipeline
Diagrammet visuallierar CI-pipelinen, hur flödet aktiveras och vad som automatiseras. Vid en puch eller pull-request triggas GitHub-actions som i sin tur kör de definierade instruktionerna (enl. ci.yml). När alla tester och byggsteg genomförts med ett lykcat resultat markeras körningen som grön.
![CI-flow](ci.png)