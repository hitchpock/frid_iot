#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

#define PN532_IRQ   9

Adafruit_PN532 nfc(PN532_IRQ, 100);

//######################################################

bool diff(uint8_t*, uint8_t*);
uint8_t* create(uint8_t*, uint8_t*);

uint8_t olduid[8];

void setup(void)
{
  Serial.begin(9600);
  Serial1.begin(115200);
  nfc.begin();
  int versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.print("Didn't find RFID/NFC reader");
    while(1) {
    }
  }
 
  Serial.println("Found RFID/NFC reader");
  nfc.SAMConfig();
  Serial.println("Waiting for a card ...");
}
 
void loop(void)
{
  uint8_t success;
  uint8_t uid[8];
  uint8_t uidLength;
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
  if (success) {
//    Serial.println("Found a card");
//    Serial.print("ID Length: ");
//    Serial.print(uidLength, DEC);
//    Serial.println(" bytes");
//    Serial.print("ID Value: ");
    //nfc.PrintHex(uid, uidLength);
    if (diff(uid, olduid) == false) {
      for (int index = 0; index < 7; index++) {
        olduid[index] = uid[index];
      }
      Serial.println("Found a card");
      Serial.print("ID Length: ");
      Serial.print(uidLength, DEC);
      Serial.println(" bytes");
      Serial.print("ID Value: ");
      nfc.PrintHex(uid, uidLength);
      Serial.println("OK");
      Serial1.write(uid, uidLength);
      Serial.println("");
    }
  }
}

bool diff(uint8_t *arr1, uint8_t *arr2) {
  for (int index = 0; index < 7; index++) {
    if (arr1[index] != arr2[index]) {
      return false;
    }
  }
  return true;
}

uint8_t* create(uint8_t *arr1, uint8_t *arr2) {
  for (int index = 0; index < 7; index++) {
    arr2[index] = arr1[index];
  }
  return arr2;
}
