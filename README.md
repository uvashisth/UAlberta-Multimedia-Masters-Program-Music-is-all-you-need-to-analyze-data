# Music is all you need to Analyze Data
## Sonification using Deep Learning Techniques
### Sonification using LSTM
__________________________________________________________________________________
Sonification is a technique of using non-speech audio to convey information or perceptualize data. It helps the listeners distinguish between the enormous amount of data and the relations between the different sets of values. Auditory perception has various parameters like amplitude, spatial, temporal and frequency resolution, which can be used as an alternative or complement to the existing visualization techniques. <br /> <br />
This repository contains the code and data used in our final project for MM811 Multimedia Topic I: AI in Multimedia. Our goal was to generate music which will follow the data which we have analyze from any time series dataset. 

### Project
_______________________________________________________________________________________________
This is PyTorch based project intended to analyze data using music.
<br />
Prerequisites
```
python==3.6
torch==1.3.0
torchvision==0.4.1
```
Install requirements.txt using the following command
```
pip install -r requirements.txt
```

#### Dataset
____________________________________________________________________________________________________
We are using a public Dataset which comprises of two different dataset. 
* Clementi Dataset - This dataset consists of 17 different songs of piano Dataset
* Piano Dataset - This dataset consists of 300 different songs

#### Overall Architecture Flow

![Overall Architecture Flow](https://drive.google.com/uc?export=view&id=1r8Q4BxBVWeJIikNY0nHMtKuhPM-sJnzj)

#### Data Influencing Technique
![Data Influencing Technique](https://drive.google.com/uc?export=view&id=1pwKrffEWWBPp2HBze9y8z3FZobtoa22J)

To know more about the architecture flow and data influencing technique please refer to the Report in the repository



### License
Distributed under the MIT License. See LICENSE for more information.























---------------------------------------------------------------------------------------
Pitch Based Approach
In this approach we have considered only the pitch values from notes of the dataset. 

#### Model
_________________________________________________________
***Training:***
<br />
We have used RNN-based Stacked-LSTM Model for predicting the next pitch value which will be generated based on the previous data which is given as an input from our training music dataset. The range of input data is 0 to 127 values which is normalized between 0 to 1.
<br />
***Testing:***
<br />
We normalize the data and scale it down to a range of 0 to 1 and feed it as an input to our existing set of validation set.
The LSTM Model is shown below:
![LSTM Model](https://drive.google.com/uc?export=view&id=1AmVkuvmzPfgPjwATq5_gxdo48YJGWwMs)
We have used two layered stacked LSTM where our hidden layers are 38 and 256 respectively.

#### Training 
You could either use pretrained weight files or train your own piano dataset.
To Train your own dataset place your data in the dataset folder and make changes in preprocessing.py file and run the model file to get the weights based on your dataset
For Training run following files
```
python 
```
#### Testing
Since our testing data is independent from our training dataset you can give any time-series dataset normalize the dataset based on postprocessing_normalize file and give it as an input to the music generation file.

For testing run the following files
```
python
```




------------------------------------------------
Temporal Based Approach
The music generated by the pitch based approach is distinguishable and soothing to ears but it considered only the pitch from the music. To enhance the model we created a new Input Vector of 98 as shown below:
<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1IuNHPJ71zlU2S8__4Y7B2Y7epm8bLYzH">

  </p>
<br />

where 0th bit considers the normalized pitch value(0-1) of the note which is played <br />
&nbsp; &nbsp; &nbsp; &nbsp; 1st to 16th bits are the duration bins from 0 to 4 seconds with each bin of 2.5 milliseconds and is one hot encoded <br />
&nbsp; &nbsp; &nbsp; &nbsp; 17th to 96th bits are the start time bins which are remainder when divided by 20 seconds so in all there are 80 bins with each bin of 2.5 milliseconds and is one hot encoded <br />
&nbsp; &nbsp; &nbsp; &nbsp; 97th bit is the normalized velocity or the volume(0-1) of the note <br />


#### Model
_________________________________________________________
***Training:***
<br />
We have used RNN-based Stacked-LSTM Model for predicting the next vector value which will be generated based on the previous data which is given as an input from our training music dataset. The input data is a 98-dimensional ector which has all values between 0 to 1.
<br />
***Testing:***
<br />
We normalize the data and scale it down to a range of 0 to 1 and feed it as an input to our existing set of validation set.
The LSTM Model is shown below:
![LSTM Model](https://drive.google.com/uc?export=view&id=1MKNLoMKiiqwwoCd8bGmeHBwjm4VhCkpR)
We have used two layered stacked LSTM where our hidden layers are 256 and 256 respectively.

#### Training 
You could either use pretrained weight files or train your own piano dataset.
To Train your own dataset place your data in the dataset folder and make changes in preprocessing.py file and run the model file to get the weights based on your dataset
For Training run following files
```
python 
```
#### Testing
Since our testing data is independent from our training dataset you can give any time-series dataset normalize the dataset based on postprocessing_normalize file and give it as an input to the music generation file.
