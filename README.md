# Object detection as a concept for automated football statistics

## Overview 

The project aims to determine a football player with possession of the ball using computer vision. Use cases for this include automatic possession statistics and potentially automatically obtaining xG (expected goals) statistics if we can capture when a short is taken by a player. The project uses a pretrained [yolov5](https://github.com/ultralytics/yolov5) model to identiy players and then draw a bounding box around the player with the ball.

![Example output from gradio](https://github.com/SitwalaM/object_detection_football/blob/main/images/example4.PNG)

## Data Source 

The data source for the project was obtained by scraping google image results in a browser console using a tutorial which can be found [here](https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/). A script was then created to clean the url lists, remove duplicates then download the to a folder. [Link to data_download script] (https://github.com/SitwalaM/object_detection_football/blob/main/scripts/get_data.py). The dataset is used merely to test the algorithm and not train it. Better results can be obtained by proving ground truth data which will help with calibrating out problematic scenarios like fans in the background and players in background who seem to be near to the ball in a 2-D perspective. Several annotating softwares are available that produce label formats that are accepted by common object detection algorithms

## Deployment and Use

The demo pipeline can be fully run in the [notebook](https://github.com/SitwalaM/object_detection_football/blob/main/notebooks/ball_possession.ipynb) provided which can run on Colab. To use the data download script

```bash
  pip install -r requirements.txt 
```

Edit the file name inputs in the script as required.

The algorithm is tested using [gradio](https://gradio.app/). It takes an input image and outputs an image with the bounding box. The following functions are used to input the image into the model:

```bash
def predict(image):
  # main prediction function that gets image and returns pandas dataframe

  results = model(image, size=640)  
  return results.pandas().xyxy[0] 
  
def processed(image):
  #inputs the image and draws the bounding box on closest player

  results = predict(image)
  results = calculate_centres(results)
  processed = calculate_distance(results)
  processed = get_second_largest(processed)
  box = draw_possession(processed,image)

  return box
```

### Gradio GUI

```bash
iface = gr.Interface(fn = processed, inputs = "image", 
             outputs = "image",
             capture_session = True, 
             title="Who Has the Ball?")
             
iface.launch(debug = False)

```

## Proximity Calculation

# Approach 1 - Simple Bounding Box Distance from Centre

The simplest baseline approach was used to come up with a working pipeline for the model. As can be seen from the image below, several problems could arise from such an approach. Some players in the background or even fans can seem to be closest to the ball. Sizes of bounding boxes due to player's arms for example can give a wrong outcome for proximity as only the centroid is being used. However, it's a good start point to tune the class detection itself and explore other ways of solving the problem. 

![player proximity calculation](https://github.com/SitwalaM/object_detection_football/blob/main/images/calculations.svg)

# Approach 2 - Two Stage Inference

YOLOv5 have a built-in function that crops images using detected bounding boxes.  The second approach leverages this function and makes predicitions twice. The first inference crops images and stores them in folder by class. In this case, person and sports ball. The second inference is restricted to the images with person and is set up to detect sports ball only. If the ball is in proximity to a player, one image will be selected. This method poses similar issues concerning the proximity of other players during a tackle for example.
![Two stage inference](https://github.com/SitwalaM/object_detection_football/blob/main/images/ausie7.jpg)

## Conclusions

* Baseline pipeline that could potentially be developed for automatic statistics collection has been demonstrated
* Ground truth training data would help calibrate out false proximities like backrground players and fans in the crowd
* With availability of open-source pre-trained models, interesting use cases as the one shows here can be developed to help us in our daily life


## Acknowledgements/ References

1. [Load YOLOv5 from PyTorch Hub](https://github.com/ultralytics/yolov5/issues/36)
2. [JS script for google search Query](https://www.pyimagesearch.com/2017/12/04/how-to-create-a-deep-learning-dataset-using-google-images/)

## Authors
1. [Sitwala Mundia](https://github.com/SitwalaM)
2. [Rhodasi Mwale](https://github.com/DhasiM)





