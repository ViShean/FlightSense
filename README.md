# FlightSense

## User Manual

### Overview
FlightSense is a project aimed at predicting flight delays, specifically focusing on arrival and departure delays. The project follows a step-by-step workflow to retrieve, process, and model flight data for accurate delay predictions.  

### Predictions Directory
Do note that the notebooks to train and predict are under `/model_development`, the other directories serve to explain the workflow and the whole process of the project to retrieve and process the dataset.  
the Final Meta Model for predicting flight arrival delays is in  
```
model_development/arrival/stacking/stackArrival.ipynb
```

### Note
Do note that every directory will also have a readme to further explain the processes and workflow for each step of the way

### Steps
1) Install all the required packages 
```
pip install >requirements.txt
```   
2) To try out the script to train and evaluate the model to predict **flight arrival delay**
- navigate to the file directory 
```
model_development/arrival/stacking/stackArrival.ipynb
```

- Run it (do note that catboost do take slightly longer due to the params used for this training process, please re-adjust the params for the training of base models as you see fit)  

3) To try out the script to train and evaluate the model to predict **flight departure delay**
- navigate to the file directory 
```
model_development/departure/stacking/stacking_3model.ipynb
```

- Run it



### Video Introduction
[![FlightSense Project Introduction](https://img.youtube.com/vi/uuWvW7OKyXA/0.jpg)](https://www.youtube.com/watch?v=uuWvW7OKyXA)