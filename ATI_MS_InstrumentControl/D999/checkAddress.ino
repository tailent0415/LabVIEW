// 檢查指令段正確性, 並回傳 command 區段字串
bool checkAddress(String address, String bufferStr){
  String temp = "";
  int cmdTermIdx = bufferStr.length()-3;
  int i = bufferStr.lastIndexOf( address );
  if (i != -1){
    /*if( checkVerifyCode( bufferStr.substring( i, cmdTermIdx ) ) ){
      cmdStr = bufferStr.substring( i+5, cmdTermIdx-1 );
      return true;
    }
    exportError( "VerifyError" );
    return true;*/
    
    cmdStr = bufferStr.substring( i+5, cmdTermIdx-1 );
    return true;
  }
  return false;
}


// 檢查校驗碼正確性
bool checkVerifyCode( String submitStr ){
  uint8_t sum = 0;
  for( int i=0; i<submitStr.length()-1; i++ ){
    sum += submitStr[i];
  }
  exportError( String(sum) );
  exportError( String(0+submitStr[ submitStr.length()-1 ]) );
  if( sum == ( 0+submitStr[ submitStr.length()-1 ] ) ){
    return true;
  }
  return false;
}
