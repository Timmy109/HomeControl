#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// Replace with your network credentials
const char* ssid = "Linksys05179";
const char* password = "Regmond.2022$";

// Replace with your server's IP address and port
const char* serverUrl = "http://192.168.1.122:5000/update";

#define DHTPIN 4      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  dht.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
    
    int httpResponseCode = http.POST(payload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.println("Error in HTTP request");
    }
    http.end();
  }
  delay(5000); // Wait for 5 seconds before sending the next reading
}
