# karaoke_type.py
import time, sys
try:
    from rich.console import Console
except ModuleNotFoundError:
    # graceful fallback if rich isn't installed
    class _Dummy:
        def print(self, *a, **k): print(*a, **{**k, "flush": True})
    Console = lambda: _Dummy()

console = Console()

SPEED = 1.0  # < 1.0 = faster, > 1.0 = slower

def type_line(text: str, total_time: float, color: str = "bold yellow"):
    """Reveal a line character-by-character so it lasts ~total_time seconds."""
    if total_time <= 0 or not text:
        console.print(f"[{color}]{text}[/{color}]")
        return

    # Show “Instrumental…” as dim, just waiting out its time.
    if text.lower().startswith("instrumental"):
        console.print(f"[dim]{text}[/dim]")
        time.sleep(total_time / SPEED)
        return

    chars = list(text)
    # avoid division by zero; also don’t go crazy-fast on single-char tokens
    per_char = (total_time / max(len(chars), 1)) / SPEED

    start = time.perf_counter()
    for i, ch in enumerate(chars, 1):
        console.print(f"[{color}]{ch}[/{color}]", end="")
        sys.stdout.flush()
        # simple pacing
        time.sleep(per_char)
    console.print()  # newline at end

    # Tiny correction to keep long runs closer to target timing
    elapsed = time.perf_counter() - start
    leftover = (total_time / SPEED) - elapsed
    if leftover > 0:
        time.sleep(leftover)

def printLyrics():
    colors = ["bold yellow"]  # add more if you want to cycle
    lyrics = [
        ("Instrumental...", 13.1),  #0
        ("I got Grey Goose in my system", 1.5),  #1
        ("And I'm trying to not give a fuck", 1.4),  #2
        ("Cause I'ma love you tonight", 1.6),  #3
        ("And hate you when I wake up", 1.6),  #4
        ("Girl, do you feel how I'm feeling?", 1.499),  #5
        ("Baby give me some of your love", 1.6),  #6
        ("Come give me some of your love", 1.6),  #7
        ("Come give me some of your love", 1.6),  #8
        ("'Cause it's on, turn on the radio baby", 2.7),  #9
        ("I'll turn you on, just make sure you ready baby", 3.215),  #10
        ("'Cause I'm down for anything", 1.294),  #11
        ("Tell me when you ready baby", 2.307),  #12
        ("Timing is everything", 1.209),  #13
        ("Tell me when you ready baby", 2.014),  #14
        ("'Cause you know when it's", 1.025),  #15
        ("Soakin' wet", 2.04),  #16
        ("Yeah, you know", 0.799),  #17
        ("Yeah, you know", 0.799),  #18
        ("Yeah, you know", 0.799),  #19
        ("Yeah, you know", 0.799),  #20
        ("Yeah, you know", 0.799),  #21
    ]

    try:
        for i, (text, delay) in enumerate(lyrics):
            color = colors[i % len(colors)]
            type_line(text, delay, color)
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped by user.[/dim]")

if __name__ == "__main__":
    printLyrics()