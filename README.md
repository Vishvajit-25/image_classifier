# image_classifier

This is the Python Flask Application which helps us to check whether the Entered Website is ISO certified . 

The Model Used of making prediction is trained seperately with the training dataset of 2000 images which is a small dataset yet the Accuracy of model is near to 90% . 

The Application goes through all the associated links of homepage and collect all those links . 

It goes through all those links and collect images from those sites and starts checking image by image . 
If the image is Classifies ISO certified by the Model than the Ouput will be ISO certified. 
If the none of the images are classified as ISO certified by the model than the Output will be NON ISO certified. 
If the Application has elapsed the time specified by the user then it will display TIMEOUT . 

Installtion :
Just make a Pull resquest and get all the files in your working directory . 

Setup :
There are absolute paths mentioned inside the script.py just make changes to those and you are ready to go . 

