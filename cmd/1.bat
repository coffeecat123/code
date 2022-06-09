@echo off
chcp 65001
cls
setlocal enabledelayedexpansion 
echo 猜數字(0,100)
set /a x=%random%%%100
::echo 答案%x%
:while1
set /p a= 
if %a% lss %x% echo 在大一點 && goto:while1
if %a% gtr %x% echo 在小一點 && goto:while1
if %a% equ %x% echo 恭喜答對，按任一鍵離開 &&pause>nul
endlocal