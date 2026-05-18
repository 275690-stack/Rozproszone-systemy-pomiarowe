# Rozproszony system pomiarowy
## 1. Informacje ogólne
Rozproszony system pomiarowy służy do pomiaru temperatury w czasie rzeczywistym, wizualizacji i zapisu uzyskanych wyników. 
## 2. Setup
Wymagane oprogramowanie:
* WSL2
* Docker
* Docker Compose
* Visual Studio Code z rozszerzeniem PlatformIO

Aby sklonować to repozytorium należy zastosować komendę
```bash
git clone https://github.com/275690-stack/Rozproszone-systemy-pomiarowe.git
cd Rozproszone-systemy-pomiarowe
```
Przed uruchomieniem kodu należy upewnić się, że środowisko Docker Compose jest uruchomione za pomocą komendy:
```bash
docker compose up --build
```
Po uruchomieniu Docker Compose powinny być dostępne usługi:
* REST API (Flask), czyli warstwa dostępu do danych pomiarowych - http://localhost:5001
* Broker MQTT, czyli centralny punkt komunikacji - localhost:1883
* PostgreSQL, czyli baza danych przechowująca pomiary, indeksy czasowe i dane urządzeń - localhost:5432
* Ingestor, czyli serwis zbierający dane z MQTT i obsługujący błędy
## 3. Zarządzanie

### Topiciem używanym w projekcie będzie:

lab/g01/esp32-%04X%08X/pomiar

### Każdy z pomiarów będzie mieć ten sam topic.

### Komunikaty statusowe będą oddzielone od komunikatów pomiarowych.

### Identyfikator urządzenia będzie wyglądać w sposób następujący:
"device_id": "esp32-ab12cd34",


"schema_version": 1,
"group_id": "g01",

"sensor": "temperature",
"value": 24.5,
"unit": "C",
"ts_ms": 1742030400000,
"seq": 15


