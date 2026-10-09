"""Save a YouTube video's captions as timestamped text, one caption per line.

Usage: python yt-transcript.py <video id> <output file>
Needs the youtube-transcript-api package. Captions are usually auto-generated, so names
and numbers must be checked by ear against the video before they are quoted.
"""
import sys

from youtube_transcript_api import YouTubeTranscriptApi

if len(sys.argv) < 3:
    sys.exit(__doc__)
video_id, out_path = sys.argv[1], sys.argv[2]

# The package renamed its entry point in 1.x; pick by what the installed version offers.
if hasattr(YouTubeTranscriptApi, "get_transcript"):
    snippets = [(s["start"], s["text"]) for s in YouTubeTranscriptApi.get_transcript(video_id)]
else:
    snippets = [(s.start, s.text) for s in YouTubeTranscriptApi().fetch(video_id)]
if not snippets:
    sys.exit("no captions returned")

with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
    for start, text in snippets:
        h, rem = divmod(int(start), 3600)
        m, s = divmod(rem, 60)
        fh.write(f"[{h}:{m:02d}:{s:02d}] {' '.join(text.split())}\n")
print(f"{len(snippets)} captions, last at {int(snippets[-1][0]) // 60} min -> {out_path}")
