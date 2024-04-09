# Ensemble des fonctions utilisées par CIDER pour calculer les features

| Différentes fonctions pour créer des features  | Compatible avec le format des données   | Pourquoi ?  |
| :--------------- |:---------------| :-----|
| active_days  |  Compatible   |   |
| number_of_contacts | Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
|call_duration |     Compatible    |   |
| percent_nocturnal |     Compatible    |   |
| percent_initiated_conversations |  Compatible  |   |
| percent_initiated_interactions |  Compatible  |   |
| response_delay_text |  Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| response_rate_text | Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| entropy_of_contacts | Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| balance_of_contacts | Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| interactions_per_contact | Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| interevent_time | Compatible        |   |
| percent_pareto_interactions |  Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| percent_pareto_durations |  Non compatible | recipient_id n'est pas disponible dans les données CDR (voix/sms) |
| number_of_interactions | Compatible        |   |
| number_of_antennas |  Compatible       |   |
| entropy_of_antennas | Compatible        |   | 
| radius_of_gyration | Compatible        |   |
| frequent_antennas | Compatible        |   |
| percent_at_home | Compatible  |   | 
 

