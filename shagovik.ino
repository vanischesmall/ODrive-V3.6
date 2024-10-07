#include <Servo.h>
Servo serv1;
Servo serv2;
Servo serv3;

#define PinM1 3
#define PinM2 5

#define PinS1 2
#define PinS2 4

#define PinBut1 6
#define PinBut2 7

#define PinKonc 8

#define PinMilk A5
#define PinCoffee A4

#define PinServ1 11
#define PinServ2 10
#define PinServ3 9

int but1 = 1;
int but2 = 1;
int konc = 1;

bool flag_reset = 0;
bool flag_conn = false;

auto timerManipulator = millis();
auto timerServ1 = millis();
auto timerServ2 = millis();
auto timerServ3 = millis();
int serv1_ang = 0;
int serv2_ang = 0;
int serv3_ang = 0;
int time_manipulator = 4000;
bool manipulator_flag = false;


int timeCoffee = 4000;
bool flag_drink_end = false;
bool flag_drink_start = false;
auto timerCoffee = millis();

int table_counter = 0;
int max_table_counter = 20;
int table_step = 1000;
int table_BIG_step = 18500;
bool table_flag = false;

int state = 0;
int rasp_state = 0;
int rasp_state_old = rasp_state;
int arduino_state = 0;
auto timerState = millis();
auto timerUart = millis();
auto timerUartOff = millis();

volatile long tick_counter = 0;

void setup() {
  Serial.begin(9600);

  pinMode(PinM1, OUTPUT);  //Настраиваем пины управления
  pinMode(PinM2, OUTPUT);

  pinMode(PinS1, INPUT);  // Конфигурируем вывод Arduino pin_S1 как вход.
  pinMode(PinS2, INPUT);
  int i = digitalPinToInterrupt(PinS1);  // Получаем номер прерывания вывода pin_S1.
  attachInterrupt(i, update_counter, RISING);

  pinMode(PinBut1, INPUT_PULLUP);
  pinMode(PinBut2, INPUT_PULLUP);
  pinMode(PinKonc, INPUT_PULLUP);

  pinMode(PinMilk, OUTPUT);
  pinMode(PinCoffee, OUTPUT);

  serv1.attach(PinServ1);
  serv2.attach(PinServ2);
  serv3.attach(PinServ3);

  if (digitalRead(PinKonc) == 1) {
    while (digitalRead(PinKonc) == 1) {
      Serial.println(digitalRead(PinKonc));
      analogWrite(PinM2, 255);
    }
    analogWrite(PinM2, 0);
  }
  analogWrite(PinM1, 255);
  delay(500);
  analogWrite(PinM1, 0);
  tick_counter = 0;
}

void update_counter() {
  if (digitalRead(PinS2)) {
    tick_counter += 1;
  } else {
    tick_counter -= 1;
  }
}

void motor_rotate(int tick) {
  // 1 оборот - 168 тиков
  int e = tick - tick_counter;
  if (100 > e and e > -100) {
    table_flag = true;
    e = 0;
  } else {
    table_flag = false;
  }
  int u = 255;


  if (e > 0) {
    analogWrite(PinM1, u);
    analogWrite(PinM2, 0);
  } else if (e < 0) {
    analogWrite(PinM1, 0);
    analogWrite(PinM2, u);
  } else {
    analogWrite(PinM1, 0);
    analogWrite(PinM2, 0);
  }
}

void uart() {
  if (flag_conn == false) {
    if (Serial.available() > 0 and Serial.read() == '@') {
      flag_conn = true;
      timerUartOff = millis();
    }
  } else {
    if (timerUart + 100 < millis()) {
      timerUart = millis();
      Serial.print("@" + String(arduino_state))
    }
    if (Serial.available() > 0) {
      String inn = Serial.readStringUntil('$');
      if (inn.length() == 2) {
        timerUartOff = millis();
        rasp_state = inn.substring(0, 1).toInt();
      }
    } else if (timerUartOff + 50000 < millis()) {
      flag_conn = false;
    }
  }
}

void manipulator(int set1, int set2, int set3) {
  if (timerServ1 + 5 < millis()) {
    if (set1 > serv1_ang) {
      serv1_ang++;
    } else if (set1 < serv1_ang) {
      serv1_ang--;
    }
  }
  if (timerServ2 + 5 < millis()) {
    if (set2 > serv2_ang) {
      serv2_ang++;
    } else if (set2 < serv2_ang) {
      serv2_ang--;
    }
  }
  if (timerServ3 + 5 < millis()) {
    if (set3 > serv3_ang) {
      serv3_ang++;
    } else if (set3 < serv3_ang) {
      serv3_ang--;
    }
  }
  if (set1 == serv1_ang and set2 == serv2_ang and set3 == serv3_ang) {
    manipulator_flag = true;
  } else {
    manipulator_flag = false;
  }
  serv1.write(serv1_ang);
  serv2.write(serv2_ang);
  serv3.write(serv3_ang);
}

void drink() {
  if (flag_drink_start == false) {
    flag_drink_start = true;
    flag_drink_end = false;
    timerCoffee = millis();
  }

  else {
    if (timerCoffee + timeCoffee > millis()) {
      digitalWrite(PinCoffee, 1);
    } else {
      digitalWrite(PinCoffee, 0);
      flag_drink_end = true;
    }

    if (flag_drink_end == true) {
      flag_drink_start = false;
    }
  }
}

void loop() {

  but1 = digitalRead(PinBut1);
  but2 = digitalRead(PinBut2);
  konc = digitalRead(PinKonc);

  uart();

  if (rasp_state != rasp_state_old) {
    state = 1;
    flag_reset = false;
  }
  rasp_state_old = rasp_state;

  if (table_counter < max_table_counter) {
    arduino_state = 9 manipulator(37, 180, 180);
  }

  else if (rasp_state == 0) {
    arduino_state = 0;
    manipulator(37, 180, 180);

  } else if (rasp_state == 1) {
    arduino_state = 1;
    if (state == 1) {
      manipulator(37, 0, 180);
      if (manipulator_flag == true) {
        state = 2;
      }
    } else if (state == 2) {
      manipulator(150, 0, 90);
      if (manipulator_flag == true) {
        state = 3;
      }
    } else if (state == 3) {
      motor_rotate(table_counter * table_step + table_BIG_step);
      if (table_flag == true) {
        state = 4;
      }
    } else if (state == 4) {
      manipulator(150, 0, 180);
      if (manipulator_flag == true) {
        state = 5;
      }
    } else if (state == 5) {
      motor_rotate(table_counter * table_step);
      if (table_flag == true) {
        state = 6;
        table_counter = table_counter + 1;
      }
    } else if (state == 6) {
      manipulator(90, 0, 180);
      if (manipulator_flag == true) {
        state = 7;
      }
    } else if (state == 7) {
      manipulator(90, 180, 180);
      if (manipulator_flag == true) {
        state = 8;
      }
    } else if (state == 8) {
      drink();
      if (flag_drink_end == true) {
        state = 0;
        flag_drink_end = false;
      }
    } else if (state == 0) {
      manipulator(37, 180, 180);
    }

  } else if (rasp_state == 4) {
    if (flag_reset == false) {
      if (digitalRead(PinKonc) == 1) {
        while (digitalRead(PinKonc) == 1) {
          Serial.println(digitalRead(PinKonc));
          analogWrite(PinM2, 255);
        }
        analogWrite(PinM2, 0);
      }
      analogWrite(PinM1, 255);
      delay(500);
      analogWrite(PinM1, 0);
      while (Serial.available > 0) {
        Serial.read();
      }
      tick_counter = 0;
      table_counter = 0;
      flag_reset = true;
    }
  }
}
