@echo off
echo Raspberry Pi Dosya Transfer Uygulaması
echo =====================================
echo.
echo Gerekli kutuphaneler yukleniyor...
pip install -r requirements.txt
echo.
echo Uygulama baslatiliyor...
python main.py
pause
