bool state = false;
const unsigned int MAX_INPUT=10;

void setup() {

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);

}

// here to process incoming serial data after a terminator received
void process_data (const char * data, int dataLen)
  {
//    if (dataLen>=2){
//      int intData = atoi(data);
//      int axis = (int) (intData/pow(10, dataLen-1));
//      if (axis >= NUM_AXES) {
//        // invalid
//        return;
//      }
//      if (axis >= NON_SERVOS) {
//        int angle = intData % ((int) ceil(pow(10, dataLen-1)));
//        servos[axis-NON_SERVOS].write(map(constrain(angle, 0, 180), 0, 180, constraints[axis-NON_SERVOS][0], constraints[axis-NON_SERVOS][1]));
//      }
//      else {
//        targetRailPosition = intData % ((int) ceil(pow(10, dataLen-1)));
//      }
//    }
    state= !state;
    
  }  // end of process_data

void processIncomingByte (const byte inByte)
  {
  static char input_line [MAX_INPUT];
  static unsigned int input_pos = 0;

  switch (inByte)
    {

    case '\n':   // end of text
      input_line [input_pos] = 0;  // terminating null byte

      // terminator reached! process input_line here ...
      process_data (input_line, input_pos);

      // reset buffer for next time
      input_pos = 0;  
      break;

    case '\r':   // discard carriage return
      break;

    default:
      // keep adding if not full ... allow for terminating null byte
      if (input_pos < (MAX_INPUT - 1))
        input_line [input_pos++] = inByte;
      break;

    }  // end of switch

  } // end of processIncomingByte  

void loop() {
  // if serial data available, process it
//  while (Serial.available () > 0)
//    processIncomingByte (Serial.read ());
  if (state) {
    digitalWrite(13, HIGH);
  }
  else {
    digitalWrite(13, LOW);
  }
  state = !state;
  Serial.print(map(analogRead(A0), 0, 1023, 0, 43));
  Serial.print(" ");
  Serial.println(map(analogRead(A1), 0, 1023, 30, 120));
  delay(100);
  
 }  // end of loop
