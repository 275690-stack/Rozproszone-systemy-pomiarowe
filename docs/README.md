# Rozproszony system pomiarowy
## 1. Informacje ogólne
Rozproszony system pomiarowy służy do pomiaru temperatury w czasie rzeczywistym, wizualizacji i zapisu uzyskanych wyników. 
## 2. Setup
Wymagane oprogramowanie:
* WSL2
* 
*
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


