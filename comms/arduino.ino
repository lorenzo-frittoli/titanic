#define SENSOR_PIN A0
#define TRIGGER_PIN 2 // MUST be 2 or 3 (for attaching the interrupt)
#define CONTROL_PIN 3
#define MOTOR_A 6
#define MOTOR_B 7
#define MOTOR_ENABLE 5
#define P 1.0
#define I 0.01
#define D 0.01
#define NEUTRAL_POS 10000
#define MAX_POS 19000
#define MOTOR_P 1        // in x/256 of the motor power per step
#define PRESSURE_FORCE 0.1  // in x/256 of the motor power per cm
#define MAX_DEPTH_CM 500


int last_update_time_ms;
int target_depth_cm = -10;
int motor_pos = 0;  // proportional to the water volume
// PID
int last_depth_cm;
int depth_integral = 0;

int get_depth_cm() {
  // TODO analogRead(SENSOR_PIN);
  return 0;
}

// power from -255 to 255
void set_motor_power(int power) {
  /*if (power > 0) {
    digitalWrite(MOTOR_A, 0);
    digitalWrite(MOTOR_B, 1);
  } else {
    digitalWrite(MOTOR_A, 1);
    digitalWrite(MOTOR_B, 0);
  }*/

  analogWrite(MOTOR_ENABLE, min(255, abs(power)));
}

void update_pos() {
  if (digitalRead(CONTROL_PIN)) motor_pos++;
  else motor_pos--;
}

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(10); // timeout in ms. Must be low because the motor must be always monitored
  pinMode(SENSOR_PIN, INPUT);
  pinMode(TRIGGER_PIN, INPUT);
  pinMode(CONTROL_PIN, INPUT);
  pinMode(MOTOR_A, OUTPUT);
  pinMode(MOTOR_B, OUTPUT);
  pinMode(MOTOR_ENABLE, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  set_motor_power(0);
  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN), update_pos, CHANGE);
  last_update_time_ms = millis();
  last_depth_cm = get_depth_cm();
}

void loop() {
  if (Serial.available() > 1) {
    target_depth_cm = Serial.parseInt();
    if (target_depth_cm < -10 || target_depth_cm > MAX_DEPTH_CM) target_depth_cm = -10;
    last_update_time_ms = millis();
  } else if (millis() - last_update_time_ms > 1000) {
    target_depth_cm = -10;
  }
  int depth_cm = get_depth_cm();

  depth_integral += target_depth_cm - depth_cm;
  int target_pos = P*(target_depth_cm - depth_cm) + I*depth_integral - D*(depth_cm - last_depth_cm) + NEUTRAL_POS;
  if (target_pos < 0) target_pos = 0;
  else if (target_pos > MAX_POS) target_pos = MAX_POS;

  //set_motor_power(MOTOR_P*(target_pos - motor_pos) + PRESSURE_FORCE*depth_cm);
  set_motor_power(target_depth_cm);
  last_depth_cm = depth_cm;
}
