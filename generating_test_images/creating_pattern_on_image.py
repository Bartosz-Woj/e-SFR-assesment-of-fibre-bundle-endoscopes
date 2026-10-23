__author__ = "Bartosz Wojciechowski"
__copyright__ = "Copyright 2026, Bartosz Wojciechowski"
__license__ = "GPL-3.0"
__version__ = "1.0.0"
__status__ = "Production"

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog

import inclined_plane_generator as ipg
import pattern_generator as pg

def merge_images_overlay(overlay_img, background_img, alpha=1.0):
    """
    Merge overlay image onto background image using alpha compositing.
    
    Parameters:
    -----------
    overlay_img : PIL.Image or numpy array
        RGBA overlay image
    background_img : PIL.Image or numpy array
        RGBA background image
    alpha : float (0.0 to 1.0)
        Global transparency factor for overlay
    
    Returns:
    --------
    PIL.Image
        Merged RGBA image
    """
    
    if isinstance(overlay_img, Image.Image):
        overlay_arr = np.array(overlay_img, dtype=np.float32)
    else:
        overlay_arr = overlay_img.astype(np.float32)
        
    if isinstance(background_img, Image.Image):
        background_arr = np.array(background_img, dtype=np.float32)
    else:
        background_arr = background_img.astype(np.float32)
    
    if overlay_arr.shape != background_arr.shape:
        raise ValueError(f"Images must have same dimensions. "
                        f"Got {overlay_arr.shape} and {background_arr.shape}")
    
    overlay_arr = overlay_arr / 255.0
    background_arr = background_arr / 255.0
    
    if overlay_arr.shape[2] == 4:
        overlay_rgb = overlay_arr[:, :, :3]
        overlay_alpha = overlay_arr[:, :, 3:] * alpha  # Apply global alpha
    else:
        overlay_rgb = overlay_arr
        overlay_alpha = np.ones_like(overlay_arr[:, :, :1]) * alpha
    
    if background_arr.shape[2] == 4:
        background_rgb = background_arr[:, :, :3]
        background_alpha = background_arr[:, :, 3:]
    else:
        background_rgb = background_arr
        background_alpha = np.ones_like(background_arr[:, :, :1])
    
    result_rgb = overlay_rgb * overlay_alpha + background_rgb * (1 - overlay_alpha)
    result_alpha = overlay_alpha + background_alpha * (1 - overlay_alpha)
    
    result = np.concatenate([result_rgb, result_alpha], axis=2)
    result = np.clip(result * 255, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result, mode='RGBA')



def test_signle_image(output_directory='output'):
    """Test merging a single image."""
    
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            ("All files", "*.*")
        ]
    )
    if not file_path:
        print("No base image selected. Exiting.")
        return
    
    base_img = Image.open(file_path).convert('RGBA')
    base_img = np.array(base_img)
    img_width, img_height = base_img.shape[1], base_img.shape[0]
    print(f"Base image shape: {base_img.shape}")
    
    overlay_img = pg.create_transparent_circles_pattern(
        width=img_width,                # Image width
        height=img_height,               # Image height
        bg_color=(0, 0, 0, 200), # Spacing color (R,G,B, Alpha)
        circle_color=(0, 0, 0, 0), # Fibers color (R,G,B,A)
        circle_radius=3,         # Radius of each circle
        spacing=2,
        blur_pixels=1)                # Spacing between circles    
    
    
    # Display detailed comparison
    merged_img = merge_images_overlay(overlay_img, base_img, alpha=1.0)
    
    merged_img=merged_img.convert("RGB")
    plt.figure(figsize=(12, 8))
    plt.imshow(merged_img)
    plt.title("Merged Image")
    plt.axis('off')
    plt.show()
    merged_img.save(f'{output_directory}/lunna_pattern.jpg', format="JPEG",  quality=100)


if __name__ == "__main__":
    X = (50, 50, 50, 255)
    Y = (220, 220, 220, 255)
    directory = 'test_images'
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_signle_image(directory)
    
    print("\nAll images created and saved successfully!")
    
        
 