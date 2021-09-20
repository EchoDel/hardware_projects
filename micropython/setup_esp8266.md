# Upload micropython 1.16
Download from http://micropython.org/download#esp8266
Local machine:
`pip install esptool
esptool --port /COM4 erase_flash
esptool --port /COM4 --baud 460800 write_flash --flash_size=detect 0 micropython\esp8622\esp8266-20210618-v1.16.bin`

# Install Packages
Micro Controller
`import upip 
upip.install('logging')`


# Cross complile required packages
Local Machine
`pip install mpy-cross
mpy-cross .\micropython\tinyweb-master\tinyweb\server.py
mv .\micropython\tinyweb-master\tinyweb\server.mpy .\tinyweb\server.mpy`


# Sync all the files
Run flash on all needed files
