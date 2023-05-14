# Project Image Filtering and Hybrid Images Stencil Code
# Based on previous and current work
# by James Hays for CSCI 1430 @ Brown and
# CS 4495/6476 @ Georgia Tech
import numpy as np
from numpy import pi, exp, sqrt
from skimage import io, img_as_ubyte, img_as_float32
from skimage.transform import rescale


def my_imfilter(image: np.ndarray, filter: np.ndarray):
  """
Your function should meet the requirements laid out on the project webpage.
Apply a filter to an image. Return the filtered image.
Inputs:
- image -> numpy nd-array of dim (m, n, c) for RGB images or numpy nd-array of dim (m, n) for gray scale images
- filter -> numpy nd-array of odd dim (k, l)
Returns
- filtered_image -> numpy nd-array of dim (m, n, c) or numpy nd-array of dim (m, n)
Errors if:
- filter has any even dimension -> raise an Exception with a suitable error message.
  """
  ##################
  # Your code here #
  #Checking if the image is colored or gray scale
  if (image.ndim == 3):
    r1, c1, ch = image.shape #get the dimensions of the image
    r2, c2 = filter.shape #get the dimensions of the filter
    if (r2 == c2 & r2 % 2 == 0): #Check the even filter
     print("The output is undefined, please make sure that the filter is not even")
    r = r1 + r2 - 1 #the dimension after padding
    c = c1 + c2 - 1
    imagepad = np.zeros((r, c, ch)) #create the temp to pad the image
    # put image in middle
    # loop on the channels and set the values of the image in the middle
    for i in range(ch):
      channel = image[:, :, i]
      imagepad[(r2 // 2):-(r2 // 2), (c2 // 2):-(c2 // 2), i] = channel #accessing the mid values
    filtered_image = np.zeros((r, c, ch)) # temp for the output image

    # filtered_image = np.fft.irfft2(np.fft.rfft2(x) * np.fft.rfft2(y, x.shape))
    #loop on the cahnnels
    for ch in range(3):
      #loop on the rows
      for i in range(r1):
        #loop on the columns
        for j in range(c1):
          #multiply the filter with crosponding value in the padded image, then sum
          # these values to set the value of the pixel in the new image
          filtered_image[i, j, ch] = (filter * imagepad[i:i + r2, j:j + c2, ch]).sum()
      # filtered_image = cv2.resize(filtered_image, (r1, c1))
    filtered_image = filtered_image[0:r1, 0:c1, :]
  else:
    # for gray scale image
    # same as the colored image but excluding the loops for the color channels
    r1, c1 = image.shape
    r2, c2 = filter.shape
    if (r2 == c2 & r2 % 2 == 0):
      print("The output is undefined, please make sure that the filter is not even")

    r = r1 + r2 - 1
    c = c1 + c2 - 1
    imagepad = np.zeros((r, c))
    # put image in middle
    imagepad[(r2 // 2):-(r2 // 2), (c2 // 2):-(c2 // 2)] = image
    filtered_image = np.zeros((r, c))

    # filtered_image = np.fft.irfft2(np.fft.rfft2(x) * np.fft.rfft2(y, x.shape))
    for i in range(r1):
      for j in range(c1):
        filtered_image[i, j] = (filter * imagepad[i:i + r2, j:j + c2]).sum()
      # filtered_image = cv2.resize(filtered_image, (r1, c1))
    filtered_image = filtered_image[0:r1, 0:c1]
    print(filtered_image.shape)
  return filtered_image

##################

def gaussian_filter(side_length, sigma):
    # side length represent the length of the kernerl assuming square kernel.
    ax = np.linspace(-(side_length - 1) / 2., (side_length- 1) / 2., side_length)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))

    return kernel / np.sum(kernel)



def gen_hybrid_image(image1: np.ndarray, image2: np.ndarray, cutoff_frequency: float):
  """
   Inputs:
   - image1 -> The image from which to take the low frequencies.
   - image2 -> The image from which to take the high frequencies.
   - cutoff_frequency -> The standard deviation, in pixels, of the Gaussian
                         blur that will remove high frequencies.

   Task:
   - Use my_imfilter to create 'low_frequencies' and 'high_frequencies'.
   - Combine them to create 'hybrid_image'.
  """

  assert image1.shape == image2.shape

  # Steps:
  # (1) Remove the high frequencies from image1 by blurring it. The amount of
  #     blur that works best will vary with different image pairs
  # generate a gaussian kernel with mean=0 and sigma = cutoff_frequency,
  # Just a heads up but think how you can generate 2D gaussian kernel from 1D gaussian kernel
  kernel = gaussian_filter(27, cutoff_frequency) #using the gaussian filter with side length = 27
  
  # Your code here:
  low_frequencies = my_imfilter(image1, kernel) #blur image 1

  # (2) Remove the low frequencies from image2. The easiest way to do this is to
  #     subtract a blurred version of image2 from the original version of image2.
  #     This will give you an image centered at zero with negative values.
  # Your code here #
  high_frequencies = image2 - my_imfilter(image2, kernel)

  # (3) Combine the high frequencies and low frequencies
  # Your code here #
  hybrid_image = high_frequencies + low_frequencies


  # (4) At this point, you need to be aware that values larger than 1.0
  # or less than 0.0 may cause issues in the functions in Python for saving
  # images to disk. These are called in proj1_part2 after the call to 
  # gen_hybrid_image().
  # One option is to clip (also called clamp) all values below 0.0 to 0.0, 
  # and all values larger than 1.0 to 1.0.
  # (5) As a good software development practice you may add some checks (assertions) for the shapes
  # and ranges of your results. This can be performed as test for the code during development or even
  # at production!

  return low_frequencies, high_frequencies, hybrid_image

def vis_hybrid_image(hybrid_image: np.ndarray):
  """
  Visualize a hybrid image by progressively downsampling the image and
  concatenating all of the images together.
  """
  scales = 5
  scale_factor = 0.5
  padding = 5
  original_height = hybrid_image.shape[0]
  num_colors = 1 if hybrid_image.ndim == 2 else 3

  output = np.copy(hybrid_image)
  cur_image = np.copy(hybrid_image)
  for scale in range(2, scales+1):
    # add padding
    output = np.hstack((output, np.ones((original_height, padding, num_colors),
                                        dtype=np.float32)))
    # downsample image
    cur_image = rescale(cur_image, scale_factor, mode='reflect', channel_axis=2)
    # pad the top to append to the output
    pad = np.ones((original_height-cur_image.shape[0], cur_image.shape[1],
                   num_colors), dtype=np.float32)
    tmp = np.vstack((pad, cur_image))
    output = np.hstack((output, tmp))
  return output

def load_image(path):
  return img_as_float32(io.imread(path))

def save_image(path, im):
  return io.imsave(path, img_as_ubyte(im.copy()))
