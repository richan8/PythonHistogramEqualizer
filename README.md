# PythonHistogramEqualizer
A python application that equalizes image histograms to increase image clarity

Histogram Equalization is a method of image processing where the intensity values of the pixels are adjusted so that the contrast of the image is increased. For this assignment, I have generalized the code to allow the equalization of histograms for images with multiple channels. The below procedure is an explanation of how it works on a single channel i.e. for a Grey scale image (As is required by the homework instructions). The same implementation is performed independently on the other channels to generate an equalized multi-channel output.

## Results

![Example 1](https://github.com/richan8/PythonHistogramEqualizer/blob/main/imgs/1.png)![Example 1 Equalized](https://github.com/richan8/PythonHistogramEqualizer/blob/main/imgs/1eq.png)

## How it works

The procedure for equalizing the histogram of an Image involves finding out the frequency of all intensities in the image. It uses this to create a cumulative sum. This alongside the frequency of the least intensity pixel is used to stretch out the intensity range of the most frequent intensity values. Since the stretched out histogram has more number of pixels cover a broader range of intensity values, the equalization results in a clearer image with higher contrast. The process of equalizing the histogram of the intensities of an image is given below.

The first step is creating the histogram of the original image Where x is the Intensity level and ni is the frequency of that intensity across the image
