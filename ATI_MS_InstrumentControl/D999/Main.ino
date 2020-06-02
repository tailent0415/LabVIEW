#include <string.h>

enum D999Cmd{
    work,   //work state
    idle,   //idle state
    EXS,    //exist
    RPA,    //Read Port AI
    RAO,    //Read All AO
    RAI,    //Read All AI
    RAS,    //Read All Switch
    WPA,    //Write Port AO
    WAA,    //Write All AO
    WAS,    //Write All Switch
};

static int Ai[12][1024] = {{0}, {0}};
static int Ai_sum[12] = {0};
static int Ai_avg[12] = {0};
static int Ai_index = 0;

static int AO_index = 0;
static int AO_state = 0;
static int AO[9] = {0};


static int P_ind = 0;
static boolean P[6] = {false};
static boolean P_Phy[6] = {false};

static int sw_ind = 0;
static boolean sw[4] = {false};
static boolean sw_Phy[4] = {false};

int idleTime = 0;

void setup() {
  Serial.begin(9600, SERIAL_8N1); // open the Serial1 port at 9600 bps:
  Serial1.begin(9600, SERIAL_8N1); // open the Serial1 port at 9600 bps:
  analogWriteResolution(12);
  analogReadResolution(12);
  pinMode(22, OUTPUT);//LENS_T0
  pinMode(23, OUTPUT);//LENS_T1
  pinMode(24, OUTPUT);//LENS_T2
  pinMode(25, OUTPUT);//LENS_T3
  pinMode(26, OUTPUT);//LENS_T4
  pinMode(27, OUTPUT);//LENS_T5
  pinMode(28, OUTPUT);//LENS_P0
  pinMode(29, OUTPUT);//LENS_P1
  pinMode(30, OUTPUT);//LENS_P2
  pinMode(31, OUTPUT);//LENS_P3
  pinMode(32, OUTPUT);//LENS_P4
  pinMode(33, OUTPUT);//LENS_P5
  /*pinMode(34, OUTPUT);
    pinMode(35, OUTPUT);
    pinMode(36, OUTPUT);
  pinMode(37, OUTPUT);*/
  pinMode(38, OUTPUT);//CEM_T
  pinMode(39, OUTPUT);//ESPY_T
  pinMode(40, OUTPUT);//ESPY_EN
  pinMode(41, OUTPUT);//DYNODE_T
  pinMode(42, OUTPUT);//DYNODE_EN
  pinMode(43, OUTPUT);//CEM_EN
  pinMode(44, OUTPUT);//LENS_EN

  pinMode(LED_BUILTIN, OUTPUT);
  idleTime = millis();
}

static String cmdStr = "";
static String errMsg = "";

String address = "@999";
String endStr = ";FF";

String receiveDataBuffer = "";
uint8_t receiveDataBufferMaxLength = 100;

static D999Cmd exeCmd = idle;
String responseStr = "";

char tempChar[1];

void loop(){
  while (Serial1.available() > 0) {
    delay(10);
    Serial1.readBytes(tempChar, 1);
    receiveDataBuffer.concat(tempChar[0]);
    exportError( receiveDataBuffer );
    if( receiveDataBuffer.endsWith( endStr ) ){
      if( checkAddress( address, receiveDataBuffer ) ){
        responseStr = runProcess( cmdStr );
        exportError( responseStr + endStr );
        Serial1.println( responseStr + endStr );
        idleTime = millis();
      }
    }
  }
  receiveDataBuffer.remove(0);
  
  PhyRead_AI();
  PhyWrite_AO();
  PhyWrite_P();
  PhyWrite_SW();

  if( idleTime-millis() > 5000 ){
    exeCmd = idle;
  }
  else{
    exeCmd = work;
  }
  digitalWrite(LED_BUILTIN, 0);
  
}
