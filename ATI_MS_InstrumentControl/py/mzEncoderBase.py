import classFPGACmdCode

a = classFPGACmdCode.cmdFormat()
a.cmdWait( 100 )
a.cmdWait( 100 )
a.cmdWait( 100 )
print( a.checkCmd() )