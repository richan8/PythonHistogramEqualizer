### MODULES USED: OPENCV (cv2), NUMPY AND MATPLOTLIB
import cv2
import numpy as np
import matplotlib.pyplot as plt

##### HELPER FUNCTION DEFINITIONS

### GENERATES A LIST HISTOGRAMS FOR EACH CHANNEL IN A GIVEN IMAGE
def getHistograms(img):
  channels = img.shape[2]
  hist = np.zeros((channels, 256))

  for channel in range(channels):
    for row in img:
      for pixel in row:
        hist[channel, pixel[channel]] += 1
    
    #plt.plot(hist[channel,:], label = 'Histogram for channel '+str(channel+1))
    #plt.legend(loc='best')
    #plt.show()

  return(hist)

### GENERATES A LIST CUMULATIVE SUM FOR EACH CHANNEL FOR A GIVEN IMAGE HISTOGRAM
def getCumulativeSums(hist):
  channels = len(hist)
  cSum = np.zeros((channels, 256))
  
  for channel in range(channels):
    cSum[channel, 0] = hist[0,0]
    
    for i in range(1, len(hist[channel])):
      cSum[channel, i] = cSum[channel, i-1] + hist[channel, i]
    
    #plt.plot(cSum[channel,:], label = 'Cumulative sum for channel '+str(channel+1))
    #plt.legend(loc='best')
    #plt.show()
  
  return(cSum)

### THE MAIN CODE
### LOADS THE IMAGE FROM THE PROVIDED IMG PATH
### CALLS THE FUNCTIONS TO GENERATE HISTOGRAM AND CUMULATIVE SUM
### USES THE CUMULATIVE SUM TO GET THE CDF
### USES THE CDF AND MAX INTENSITY TO GENERATE THE EQUALIZED IMAGE
### SAVES THE IMAGE IF A SAVE PATH IS PROVIDED
### PLOTS THE ORIGINAL VS RESULTING INTENSITY FREQUENCY DISTRIBUTION 
def equalizeHistogram(imgPath, newImgPath = None):
  img = cv2.imread(imgPath)
  if(img is not None):
    print('Read Image '+ imgPath + ' successfully')
  else:
    print('Image read error.')
    print('Exiting')
    return (None)

  print('Image Shape:', img.shape)
  channels = img.shape[2]
  print('Image Channels:',channels)

  print('Calculating Histogram')
  imgHist = getHistograms(img)

  print('Calculating Cumulative sum')
  imgCSum = getCumulativeSums(imgHist)
  totPixels = sum(imgHist[2])

  ### NORMALIZING UPDATING PIXEL VALUES
  print('Adjusting Image Values')
  Hmin = np.zeros(channels)
  for channel in range(channels):
    for intensity in range(len(imgHist)):
      if (imgHist[channel, intensity] > 0):
        Hmin[channel] = imgCSum[channel, intensity]
        break
    
    for row in img:
      for pixel in row:
        pixel[channel] = 255 * (imgCSum[channel, pixel[channel]] - Hmin[channel]) / (totPixels - Hmin[channel])

  img2Hist = getHistograms(img)
  img2CSum = getCumulativeSums(img2Hist)

  ### SAVING IF PATH IS PROVIDED
  if(newImgPath is not None):
    print('Saving the Image as ', newImgPath)
    if(cv2.imwrite(newImgPath, img)):
      print('Saved Successfully')
    else:
      print('Error Saving the image\nSkipping this step.')
  else:
    print('Skipping the saving step because new path was not defined')

  ### PLOTTING
  print('Plotting the Intensity\'s Frequency distribution graphs for the original vs. Adjusted Image')
  fig, axs = plt.subplots(2, channels)
  RGBAColors = ['Red', 'Green', 'Blue', 'Alpha']
  for channel in range(channels):
    x1, y1 = [x for x in range(len(imgHist[channel]))], imgHist[channel] / totPixels
    x2, y2 = x1, img2Hist[channel] / totPixels

    color = 'black'
    channelName = str(channel)
    if((channels == 3) or (channels == 4)):
      color = RGBAColors[channel]
      channelName = RGBAColors[channel]

    axs[0, channel].set(xlabel = 'Intensity', ylabel = 'Frequency', title = 'Original Channel ' + channelName)
    axs[1, channel].set(xlabel = 'Intensity', ylabel = 'Frequency', title = 'Adjusted Channel ' + channelName)

    axs[0, channel].bar(x1, y1)
    axs[1, channel].bar(x2, y2)

  print('Image histogram of ' + imgPath +' successfully equalized')
  plt.show()
  return(img)

##### END OF FUNCTION DEFINITIONS

print('\nImage Equalizer program')
print('CV - Assignment 1')
print('Made by Richanshu Jha - rj1469 \n')

### THE DRIVER FUNCTION IS INITIALIZED HERE
### IT TAKES THE PARAMETERS:
###   INPUT FILE PATH
###   OUTPUT FILE PATH. CAN BE SET TO NONE IF WE DONT WANT TO SAVE.
newImg = equalizeHistogram('crowd.png', 'crowdEqualized.png')

if(newImg is not None):
  print('Program complete, Input any key to exit')
  input()
else:
  print('Error, Input any key to exit')
  input()