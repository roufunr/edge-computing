import cv2
import os

# Load the original image
original_image = cv2.imread('images/test_1.jpg')
scaling_factor = 0.1
# List of interpolation algorithms
interpolation_methods = {
    'INTER_NEAREST': cv2.INTER_NEAREST,
    'INTER_LINEAR': cv2.INTER_LINEAR,
    'INTER_CUBIC': cv2.INTER_CUBIC,
    'INTER_AREA': cv2.INTER_AREA,
    'INTER_LANCZOS4': cv2.INTER_LANCZOS4
}

# Create a directory to save the results
if not os.path.exists('images/results'):
    os.makedirs('images/results')

# Downscale and upscale for each interpolation method
for method_name, method in interpolation_methods.items():
    # Downscale
    downscaled_image = cv2.resize(original_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=method)
    downscale_filename = f'images/results/test_1_{method_name}.jpg'
    cv2.imwrite(downscale_filename, downscaled_image)
    downscale_size_mb = os.path.getsize(downscale_filename) / (1024 * 1024)
    
    # Upscale
    #upscaled_image = cv2.resize(downscaled_image, (original_image.shape[1], original_image.shape[0]), interpolation=method)
    upscaled_image = cv2.resize(downscaled_image, None, fx=1/scaling_factor, fy=1/scaling_factor, interpolation=method)
    upscale_filename = f'images/results/test_1_{method_name}_upscaled.jpg'
    cv2.imwrite(upscale_filename, upscaled_image)
    upscale_size_mb = os.path.getsize(upscale_filename) / (1024 * 1024)
    
    # Display image sizes in MB
    print(f'{method_name} - Downscale Image Size: {downscale_size_mb:.2f} MB')
    print(f'{method_name} - Upscale Image Size: {upscale_size_mb:.2f} MB')
    print('-----------------------------')

print('Processing complete.')