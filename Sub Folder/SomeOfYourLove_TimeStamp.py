# tap_timing.py
import time, textwrap

LYRICS = """
Instrumental...
I got Grey Goose in my system
And I'm trying to not give a fuck
Cause I'ma love you tonight
And hate you when I wake up
Girl, do you feel how I'm feeling?
Baby give me some of your love
Come give me some of your love
Come give me some of your love
'Cause it's on, turn on the radio baby
I'll turn you on, just make sure you ready baby
'Cause I'm down for anything
Tell me when you ready baby
Timing is everything
Tell me when you ready baby
'Cause you know when it's
Soakin' wet
Yeah, you know
Yeah, you know
Yeah, you know
Yeah, you know
Yeah, you know
"""

def main():
    lines = [l.strip() for l in LYRICS.splitlines() if l.strip() and not (l.startswith('[') and l.endswith(']'))]
    print("Timing helper\n")
    print("Play the song, then:")
    print(" - Press ENTER to start the timer.")
    print(" - Press ENTER each time the NEXT line should appear.")
    input("\nReady? Press ENTER to start…")
    print("\nStart timing! (Press ENTER for each NEXT line.)\n")

    stamps = []
    t0 = time.perf_counter()
    for i, line in enumerate(lines, 1):
        input(f"[{i:02}] Next line: {line!r} — press ENTER at the right moment…")
        now = time.perf_counter()
        stamps.append(now - t0)
        # small visual spacer
        print()

    # convert absolute stamps to per-line delays
    delays = [stamps[0]] + [stamps[i] - stamps[i-1] for i in range(1, len(stamps))]

    print("\nCopy/paste this into your code:")
    print("lyrics = [")
    for line, d in zip(lines, delays):
        print(f"    ({line!r}, {round(d, 3)}),")
    print("]")

if __name__ == "__main__":
    main()