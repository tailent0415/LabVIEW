@999 XXX M;FF
@999    arduino標頭
XXX     命令
M       辨識碼
;FF     結尾符
XXX 命令表
EXS                         詢問arduino
RPA index                   讀取指定的 AI Port 狀態
RAO							讀取全部 AO 狀態
RAI							讀取全部 AI 狀態
RAS							讀取全部 Switch 狀態
WPA	index,value				寫入指定的 AO Port 狀態
WAA Value0,Value1...,Value8	依序寫入全部的 AO Port 新狀態
WAS							依序寫入全部的 Switch, 新狀態Value 是由4個 Switch bool 轉換成 uint8