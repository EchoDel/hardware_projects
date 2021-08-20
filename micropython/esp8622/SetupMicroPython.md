esptool --port COM4 erase_flash
esptool --port COM4 --baud 460800 write_flash --flash_size=detect 0 .\micropython\esp8622\esp8266-20210618-v1.16.bin
