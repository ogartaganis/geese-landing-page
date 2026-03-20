import os
from PIL import Image

# Map of (Original File Name, Target Cartoon Image)
# This mapping matches the new chronological order from 1 to 6
mappings = [
    ("1. Monserrate.jpg", "geese_monserrate.png"),
    ("2. Villa de leyva.jpg", "geese_villa.png"),
    ("3. Cartagena.jpg", "geese_cartagena_1771890531965.png"),
    ("4. Aviario nacional.jpg", "geese_birds_v13_final_1771930947845.png"),
    ("5. Casa en el agua.jpg", "geese_casa_en_el_agua_1771890552083.png"),
    ("6. Medellin hot tub.jpg", "geese_medellin.png")
]

orig_dir = "images_original"
cartoon_dir = "images"
out_dir = "images_cropped"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for orig_name, cartoon_name in mappings:
    orig_path = os.path.join(orig_dir, orig_name)
    cartoon_path = os.path.join(cartoon_dir, cartoon_name)
    
    if not os.path.exists(orig_path):
        print(f"Skipping {orig_name}: not found.")
        continue
    if not os.path.exists(cartoon_path):
        print(f"Skipping {cartoon_name}: not found.")
        continue

    with Image.open(cartoon_path) as c_img:
        target_w, target_h = c_img.size

    with Image.open(orig_path) as o_img:
        o_w, o_h = o_img.size
        # Maintain aspect ratio, cover the target area, center crop
        target_aspect = target_w / target_h
        o_aspect = o_w / o_h
        
        if o_aspect > target_aspect:
            # Original is wider than target -> crop left and right
            new_h = target_h
            new_w = int(new_h * o_aspect)
        else:
            # Original is taller than target -> crop top and bottom
            new_w = target_w
            new_h = int(new_w / o_aspect)
            
        # Resize to cover
        resized = o_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_w - target_w) / 2
        top = (new_h - target_h) / 2
        right = (new_w + target_w) / 2
        bottom = (new_h + target_h) / 2
        
        cropped = resized.crop((left, top, right, bottom))
        
        # Determine output name (e.g. before_1.jpg)
        idx = mappings.index((orig_name, cartoon_name)) + 1
        out_path = os.path.join(out_dir, f"before_{idx}.jpg")
        
        cropped.save(out_path, quality=95)
        print(f"Saved {out_path} with size {target_w}x{target_h} (cropped from {o_w}x{o_h})")
