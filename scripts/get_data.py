
#import librariries


import requests
import os
import urllib
import urllib.request
from os import walk

# list the urls in the text files that were saved from the google search


files = [1,2]

lines = []
for file in files:
  document = "./data/urls_{}.txt".format(file)
  with open(document) as f:
    for line in f:
      lines.append(line.strip().split("\n"))


# flatten list

flat_list = [item for sublist in lines for item in sublist]
final_urls = set(flat_list)

# download the images

counter = 0

for url in final_urls:
  try:
    urllib.request.urlretrieve(url, "./data/image_{}.jpg".format(counter))
    counter += 1
  except:
    counter += 1


filenames = next(walk("./images"), (None, None, []))[2]  # [] if no file

# can be used to check the list of paths
paths = []
for file in filenames:
  paths.append("../data/" + str(file))




