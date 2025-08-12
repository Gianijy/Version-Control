import sys
import time
from rich import print

def printLyrics():
    colors = [
        "bold yellow"]

    lyrics = [
        ("Instrumental...", 13.36),  #0
        ("I got Grey Goose in my system", 1.81),  #1
        ("And I'm trying to not give a fuck", 1.456),  #2
        ("Cause I'ma love you tonight", 1.661),  #3
        ("And hate you when I wake up", 1.712),  #4
        ("Girl, do you feel how I'm feeling?", 1.499),  #5
        ("Baby give me some of your love", 1.919),  #6
        ("Come give me some of your love", 1.795),  #7
        ("Come give me some of your love", 1.669),  #8
        ("'Cause it's on, turn on the radio baby", 3.296),  #9
        ("I'll turn you on, just make sure you ready baby", 3.215),  #10
        ("'Cause I'm down for anything", 1.294),  #11
        ("Tell me when you ready baby", 2.307),  #12
        ("Timing is everything", 1.209),  #13
        ("Tell me when you ready baby", 2.014),  #14
        ("'Cause you know when it's", 1.025),  #15
        ("Soakin' wet", 2.112),  #16
        ("Yeah, you know", 0.799),  #17
        ("Yeah, you know", 0.799),  #18
        ("Yeah, you know", 0.799),  #19
        ("Yeah, you know", 0.799),  #20
        ("Yeah, you know", 0.799),  #21
    ]

    for i, (text, delay) in enumerate(lyrics):
        color = colors[i % len(colors)]  # cycle through colors
        print(f"[{color}]{text}[/{color}]")
        time.sleep(delay)

if __name__ == "__main__":
    printLyrics()