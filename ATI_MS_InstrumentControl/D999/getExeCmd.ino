void getExeCmd(String cmdCode) {
  if ( cmdCode.equals( "EXS" ) ){
    exeCmd = EXS;
    return;
  };
  if ( cmdCode.equals( "RPA" ) ){
    exeCmd = RPA;
    return;
  };
  if ( cmdCode.equals( "RAI" ) ){
    exeCmd = RAI;
    return;
  };
  if ( cmdCode.equals( "RAO" ) ){
    exeCmd = RAO;
    return;
  };
  if ( cmdCode.equals( "RAS" ) ){
    exeCmd = RAS;
    return;
  };
  if ( cmdCode.equals( "WPA" ) ){
    exeCmd = WPA;
    return;
  };
  if ( cmdCode.equals( "WAA" ) ){
    exeCmd = WAA;
    return;
  };
  if ( cmdCode.equals( "WAS" ) ){
    exeCmd = WAS;
    return;
  };
  exeCmd = idle;
}
