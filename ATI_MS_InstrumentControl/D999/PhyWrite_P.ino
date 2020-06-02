void PhyWrite_P() {
  int P_pin[] = {28, 29, 30, 31, 32, 33};
  int a = P_pin[P_ind];
  if (P[P_ind] != P_Phy[P_ind]) {
    //digitalWrite(LED_BUILTIN, LOW);
    P_Phy[P_ind] = P[P_ind] ;
    digitalWrite( a, P_Phy[P_ind]);
  }
  P_ind++;
  if (P_ind >= 6) P_ind = 0;
}
