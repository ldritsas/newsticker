#program to run a news ticker on a 16x2 CharLCD with a Raspberry Pi Zero W
#Will use the NewsAPI service for headlines and scroll through them
#will use RPLCD Library

##newsapi key='record your key here, get one free at newsapi.org'

##include libraries
import RPi.GPIO as GPIO
import time
from subprocess import check_output
from datetime import datetime
from RPLCD.gpio import CharLCD
import json
import requests

##configure the LCD, this is my wiring scheme
lcd = CharLCD(pin_rs=22, pin_e=18, pin_rw=None, pins_data=[16, 11, 12, 15], numbering_mode=GPIO.BOARD, cols=16, rows=2, dotsize=8)
lcd.clear()

##request top headlines from a specific country from NewsAPI
##check thier site for the correct country code
url = ('https://newsapi.org/v2/top-headlines?country=<your country code>&apiKey=<your key here>')
r = requests.get(url)
news = json.loads(r.text)

##test scripts to check request result, if you want to.
##run these and two files will be created the same library
    ##with open('news_text.json', 'w') as f:
    ##    json.dump(news, f, indent=2)
    ##f.close()

    ##f = open('headlines.txt', 'w')
    ##f.write(articles['title'] + ' \n')
    ##f.close()

##create empty list for strings that will be topline date and time and second line scrolling headlines
framebuffer = ['', '',]

##write the framebuffer list to the LCD
def write_to_lcd(lcd, framebuffer, num_cols):
    """Write the framebuffer out to the specified LCD."""
    lcd.home()
    ##get current time for top row
    framebuffer[0] = datetime.now().strftime('%a,%d %b %H:%M')
    ##write each row to the lcd
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')

##define function to infinitely loop titles on second line   
def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.1):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)
        
##build long string of all titles with | separator
titles = ''
for articles in news['articles']:
    ##print(articles['title'])
    titles = titles + (articles['title'] + ' | ')

##pass titles string into loop_string function
while True:
    loop_string(titles, lcd, framebuffer, 1, 16)

lcd.close() 
GPIO.cleanup()
