from moviepy import *
from random import randint, uniform, choice
from glob import glob

videos = glob("source/video/*")
images = glob("source/img/*")

# this is major spaghetti but i dont care
target_duration = input("Input the target duration in seconds (output will be rough, not exact) (default: 30s): ")

if not target_duration:
    target_duration = 30
else:
    target_duration = float(target_duration)

min_length = input("Input the minimum clip length in seconds (default: 0.1s): ")

if not min_length:
    min_length = 0.1
else:
    min_length = float(min_length)

max_length = input("Input the maximum clip length in seconds (default: 5s): ")

if not max_length:
    max_length = 5
else:
    max_length = float(max_length)

image_prob = input("Input the probability of images showing up (default: 70%): ")

if not image_prob:
    image_prob = 70
else:
    image_prob = float(image_prob)

video = VideoClip()

image_comp = []

while True:
    if video.duration is not None and video.duration >= target_duration:
        break

    clip = VideoFileClip(choice(videos))

    if randint(0, 100) < image_prob:
        image_clip = ImageClip(choice(images))
    else:
        image_clip = ImageClip(choice(images)).with_opacity(0)

    cut_length = max_length + 1
    
    # this is majorly inefficient but this is the punishment for thinking to even use this tool
    while min_length <= cut_length >= max_length:
        cut_end = round(uniform(0.1, clip.duration), 2)
        cut_start = round(uniform(0, cut_end), 2)
        cut_length = cut_end - cut_start

    clip = clip.subclipped(cut_start, cut_end)

    clip = clip.with_effects([
        vfx.MultiplySpeed(uniform(0.6, 3)), 
        afx.MultiplyVolume(randint(1, 4))
    ])

    clip = clip.resized((320, 240))

    print(image_clip)

    if video.duration is None:
        video = clip
    else:
        video = concatenate_videoclips([video, clip])

        image_clip = image_clip.with_start((video.duration - clip.duration) + uniform(0, 3)).resized((randint(100, 300), randint(100,300))).with_duration(uniform(clip.duration/2, clip.duration*1.4)).with_position((randint(0, 100), randint(0,100))).with_opacity(uniform(0.3,1))
        image_comp.append(image_clip)

final_video = CompositeVideoClip([video] + image_comp)

print(video.duration)

final_video.write_videofile("output/result2.mp4")
