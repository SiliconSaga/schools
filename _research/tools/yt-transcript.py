"""Save a YouTube video's captions as timestamped text, one caption per line.

Usage: python yt-transcript.py <video id> <output file>
Needs the youtube-transcript-api package. Captions are usually auto-generated, so names
and numbers must be checked by ear against the video before they are quoted.
"""
import sys

from youtube_transcript_api import YouTubeTranscriptApi

video_id, out_path = sys.argv[1], sys.argv[2]
try:
    snippets = [(s.start, s.text) for s in YouTubeTranscriptApi().fetch(video_id)]
except AttributeError:
    snippets = [(s["start"], s["text"]) for s in YouTubeTranscriptApi.get_transcript(video_id)]

with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
    for start, text in snippets:
        h, rem = divmod(int(start), 3600)
        m, s = divmod(rem, 60)
        fh.write(f"[{h}:{m:02d}:{s:02d}] {' '.join(text.split())}\n")
print(f"{len(snippets)} captions, last at {int(snippets[-1][0]) // 60} min -> {out_path}")
