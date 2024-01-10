# INTEGRAZIOEN CON HA

## Streaming MJPEG 
1. Configura il Server Flask sul Raspberry Pi:
Assicurati che il server Flask con lo streaming della telecamera sia in esecuzione sul Raspberry Pi. Puoi utilizzare il codice fornito precedentemente.

2. Configura Home Assistant:
Aggiungi il seguente codice al tuo file di configurazione di Home Assistant (configuration.yaml). Sostituisci <RASPBERRY_PI_IP> con l'indirizzo IP effettivo del tuo Raspberry Pi.
```yml
camera:
  - platform: mjpeg
    mjpeg_url: http://<RASPBERRY_PI_IP>:5000/video_feed
    name: Raspberry Pi Camera
```
Questo configura una telecamera MJPEG in Home Assistant che utilizza lo streaming fornito dal server Flask sul Raspberry Pi.

4. Riavvia Home Assistant:
Dopo aver aggiunto la configurazione, riavvia Home Assistant per applicare le modifiche.

5. Visualizza la Telecamera:
Ora dovresti essere in grado di visualizzare la telecamera Raspberry Pi all'interno dell'interfaccia di Home Assistant.
## Aggiunta pulsante di salvataggio dell'immagine in HA
Aggiungi il pulsante di salvataggio dell'immagine in Home Assistant. Puoi farlo creando un'automazione che invoca il servizio "camera.snapshot" quando il pulsante viene premuto. Aggiungi quanto segue nel tuo file di configurazione di Home Assistant (configuration.yaml), sostituendo raspberry_pi_ip con l'indirizzo IP effettivo del tuo Raspberry Pi:
```yml
automation:
  - alias: Cattura e Salva Immagine
    trigger:
      platform: state
      entity_id: input_boolean.capture_image_button
      to: 'on'
    action:
      service: camera.snapshot
      data:
        entity_id: camera.raspberry_pi_camera
        filename: '/config/www/captured_image.jpg'  # Regola il percorso in base alle tue esigenze
  - alias: Resetta Pulsante Cattura Immagine
    trigger:
      platform: state
      entity_id: input_boolean.capture_image_button
      to: 'on'
      for:
        seconds: 1
    action:
      service: input_boolean.turn_off
      entity_id: input_boolean.capture_image_button
```
In questo esempio, ho anche aggiunto un'entità di input boolean (input_boolean.capture_image_button) per rappresentare lo stato del pulsante di cattura.
