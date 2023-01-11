#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>

const char* ssid     = "ESP32-AP";
const uint16_t portNumber = 50000; // System Ports 0-1023, User Ports 1024-49151, dynamic and/or Private Ports 49152-65535

WiFiServer server(portNumber);
WiFiClient client;
bool connected = false;

int left = 0;
int right = 0;

void Left_Motor_Forward()
{
  digitalWrite(0, HIGH);
  digitalWrite(4, LOW);
}

void Left_Motor_Backward()
{
  digitalWrite(0, LOW);
  digitalWrite(4, HIGH);
}

void Left_Motor_Stop()
{
  digitalWrite(0, LOW);
  digitalWrite(4, LOW);
}

void Right_Motor_Forward()
{
  digitalWrite(16, HIGH);
  digitalWrite(17, LOW);
}

void Right_Motor_Backward()
{
  digitalWrite(16, LOW);
  digitalWrite(17, HIGH);
}

void Right_Motor_Stop()
{
  digitalWrite(16, LOW);
  digitalWrite(17, LOW);
}



void setup()
{
    Serial.begin(9600);

    
    pinMode(0, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(16, OUTPUT);
    pinMode(17, OUTPUT);

    digitalWrite(0, LOW);
    digitalWrite(4, LOW);

    digitalWrite(16, LOW);
    digitalWrite(17, LOW);

    delay(10);

    Serial.begin(115200); Serial.println();
    Serial.print("Setting AP (Access Point)…");
    WiFi.softAP(ssid);
    
    IPAddress IP = WiFi.softAPIP();
    Serial.print(" -> IP address: "); Serial.println(IP);
    server.begin();

}

void loop() {

  if (!connected) {
    // listen for incoming clients
    client = server.available();
    if (client) {
      Serial.println("Client geldi");
      if (client.connected()) {
        Serial.println("ve baglandi!");
        connected = true;
      } else {
        Serial.println("ama baglanamadi :(");
        client.stop();  // close the connection:
      }
    }
  } else {
    if (client.connected()) {
      while (client.available()) 
      {
        char rxData = client.read();

        if (rxData == (char)'M')
        {
          Left_Motor_Stop();
          Right_Motor_Stop();
        }
        else if (rxData == (char)'B')
        {
          Left_Motor_Backward();
          Right_Motor_Backward();
        }
        else if (rxData == (char)'T')
        {
          Left_Motor_Forward();
          Right_Motor_Forward();
        }
        else if (rxData == (char)'L')
        {
          Left_Motor_Backward();
          Right_Motor_Forward();
          delay(20);
          Left_Motor_Stop();
          Right_Motor_Stop();
        }
        else if (rxData == (char)'R')
        {
          Right_Motor_Backward();
          Left_Motor_Forward();
          delay(20);
          Left_Motor_Stop();
          Right_Motor_Stop();
        }
        
        Serial.write(client.read());
      }
      
      while (Serial.available()) {
        char r = Serial.read();
        Serial.write(r);
        client.write(r);
      }
    } else {
      Serial.println("client kacip gitti :(");
      client.stop();
      connected = false;
    }
  }
}
