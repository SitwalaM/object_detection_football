# Object detection as a concept for automated football statistics

## Overview 

The project aim is to determine a football player with possession of the ball using computer vision. Use cases for this include automatic possession statistics and potentially automatically obtaining xG (expected goals) statistics if we can capture when a short is taken by a player. The project uses a pretrained yolov5 model to identiy players and then draw a bounding box around the player with the ball

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

### Gadio GUI

```bash
iface = gr.Interface(fn = processed, inputs = "image", 
             outputs = "image",
             capture_session = True, 
             title="Who Has the Ball?")
             
iface.launch(debug = False)

```

## Proximity Calculation

# Approach 1 - Simple Bounding Box Distance from Centre

![player proximity calculation](https://github.com/SitwalaM/object_detection_football/blob/main/images/calculations.svg)


