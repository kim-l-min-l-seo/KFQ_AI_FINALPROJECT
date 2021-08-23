@echo off
color a
rmdir /s KFQ_FinalProject

msg %username% Download ...

color 4
git clone https://github.com/IIBlackCode/KFQ_FinalProject.git


msg %username% Download Success!! server start by KFQ_FinalProject/start_Server.cmd

cd KFQ_FinalProject/WAS
python manage.py runserver