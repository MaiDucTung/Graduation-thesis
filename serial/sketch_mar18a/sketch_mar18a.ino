void setup() {
 Serial.begin(115200);
 while(!Serial) {}
}

void loop() {
  Serial.println("Hello from Bao");
  delay(1000);
  

}
