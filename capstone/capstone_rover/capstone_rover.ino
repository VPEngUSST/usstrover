// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the rover unit

//#define DEBUG

// dependencies
#include <Servo.h>

// pin connections
#define SLIDER_PWM 6
#define TABLE_A 8
#define TABLE_B 9
#define TABLE_PWM 5
#define PAN_SERVO_PIN 14
#define TILT_SERVO_PIN 10

// don't change these because interrupts would break
#define SLIDER_A 7
#define SLIDER_B 4
#define LEFT_LIMIT 2
#define RIGHT_LIMIT 3

// configuration
#define PAN_SERVO_MIN 1000
#define PAN_SERVO_MAX 2000
#define TILT_SERVO_MIN 1000
#define TILT_SERVO_MAX 2000

// function prototypes
void setSlider(int rate);
void setTable(int rate);
void limitInterrupt();

// command message struct
typedef struct
{
	char sliderRate;
	char tableRate;
	byte panPosition;
	byte tiltPosition;
	byte csum;
} command_t;

// union for handling messages bytewise
typedef union
{
	command_t cmd_struct;
	byte cmd_bytes[sizeof(command_t)];
} command_t_union;

// command message header and key (header checker)
const byte header[2] = {'m', 's'};
byte key[2] = {0, 0};

// globals
Servo panServo;
Servo tiltServo;
volatile enum {STOPPED, LEFT, RIGHT} sliderDirection;

// this is run at power-up
void setup()
{
	// configure I/O
	pinMode(SLIDER_A, OUTPUT);
	pinMode(SLIDER_B, OUTPUT);
	pinMode(SLIDER_PWM, OUTPUT);
	pinMode(LEFT_LIMIT, INPUT_PULLUP);
	pinMode(RIGHT_LIMIT, INPUT_PULLUP);
	pinMode(TABLE_A, OUTPUT);
	pinMode(TABLE_B, OUTPUT);
	pinMode(TABLE_PWM, OUTPUT);
	panServo.attach(PAN_SERVO_PIN, PAN_SERVO_MIN, PAN_SERVO_MAX);
	tiltServo.attach(TILT_SERVO_PIN, TILT_SERVO_MIN, TILT_SERVO_MAX);
	
	// initialize output states
	digitalWrite(SLIDER_A, LOW);
	digitalWrite(SLIDER_B, LOW);
	digitalWrite(SLIDER_PWM, LOW);
	sliderDirection = STOPPED;
	digitalWrite(TABLE_A, LOW);
	digitalWrite(TABLE_B, LOW);
	digitalWrite(TABLE_PWM, LOW);
	panServo.write(90);
	tiltServo.write(90);
	
	// set up serial port for XBEE connection
	Serial1.begin(9600);
	Serial1.flush();
	
	// set up interrupts on limit switches
	attachInterrupt(0, limitInterrupt, FALLING);
	attachInterrupt(1, limitInterrupt, FALLING);
	
	#ifdef DEBUG
	{
		Serial.begin(9600);
		Serial.println("Hello world!");
	}
	#endif
}

// runs forever
void loop()
{
	static command_t_union msg;
	byte i, tmp;
	
	// check serial port for new message data
	if(Serial1.available())
	{
		// shift the next byte
		key[0] = key[1];
		key[1] = (byte)Serial1.read();
		
		// check for a complete header
		if((header[0] == key[0]) && (header[1] == key[1]))
		{
			#ifdef DEBUG
				Serial.print("got header");
			#endif
			// read in message data
			for(i = 0; i < sizeof(msg); i++)
			{
				while(!Serial1.available());
				msg.cmd_bytes[i] = Serial1.read();
			}
			
			// check for a valid checksum
			tmp = (byte)msg.cmd_struct.sliderRate;
			tmp += (byte)msg.cmd_struct.tableRate;
			tmp += (byte)msg.cmd_struct.panPosition;
			tmp += (byte)msg.cmd_struct.tiltPosition;
			
			// execute the commands in the message
			if(msg.cmd_struct.csum == tmp)
			{
  				panServo.write(msg.cmd_struct.panPosition);
				tiltServo.write(msg.cmd_struct.tiltPosition);
				setSlider(msg.cmd_struct.sliderRate);
				setTable(msg.cmd_struct.tableRate);
				#ifdef DEBUG
				{
					Serial.print("\tCsum ok");
					Serial.print("\t  Pan: ");
					Serial.print((int)msg.cmd_struct.panPosition);
					Serial.print("\t  Tilt: ");
					Serial.print((int)msg.cmd_struct.tiltPosition);
					Serial.print("\tSlider: ");
					Serial.print((int)msg.cmd_struct.sliderRate);
					Serial.print("\tTable: ");
					Serial.println((int)msg.cmd_struct.tableRate);
				}
				#endif
			}
			else
			{
				#ifdef DEBUG
					if(msg.cmd_struct.csum != tmp)
					{
						Serial.print("bad checksum: ");
						Serial.print(tmp);
						Serial.print(" != ");
						Serial.println(msg.cmd_struct.csum);
					}
				#endif
			}
		}
	}
}

void setSlider(char rate)
{
	if(rate == 0) // stop slider
	{
		digitalWrite(SLIDER_PWM, LOW);
		digitalWrite(SLIDER_A, LOW);
		digitalWrite(SLIDER_B, LOW);
		sliderDirection = STOPPED;
	}
	else if(rate > 0) // move right
	{
		if(digitalRead(RIGHT_LIMIT) == HIGH) // limit switch not pressed
		{
			digitalWrite(SLIDER_A, LOW);
			digitalWrite(SLIDER_B, HIGH);
			digitalWrite(SLIDER_PWM, HIGH);
			sliderDirection = RIGHT;
		}
	}
	else // move left
	{
		if(digitalRead(LEFT_LIMIT) == HIGH); // limit switch not pressed
		{
			digitalWrite(SLIDER_A, HIGH);
			digitalWrite(SLIDER_B, LOW);
			digitalWrite(SLIDER_PWM, HIGH);
			sliderDirection = LEFT;
		}
	}
}

void setTable(char rate)
{
	if(rate == 0) // stop table
	{
		digitalWrite(TABLE_PWM, LOW);
		digitalWrite(TABLE_A, LOW);
		digitalWrite(TABLE_B, LOW);
	}
	else if(rate > 0) // rotate clockwise
	{
		digitalWrite(TABLE_A, LOW);
		digitalWrite(TABLE_B, HIGH);
		digitalWrite(TABLE_PWM, HIGH);
	}
	else // rotate counterclockwise
	{
		digitalWrite(TABLE_A, HIGH);
		digitalWrite(TABLE_B, LOW);
		digitalWrite(TABLE_PWM, HIGH);
	}
}

// ISR which stops the slider when the limit switches are pressed
void limitInterrupt()
{
	PORTB &= B11001111; // sets pins directly on the pro micro board
	sliderDirection = STOPPED;
}
