__author__ = "Bartosz Wojciechowski"
__copyright__ = "Copyright 2026, Bartosz Wojciechowski"
__license__ = "GPL-3.0"
__version__ = "1.0.0"
__status__ = "Production"

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

import os


def create_transparent_circles_pattern(
    width=1062,
    height=1061,
    bg_color=(30, 30, 30, 255), # Background (spacing) color (R,G,B, Alpha)
    circle_color=(255, 255, 255, 255), # Circle fill color (R,G,B, Alpha)
    circle_radius=3,            # Radius of each circle
    spacing=2,                  # Spacing between circles
    blur_pixels=0,              # Optional: number of pixels to blur the circles (0 for no blur)
):
    """
    Create an image with a background color and transparent circles
    arranged in a hexagonal/honeycomb pattern.
    """
    
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    diameter = circle_radius * 2

    # Center-to-center distance between circles (including spacing)
    center_distance = diameter + spacing
  
    # Vertical spacing for hexagonal pattern (height of equilateral triangle)
    vertical_spacing = center_distance * math.sqrt(3) / 2
    
    num_cols = int(width // center_distance) + 3  
    num_rows = int(height // vertical_spacing) + 3  
    
    for row in range(num_rows):
        x_offset = (center_distance / 2) if (row % 2 == 1) else 0
        
        for col in range(num_cols):

            center_x = x_offset + col * center_distance
            center_y = row * vertical_spacing
            
            if (center_x - circle_radius <= width + circle_radius and 
                center_y - circle_radius <= height + circle_radius):

                top_left = (center_x - circle_radius, center_y - circle_radius)
                bottom_right = (center_x + circle_radius, center_y + circle_radius)
                
                draw.ellipse([top_left, bottom_right], fill=circle_color)

    if blur_pixels > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur_pixels))
    
    return image



if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)


    img = create_transparent_circles_pattern()
    img.save("transparent_circles_patternZuzia.png", "PNG")
    '''
    # Create variant patterns
    print("\nCreating variant patterns...")
    create_variant_patterns()
    '''
    print("\nAll patterns created successfully!")
    
