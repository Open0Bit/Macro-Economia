@echo off
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir scripts 2>nul
mkdir notebooks 2>nul
mkdir figures 2>nul
mkdir output 2>nul
mkdir docs 2>nul
mkdir tests 2>nul
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
pause
