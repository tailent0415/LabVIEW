void PhyRead_AI(void) {
  int Ai_number = 12;
  for (int i = 0; i < Ai_number; i++) {
    int Ai_read = analogRead(i);
    delayMicroseconds(100);
    Ai_sum[i] += Ai_read;
    Ai_sum[i] -= Ai[i][Ai_index];
    Ai[i][Ai_index] = Ai_read;
    Ai_avg[i] = Ai_sum[i] >> 6;
  }
  Ai_index ++;
  if ( Ai_index == 64) Ai_index = 0;
}
