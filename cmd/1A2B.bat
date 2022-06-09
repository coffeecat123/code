@echo off
chcp 65001
cls
echo 歡迎來到1A2B遊戲
echo 若想中途離開遊戲，請按ctrl+c
setlocal enabledelayedexpansion
:begin
set /a d=1
set /a z=%random%%%10
:x
set /a x=%random%%%10
if %x% == %z% goto :x
:c
set /a c=%random%%%10
if %c% == %z% goto :c
if %c% == %x% goto :c
:v
set /a v=%random%%%10
if %v% == %z% goto :v
if %v% == %x% goto :v
if %v% == %c% goto :v
:ans
echo 請猜一個數(0,9999)數字不重複:
set /p an= 
if %an% leq 0 goto :ans
if %an% lss 1000 set an=%an:0=%
set /a l=0
set /a k=0
::echo %an%
if %an% gtr 9999 goto :ans
set /a q=an/1000
set /a w=an/100%%10
set /a e=an/10%%10
set /a r=an%%10
if %an% lss 1000 set /a q=0
if %an% lss 1000 set /a w=an/100
if %an% lss 1000 set /a e=an/10%%10
if %q% == %w% goto :ans
if %q% == %e% goto :ans
if %q% == %r% goto :ans
if %w% == %e% goto :ans
if %w% == %r% goto :ans
if %e% == %r% goto :ans

if %q% == %z% set /a l+=1
if %q% == %x% set /a k+=1
if %q% == %c% set /a k+=1
if %q% == %v% set /a k+=1
if %w% == %z% set /a k+=1
if %w% == %x% set /a l+=1
if %w% == %c% set /a k+=1
if %w% == %v% set /a k+=1
if %e% == %z% set /a k+=1
if %e% == %x% set /a k+=1
if %e% == %c% set /a l+=1
if %e% == %v% set /a k+=1
if %r% == %z% set /a k+=1
if %r% == %x% set /a k+=1
if %r% == %c% set /a k+=1
if %r% == %v% set /a l+=1
if %l% lss 4 echo|set /p j=%d%.
if %an% lss 1000 if %l% lss 4  echo|set /p j=0
if %l% lss 4 echo|set /p j=%an% 
if %l% lss 4 echo %l%A%k%B
if %l% lss 4 set /a d+=1 && goto :ans
echo 恭喜答對
echo 你一共猜了%d%次 在玩一次?(y/n)
set /p j= 
if %j% == y goto :begin
echo 遊戲結束，按任一鍵離開
pause >nul
endlocal