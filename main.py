import ffmpeg, json, random, subprocess, os, sox
from glob import glob

# load the main config.json and convert to python dict
MAIN_CONFIG = json.loads(open("config.json", "r").read())

# get lists of videos/images in folders
SOURCES_VID = glob("source/video/*")
SOURCES_IMG = glob("source/img/*")

print(f"""
    USING CONFIG:
      Target duration: {MAIN_CONFIG["target_duration"]}s
      Clip length range: {MAIN_CONFIG["clip"]["min_length"]}s - {MAIN_CONFIG["clip"]["max_length"]}s
      Clip speed range: {MAIN_CONFIG["clip"]["min_speed"]}x - {MAIN_CONFIG["clip"]["max_speed"]}x

    SOURCES:
      {len(SOURCES_VID)} videos
      {len(SOURCES_IMG)} images
""")

input("-- Press enter to continue --")

clip = {
    "source": random.choice(SOURCES_VID)
}
clip.update({
    "streams": {
        "video": ffmpeg.input(clip["source"]).video,
        "audio": ffmpeg.input(clip["source"]).audio
    },
    "duration": float(ffmpeg.probe(clip["source"])["format"]["duration"])
})

clip_video_processed = (
    clip["streams"]["video"]
    .hflip()
    .filter('setpts', f'{(1.0 / random.uniform(MAIN_CONFIG["clip"]["min_speed"], MAIN_CONFIG["clip"]["max_speed"])):.3f}*PTS')
    .trim(duration=clip["duration"] / 2)
)

clip_audio_processed = (    
    clip["streams"]["audio"]
    .filter("rubberband", pitch=2.559463094352953, tempo=2)
    .filter("atrim", duration=clip["duration"] / 2)
    .output("output/tmp/audio_processed.ogg")
    .run(overwrite_output=True)
)

tfm = sox.Transformer() # <- i am, yet again, one of these
tfm.reverse()
tfm.build_file("output/tmp/audio_processed.ogg", "output/tmp/audio_processed1.ogg")

# VICTORYYYYYYYYYYYYYYY

(
    clip_video_processed
    .output(ffmpeg.input("output/tmp/audio_processed1.ogg"), "output/output.mp4")
    .run(overwrite_output=True, quiet=False)
)