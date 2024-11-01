// Pin locations
const int latchPin = 10;
const int clockPin = 11;
const int dataPin = 12;
int modeDisp = 1;
// Debounce for buttons
#define modeButtonPin 9
byte lastButtonState;

// Variables 
int modeSelector = 0;
int modeButtonState = 0;
int datArray[3] = {B01100000, B11011010, B11110010};

void setup() {
  // Setup code to run once
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  
  // Debounce
  pinMode(modeButtonPin, INPUT);
  lastButtonState = digitalRead(modeButtonPin);
  Serial.begin(9600);
}

void loop() {
    modeButtonState = digitalRead(modeButtonPin);

    if (modeButtonState != lastButtonState) {
        lastButtonState = modeButtonState;
        
        // Increment modeDisp when the button is released
        if (modeButtonState == LOW) {
            modeDisp++;

            // Reset modeDisp to 1 if it exceeds 3
            if (modeDisp > 3) {
                modeDisp = 1;
            }
            
            Serial.println(modeDisp);

            // Use modeDisp to control the shift register output
            if (modeDisp == 1) {
                digitalWrite(latchPin, LOW);
                shiftOut(dataPin, clockPin, LSBFIRST, datArray[0]);
                digitalWrite(latchPin, HIGH);
            } else if (modeDisp == 2) {
                digitalWrite(latchPin, LOW);
                shiftOut(dataPin, clockPin, LSBFIRST, datArray[1]);
                digitalWrite(latchPin, HIGH);
            } else if (modeDisp == 3) {
                digitalWrite(latchPin, LOW);
                shiftOut(dataPin, clockPin, LSBFIRST, datArray[2]);
                digitalWrite(latchPin, HIGH);
            }
        }
    }
}


  // Check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  // if (modeButtonState == HIGH) {
  //   modeSelector++;
  //   delay(500);
  //   Serial.println(modeSelector);
  //   if (modeSelector < 3){
  //     modeSelector = 0;
  //   } else if (0 <= modeSelector <= 3){
  //     digitalWrite(latchPin, LOW);
  //     shiftOut(dataPin, clockPin, LSBFIRST, datArray[modeSelector]);
  //     digitalWrite(latchPin, HIGH);
  //     delay(500);
  //   }

  // }
  
  // Test for only shift, number 1 through 3
  // for (int num = 0; num < 3; num++) {
    // digitalWrite(latchPin, LOW);
    // shiftOut(dataPin, clockPin, LSBFIRST, datArray[num]);
    // digitalWrite(latchPin, HIGH);
  //   delay(500);
  // }
//}