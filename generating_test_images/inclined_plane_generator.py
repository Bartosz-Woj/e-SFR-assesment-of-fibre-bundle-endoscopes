__author__ = "Bartosz Wojciechowski"
__copyright__ = "Copyright 2026, Bartosz Wojciechowski"
__license__ = "GPL-3.0"
__version__ = "1.0.0"
__status__ = "Production"

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def create_inclined_plane_image(n, m, X, Y, blur_pixels=10, angle_degrees=30):
    """
    Create an image with an inclined plane separating two colors with blur.
    
    Parameters:
    -----------
    n : int
        Image width in pixels
    m : int
        Image height in pixels
    X : tuple
        RGBA color below the plane (R,G,B,A)
    Y : tuple
        RGBA color above the plane (R,G,B,A)
    blur_pixels : int
        Number of pixels for edge blur
    angle_degrees : float
        Angle of inclination in degrees (0 = horizontal, 90 = vertical)
    
    Returns:
    --------
    PIL.Image
        Image with inclined plane and blurred edge
    """

    angle = np.radians(angle_degrees)
    
    x = np.linspace(-1, 1, m)
    y = np.linspace(-1, 1, n)
    X_grid, Y_grid = np.meshgrid(x, y, indexing='ij')
    
    # Define inclined plane equation: ax + by + c = 0
    a = np.sin(angle)
    b = np.cos(angle)
    c = 0  # Plane goes through center
    
    # Calculate signed distance from each pixel to the plane
    distances = a * X_grid + b * Y_grid + c
    
    max_dist = np.max(np.abs(distances))
    if max_dist > 0:
        normalized_dist = distances / max_dist
    else:
        normalized_dist = distances
    
    blur_factor = blur_pixels / max(n, m)
    
    # Smooth transition using sigmoid function
    transition = 1 / (1 + np.exp(-normalized_dist / blur_factor))
    
    # Create RGBA arrays for both colors
    X_array = np.array(X).reshape(1, 1, 4)
    Y_array = np.array(Y).reshape(1, 1, 4)

    transition_3d = transition[:, :, np.newaxis]
    image_array = X_array * (1 - transition_3d) + Y_array * transition_3d

    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    image = Image.fromarray(image_array, mode='RGBA')

    return image, normalized_dist


# Example usage
if __name__ == "__main__":
    # Define image dimensions
    n, m = 300, 150
    
    # Define colors (RGBA)
    # Color X: below the plane (blue with transparency)
    X = (100, 100, 100, 255)
    
    # Color Y: above the plane (orange with transparency)
    Y = (200, 200, 200, 255)
    
    # Create inclined plane image
    print(f"Creating {n}x{m} image with inclined plane...")
    img, distances = create_inclined_plane_image(n, m, X, Y, blur_pixels=0, angle_degrees=105)

    # Display the main image
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.title(f"Inclined Plane: {n}x{m} pixels,105° angle, 2-pixel blur")
    plt.axis('off')
    plt.tight_layout()
    plt.show()