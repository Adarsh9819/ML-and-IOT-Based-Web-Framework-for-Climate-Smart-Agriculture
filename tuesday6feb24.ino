#include <WiFi.h>
#include <Adafruit_Sensor.h>

#include <DHT.h>

#include<ThingSpeak.h>
#include <HTTPClient.h>
#define USE_SERIAL Serial
// String apiKeyValue = "tPmAT5Ab3j7F9";

char* ssid = "STAFF-403"; //enter SSID

char* password = "1203aigb82"; // enter the password

// WiFiServer server(80);


// WiFiClient client;

// unsigned long myChannelNumber = 1;

// const char * myWriteAPIKey = "R8OX03OOF3C7EA48";

unsigned long lastTime = 0;

unsigned long timerDelay = 10000;

#define DHTPIN 15 // Digital pin connected to the DHT sensor

#define DHTTYPE DHT11 // DHT 11
float h, t;

DHT dht(DHTPIN, DHTTYPE);

void setup()
{

Serial.begin(115200); //Initialize serial

Serial.print("Connecting to ");

Serial.println(ssid);

WiFi.begin(ssid, password);

while (WiFi.status() != WL_CONNECTED) {

delay(500);

Serial.print(".");

}

// Print local IP address and start web server

Serial.println("");

Serial.println("WiFi connected.");

Serial.println("IP address: ");

Serial.println(WiFi.localIP());

// server.begin();

//----nitialize dht11

dht.begin();

// ThingSpeak.begin(client); // Initialize ThingSpeak

pinMode(DHTPIN,INPUT);

}

void loop()

{
// float h, t;
if ((millis() - lastTime) > timerDelay)

{

delay(2500);

// Reading temperature or humidity takes about 250 milliseconds!

h = dht.readHumidity();

// Read temperature as Celsius (the default)

t = dht.readTemperature();

float f = dht.readTemperature(true);

if (isnan(h) || isnan(t) || isnan(f)) {

Serial.println(F("Failed to read from DHT sensor!"));

return;

}
else{
Serial.print("Temperature (ºC): ");

Serial.print(t);

Serial.println("ºC");

Serial.print("Humidity");

Serial.println(h);

ThingSpeak.setField(1, t);
ThingSpeak.setField(2, h);


// int x = ThingSpeak.writeFields(myChannelNumber,myWriteAPIKey);

// if(x == 200){

// Serial.println("Channel update successful.");

// }

// else{

// Serial.println("Problem updating channel. HTTP error code " + String(x));

// }

lastTime = millis();

}

}
if (WiFi.status() == WL_CONNECTED){
        HTTPClient http;

        USE_SERIAL.print("[HTTP] begin...\n");
        // configure traged server and url
        //http.begin("https://www.howsmyssl.com/a/check", ca); //HTTPS
        //http.begin("http://192.168.9.72/sem8/post-esp-data.php"); //HTTP
        http.begin("http://192.168.9.72/sem8/post.php");
          
        USE_SERIAL.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        // String httpRequestData = "api_key=tPmAT5Ab3j7F9&temperature=23&humidity=89&moisture=89";
        String httpRequestData = "temperature=" + String(t) + "&humidity=" + String(h);

        int httpCode = http.POST(httpRequestData);

        // httpCode will be negative on error
        if(httpCode > 0) {
            // HTTP header has been send and Server response header has been handled
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

            // file found at server
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                USE_SERIAL.println(payload);
            }
        } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
}
delay(7000);
}
