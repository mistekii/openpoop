import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import *
from random import randint, uniform, choice
from glob import glob
import threading

def generate_video():
    videos = glob(videos_entry.get() + "/*")
    images = glob(images_entry.get() + "/*")

    try:
        target_duration = float(target_duration_entry.get())
        min_length = float(min_length_entry.get())
        max_length = float(max_length_entry.get())
        min_speed = float(min_speed_entry.get())
        max_speed = float(max_speed_entry.get())
        image_prob = float(image_prob_entry.get())
    except ValueError:
        messagebox.showerror("Error", "enter fucking numbers idiot")
        return

    video = VideoClip()
    image_comp = []

    while True:
        if video.duration is not None and video.duration >= target_duration:
            break

        clip = VideoFileClip(choice(videos))

        if images:
            if randint(0, 100) < image_prob:
                image_clip = ImageClip(choice(images))
            else:
                image_clip = ImageClip(choice(images)).with_opacity(0)

        cut_length = max_length + 1
        while min_length <= cut_length >= max_length:
            cut_end = round(uniform(0.1, clip.duration), 2)
            cut_start = round(uniform(0, cut_end), 2)
            cut_length = cut_end - cut_start

        clip = clip.subclipped(cut_start, cut_end)
        clip = clip.with_effects([
            vfx.MultiplySpeed(uniform(min_speed, max_speed)),
            afx.MultiplyVolume(randint(1, 4))
        ])
        clip = clip.resized((320, 240))

        if video.duration is None:
            video = clip
        else:
            video = concatenate_videoclips([video, clip])

            if images:
                image_clip = image_clip.with_start((video.duration - clip.duration) + uniform(0, 3)).resized((randint(100, 300), randint(100, 300))).with_duration(uniform(clip.duration / 2, clip.duration * 1.4)).with_position((randint(0, 100), randint(0, 100))).with_opacity(uniform(0.3, 1))
                image_comp.append(image_clip)

    final_video = CompositeVideoClip([video] + image_comp)
    print(video.duration)
    final_video.write_videofile(output_entry.get() + "/result.mp4")
    messagebox.showinfo("Info", "your poop is served sir")

def browse_videos():
    folder_selected = filedialog.askdirectory()
    videos_entry.delete(0, tk.END)
    videos_entry.insert(0, folder_selected)

def browse_images():
    folder_selected = filedialog.askdirectory()
    images_entry.delete(0, tk.END)
    images_entry.insert(0, folder_selected)

def browse_output():
    folder_selected = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_selected)

def start_generation():
    threading.Thread(target=generate_video).start()

root = tk.Tk()
root.title("OpenPoop (poop version with gui this time)")

tk.Label(root, text="vidya folder:").grid(row=0, column=0, sticky="w")
videos_entry = tk.Entry(root, width=50)
videos_entry.grid(row=0, column=1)
videos_button = tk.Button(root, text="browze", command=browse_videos)
videos_button.grid(row=0, column=2)

tk.Label(root, text="image folder:").grid(row=1, column=0, sticky="w")
images_entry = tk.Entry(root, width=50)
images_entry.grid(row=1, column=1)
images_button = tk.Button(root, text="Bowser", command=browse_images)
images_button.grid(row=1, column=2)

tk.Label(root, text="output folder:").grid(row=2, column=0, sticky="w")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1)
output_button = tk.Button(root, text="brow's", command=browse_output)
output_button.grid(row=2, column=2)

tk.Label(root, text="target duration (seconds):").grid(row=3, column=0, sticky="w")
target_duration_entry = tk.Entry(root)
target_duration_entry.insert(0, "30")
target_duration_entry.grid(row=3, column=1)

tk.Label(root, text="minimum clip length (seconds):").grid(row=4, column=0, sticky="w")
min_length_entry = tk.Entry(root)
min_length_entry.insert(0, "0.1")
min_length_entry.grid(row=4, column=1)

tk.Label(root, text="maximum clip length (seconds):").grid(row=5, column=0, sticky="w")
max_length_entry = tk.Entry(root)
max_length_entry.insert(0, "3")
max_length_entry.grid(row=5, column=1)

tk.Label(root, text="image probability (%):").grid(row=6, column=0, sticky="w")
image_prob_entry = tk.Entry(root)
image_prob_entry.insert(0, "70")
image_prob_entry.grid(row=6, column=1)

tk.Label(root, text="min video speed multiply:").grid(row=7, column=0, sticky="w")
min_speed_entry = tk.Entry(root)
min_speed_entry.insert(0, "0.6")
min_speed_entry.grid(row=7, column=1)

tk.Label(root, text="max video speed multiply:").grid(row=8, column=0, sticky="w")
max_speed_entry = tk.Entry(root)
max_speed_entry.insert(0, "3")
max_speed_entry.grid(row=8, column=1)

generate_button = tk.Button(root, text="let the Sewage spill", command=start_generation)
generate_button.grid(row=9, column=1)

root.mainloop()