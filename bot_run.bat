@echo off

call %~dp0bot_prognoz\venv\Scripts\activate

cd %~dp0bot_prognoz

set TOKEN=6243379612:AAFBILO3Il2bkBgs-JIBN4PnGRTneDmcuAM
set OWTOKEN=b73b7c13e254f827ddaf558be5fe8261

python tg_bot.py

pause