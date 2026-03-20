import subprocess
import os

# Paths to the generated images
images = [
    "/Users/orestis/.gemini/antigravity/brain/48b51eb6-0b09-4d3f-b658-32370bbf5050/geese_cartagena_1771890531965.png",
    "/Users/orestis/.gemini/antigravity/brain/48b51eb6-0b09-4d3f-b658-32370bbf5050/geese_casa_en_el_agua_1771890552083.png",
    "/Users/orestis/.gemini/antigravity/brain/48b51eb6-0b09-4d3f-b658-32370bbf5050/geese_medellin_metrocable_1771890572797.png"
]

output_dir = "/Users/orestis/.gemini/antigravity/brain/48b51eb6-0b09-4d3f-b658-32370bbf5050/"
temp_clips = []

def create_clip(image_path, output_path, zoom_type="zoom_in"):
    """Creates a 4-second clip with zoom effect."""
    print(f"Processing {image_path}...")
    
    # Zoom in effect: scale increases over time
    # Zoom pan filter: zoom=min(zoom+0.0015,1.5)
    if zoom_type == "zoom_in":
        vf = "zoompan=z='min(zoom+0.0015,1.5)':d=100:s=1280x720"
    else:
        vf = "zoompan=z='1.5-0.0015*on':d=100:s=1280x720"

    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", vf,
        "-c:v", "libx264",
        "-t", "4",
        "-pix_fmt", "yuv420p",
        "-profile:v", "baseline",
        "-level", "3.0",
        output_path
    ]
    subprocess.run(cmd, check=True)

try:
    # 1. Create individual clips
    for i, img in enumerate(images):
        clip_path = os.path.join(output_dir, f"clip_{i}.mp4")
        create_clip(img, clip_path, zoom_type="zoom_in" if i % 2 == 0 else "zoom_out")
        temp_clips.append(clip_path)

    # 2. Concat clips
    concat_list_path = os.path.join(output_dir, "clips.txt")
    with open(concat_list_path, "w") as f:
        for clip in temp_clips:
            f.write(f"file '{clip}'\n")

    final_output = os.path.join(output_dir, "geese_colombia_animation.mp4")
    print("Stitching clips and adding silent audio...")
    
    # We use -f lavfi -i anullsrc to add a silent audio track
    # and re-encode to ensure the pixel format is strictly yuv420p (limited range)
    cmd_concat = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", "format=yuv420p,scale=out_range=limited",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-level", "3.1",
        "-c:a", "aac",
        "-shortest",
        final_output
    ]
    subprocess.run(cmd_concat, check=True)
    
    print(f"Video created successfully: {final_output}")

except Exception as e:
    print(f"Error: {e}")
