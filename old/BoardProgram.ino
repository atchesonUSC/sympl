#define block0 A7
#define block1 A13
#define block2 A14
#define block3 A15
#define button 23
#define collectDataFlag 2000

int runPythonScript = 3000;
int buttonFlag;

void printToSerial(int x, int y);

void setup() {
  pinMode(block0, INPUT);
  pinMode(block1, INPUT);
  pinMode(block2, INPUT);
  pinMode(block3, INPUT);
  pinMode(button, INPUT);
  Serial.begin(9600); // Data transfer rate - 9600 bits/sec
}

void loop() {
  // Gets status of switch
  buttonFlag = digitalRead(button);
  if (buttonFlag == HIGH) { // Checks if switch was pressed
    Serial.println(runPythonScript);
    delay(500);
  }
  Serial.println(collectDataFlag);
  printToSerial(block0);
  printToSerial(block1);
  printToSerial(block2);
  printToSerial(block3);
}

// Reads voltage from block, prints to serial
void printToSerial(int block) {
  int blockData = analogRead(block); // Read from analog pin
  Serial.println(blockData); // Print to serial
}
