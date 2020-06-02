int PhyWrite_AO() {
  //Dynode,CEM,ESI,LENS1 ~ 8//
  int AO_avg[] = {41,38,39,22,23,24,25,26,27};
  int j = AO_avg[AO_index];
  int k = 0;
  switch (AO_state) {
    case 0:
      digitalWrite(j, LOW);
      break;
    case 1:
    if(AO[AO_index] <= -1) k =0;
    else k = AO[AO_index];
      analogWrite(DAC0, k);
      break;
    case 2:
      digitalWrite(j, HIGH);
      break;
    case 3:
      digitalWrite(j, LOW);
      AO_index++;
      if (AO_index >= 9) AO_index = 0;
      break;
  }
  AO_state++;
  if (AO_state >= 4) AO_state = 0;
}
