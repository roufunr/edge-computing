1. MSE (Mean Squared Error):
   -------------------------
	MSE measures the average of the squared differences between corresponding pixel values in two images.
	It provides a quantitative measure of the average squared difference between the original and processed images.
	Lower MSE values indicate higher similarity between the images, but it may not always align with human perception.

2. PSNR (Peak Signal-to-Noise Ratio):
   ----------------------------------

	PSNR quantifies the ratio between the maximum possible pixel value and the noise introduced during image processing.
	It's a logarithmic measure that represents the peak amplitude of the signal compared to the amplitude of noise.
	Higher PSNR values are indicative of better image quality, but it may not fully capture perceptual differences.

3. MAE (Mean Absolute Error):
   -------------------------
	MAE computes the average absolute difference between corresponding pixel values in two images.
	It provides a measure of the average magnitude of the differences without considering the direction (positive/negative) of the errors.
	Like MSE, lower MAE values suggest higher image similarity, but it's sensitive to outliers.
