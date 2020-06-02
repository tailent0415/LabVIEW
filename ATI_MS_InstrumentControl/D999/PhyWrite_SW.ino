void PhyWrite_SW() {
  int sw_index[] = {44, 40, 42, 43};
  int a = sw_index[sw_ind];
  if (sw[sw_ind] != sw_Phy[sw_ind]) {
    sw_Phy[sw_ind] = sw[sw_ind] ;
    digitalWrite( a, sw_Phy[sw_ind]);
  }
  sw_ind++;
  if (sw_ind >= 4) sw_ind = 0;

}
