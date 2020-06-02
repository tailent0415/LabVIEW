String runProcess( String cmdStr ) {
  String cmdCode = "";
  String valStr = "";
  String responseVal = "";
  int spaceIdx = cmdStr.indexOf(" ");
  int commaIdx = 0;
  int portIdx = 0;
  int value = 0;
  cmdCode = cmdStr.substring( 0, spaceIdx );
  valStr = cmdStr.substring( spaceIdx+1, cmdStr.length() );
  getExeCmd( cmdCode );
  switch( exeCmd ){
    case EXS:
      responseVal = "999";
      break;
    case RPA:
      responseVal = readPortAI( valStr.toInt() );
      break;
    case RAI:
      responseVal = readAllAI();
      break;
    case RAO:
      responseVal = readAllAO();
      break;
    case RAS:
      responseVal = readAllSW();
      break;
    case WPA:
      commaIdx = valStr.indexOf(",");
      portIdx = valStr.substring( 0, commaIdx ).toInt();
      value = valStr.substring( commaIdx+1, valStr.length() ).toInt();
      responseVal = writePortAO( portIdx, value );
      break;
    case WAA:
      responseVal = writeAllAO( valStr );
      break;
    case WAS:
      responseVal = writeAllSwitch( valStr.toInt() );
      break;
    default:
      responseVal = "-1";
      errMsg = "CommandError";
  };
  if( responseVal.equals( "-1" ) ){
    responseVal = errMsg;
  }
  return responseVal;
};

//========================================================================================================
// Read Port AI
String readPortAI( int i ) {
  if ( i < sizeof(AO)/sizeof(int) ) {
    return  String( Ai_avg[i] ); // 5V/4096
  }
  errMsg = "IndexError";
  return "-1";
};
//========================================================================================================
// Read All AI
String readAllAI() {
  String aiConcat;
  for ( int i = 0; i < sizeof(Ai_avg)/sizeof(int); i++) {
    aiConcat.concat( Ai_avg[i] );
    if (i == sizeof(Ai_avg)/sizeof(int)-1 ){
      break;
    }
    aiConcat.concat( "," );
  }
  if ( aiConcat.length() != 0 ){
    return aiConcat;
  }
  errMsg = "ValueError";
  return "-1";
};
//========================================================================================================
// Read All AO
String readAllAO() {
  String aoConcat;
  for ( int i = 0; i < sizeof( AO )/sizeof(int); i++) {
    if( i >= 3 ){
      if( P[i-3] == 1 ){
        aoConcat.concat( '-' );
      }
    }
    aoConcat.concat( AO[i] );
    if ( i == sizeof(AO)/sizeof(int)-1 ){
      break;
    }
    aoConcat.concat( "," );
  }
  
  if ( aoConcat.length() != 0 ){
    return aoConcat;
  }
  errMsg = "ValueError";
  return "-1";
};
//========================================================================================================
// Read All Switch
String readAllSW( ) {
  int value = 0;
  for (int i = 0; i < sizeof(sw)/sizeof(boolean) ; i++) {
    value += sw[i] << i;
  }
  return String( value );
};
//========================================================================================================
// Write Port AO
String writePortAO( int port , int value){
  if (port < 0 || port > 8 ) {
    errMsg = "IndexError";
    return "-1";
  }
  if (value < -4095 || value > 4095) {
    errMsg = "ValueError";
    return "-1";
  }
  if ( port >= 3 ) {
    if (value < 0) {
      P[port-3] = 1;
    }
    else {
      P[port-3] = 0;
    }
  }
  AO[port] = abs(value);
  return "0";
}
//========================================================================================================
// Write All AO
String writeAllAO(String valStr) {
  char bufferChar[valStr.length()+1];
  valStr.toCharArray(bufferChar, valStr.length()+1);
  char* token = strtok(bufferChar, ",");
  String writeRes = "";
  int idx = 0;
  while (token != NULL) {
    writeRes = writePortAO( idx, String(token).toInt() );
    if( writeRes.equals( "-1" ) ){
      token = NULL;
      break;
    }
    token = strtok(NULL, ",");
    idx++;
  };
  return writeRes;
}
//========================================================================================================
// Write All Switch
String writeAllSwitch(int ctrlVal) {
  for (int i = 0; i < sizeof(sw)/sizeof(boolean); i++) {
    sw[i] = bitRead(ctrlVal, i);
  }
  return "0";
}
//========================================================================================================
