# FlightSense

# User Manual

# Overview

# Predictions Directory
Do note that the notebooks to train and predict are under "/model_development", the other directories serve to explain the workflow and the whole process of the project to retrieve and process the dataset.  
the Final Meta Model for predicting flight arrival delays is in  
```
model_development/arrival/stacking/stackArrival.ipynb
```

# Note
Do note that every directory will also have a readme to further explain the processes and workflow for each step of the way

# Steps
1) Install all the required packages 
```
pip install >requirements.txt
```   
2) To try out the script to train and evaluate the model to predict flight arrival delay
- navigate to the file directory 
```
model_development/arrival/stacking/stackArrival.ipynb
```

- Run it (do note that catboost do take slightly longer due to the params used for this training process, please re-adjust the params for the training of base models as you see fit)  

3) To try out the script to train and evaluate the model to predict flight departure delay
- navigate to the file directory 
```
model_development/departure/stacking/stacking_3model.ipynb
```

- Run it