#Standard library modules
import glob
import sys
import os
import logging
from fnmatch import fnmatch
from collections import Counter
import csv

#Third Party imports
from music21 import *
import numpy as np
import torch 
from sklearn import preprocessing
from matplotlib import pyplot as plt
import pandas as pd

#Local Modules
from util.midi_class_mapping import MidiClassMapping
from util.midi_notes_mapping import MidiNotesMapping


class PreprocessingTrainingData():
    """
    This class is created to preprocess the training data and return the input, output and min and max midi values which will be required for training
    """
    def __init__(self,sequence_length=50):
        self.sequence_length=sequence_length

    #Create a Logging File
    logging.basicConfig(filename="test.log", level=logging.DEBUG)
    """
    This function is to extract the notes from the midi file 
    Input Parameters: Absolute File path of the midi file
    Output Parameters: List of notes 
    """
    def extract_notes(self,file_path):
        #Intializing empty set
        notes = {}
        #Check if the input path is a file or not
        notes = self.get_notes(file_path)
        #Return the list of notes
        return notes
    
    """
    This function is to read midi file and get notes
    Input Parameters:Absolute File path of the midi file
    Output Parameters:List of notes 
    """
    def get_notes(self,filename):
        #Read the midi file
        midi = converter.parse(filename)
        notes_i = []
        notes_to_parse = None
        #Logging file
        logging.debug("File that is being parsed currently is {}".format(filename))
        
        try: 
            # Extracting the instrument parts
            notes_to_parse = midi[0].recurse()
        
        except: 
            # Extracting the notes in a flat structure
            notes_to_parse = midi.flat.notes
        #Iterate through each and every element in the notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                # Taking the note
                notes_i.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                # Taking the note with the highest octave.
                notes_i.append(str(element.pitches[-1])) 
        return notes_i
    
    """
    This function to calculate the count of unique number of notes
    Input Parameters: List of all notes from file
    Output Parameters: Number of unique number of notes
    """
    def number_of_output_notes_generated(self,notes):
        #Convert 2D list into 1D list
        all_notes=[]
        #Iterate through the 2D list
        for item in notes:
            all_notes.extend(item)
        #Number of unique notes
        number_of_output_notes=len(set(all_notes))
        return number_of_output_notes
    """
    This function is to normalize data 
    Input Parameters: List of input values
    Output Parameters: List of normalized data
    """
    def normalize_data(self,list_of_input_values,min_value,max_value):
        
        #Normalize each value of the list
        for i in range(len(list_of_input_values)):
            list_of_input_values[i]=(list_of_input_values[i]-min_value)/(max_value-min_value)
        return list_of_input_values

    def bakchodi(self, network_input,network_output):
        # print(network_input)
        # print(network_output)
        network_input=np.asarray(network_input)
        network_output=np.asarray(network_output)
        SIZE = 10000
        input_length = 50

        X_orig = network_input
        Y_orig = network_output
        all_notes = np.unique(X_orig)
        count_notes_X = np.zeros(128)
        count_notes_Y = np.zeros(128)
            
        notes_in_set = 0
        index = 0
        new_set_X = []
        new_set_Y = []
        x = np.zeros(input_length)
        while (notes_in_set < SIZE and index < len(X_orig)):
            x = np.copy(X_orig[index].astype(int)) 
            y = np.copy(Y_orig[index].astype(int))
            norm_count_notes_x = np.mean(count_notes_X[x] / (np.mean(count_notes_X) + 500))
            norm_count_notes_y = count_notes_Y[y] / (np.mean(count_notes_Y) + 50)
            if norm_count_notes_x < 1:
                new_set_X.append(np.copy(X_orig[index]))
                new_set_Y.append(np.copy(Y_orig[index]))
                count_notes_X[x] += 1
                count_notes_Y[y] += 1
                notes_in_set += 1
            elif norm_count_notes_y < 1:
                new_set_X.append(np.copy(X_orig[index]))
                new_set_Y.append(np.copy(Y_orig[index]))
                count_notes_X[x] += 1
                count_notes_Y[y] += 1
                notes_in_set += 1
            index += 1    
            
        X = np.array(new_set_X)
        Y = np.array(new_set_Y)

        sorted_notes = np.unique(Y)
        max_note = np.max(Y)
        min_note = np.min(Y)
        
        return X,Y


    """
    This function is to generate training data i.e model input,output,max value,min value
    Input Parameters: Set of input notes read from midi files
    Output Parameters: Network Input,Network Output, Max midi Value,Min midi value
    """
    def generate_training_data(self,notes):
        
        #Generate a flat list of input notes
        notes_from_training_data = []
        
        for item in notes:
            notes_from_training_data.extend(item)
        # get all right hand note names
        right_hand_notes = sorted(set(item for item in notes_from_training_data))
        #Get note to midi number mapping
        note_to_midi_number_mapping=MidiNotesMapping().get_midi_number_notes_mapping("A.txt")
        #Get maximum and minimum midi number values
        note_to_int,int_to_note,max_midi_value,min_midi_value=MidiClassMapping().midi_notes_to_class_mapping(right_hand_notes,note_to_midi_number_mapping)
        
        
        network_input = []
        network_output = []
        for song in notes:
            for i in range(0, len(song) - self.sequence_length, 1):                
                sequence_in = song[i:i + self.sequence_length]           
                sequence_out = song[i + self.sequence_length]
                for notes in range(len(sequence_in)):
                    for key,value in note_to_midi_number_mapping.items():
                        if  str(sequence_in[notes]) in value:
                            sequence_in[notes]=key
                
                for key,value in note_to_midi_number_mapping.items():
                    if  str(sequence_out) in value:
                        sequence_out=key    
                network_input.append(sequence_in)
                network_output.append(int(sequence_out) )
        #Check if length of input and output is same
        assert len(network_input) == len(network_output), len(network_input)
        
        #Trial function 
        network_input,network_output=self.bakchodi(network_input,network_output)
        
        network_input=list(network_input)
        network_output=list(network_output)

        #Number of input batches
        n_patterns = len(network_input)
        #Normalize the input data


        for i in range(len(network_input)):  
            network_input[i]=self.normalize_data(list(network_input[i]),min_midi_value,max_midi_value) 
        
        
        #Converting the output data in range of 0-37
        for i in range(len(network_output)):
            network_output[i]=note_to_int[network_output[i]]
        #Converting 2d list to 2d numpy array
        network_input=np.array(network_input)
        #Reshaping the 2d numpy array to 3d array
        network_input = np.reshape(network_input, (n_patterns, self.sequence_length, 1))        
        return (network_input, network_output,max_midi_value,min_midi_value,int_to_note)
    """
    This is the main function which has to be called it acts like a wrapper function
    Input Parameters:
    Output Parameters:
    """
    def preprocess_notes(self,path):
        pattern = "*.mid"
        notes=[]
        if not path.endswith(".mid"):
            for path, subdirs, files in os.walk(path):
                for name in files:
                    if fnmatch(name, pattern):
                        notes.append(self.extract_notes(os.path.join(path, name)))
        else:        
            notes.append(self.extract_notes(path))
        number_of_output_notes=self.number_of_output_notes_generated(notes)
        network_input,network_output,max_midi_number,min_midi_number,int_to_note=self.generate_training_data(notes)
        for i in range(len(network_input)):
            for j in range(len(network_input[i])):
                temp=[]
                
                temp.append((network_input[i][j]))
                network_input[i][j]=temp
        network_input = np.asarray(network_input,dtype=np.float32)
        network_input=torch.tensor(network_input)
        network_output=torch.tensor(network_output)

        return network_input,network_output,max_midi_number,min_midi_number,int_to_note


if __name__=="__main__":
    network_input,network_output,max_midi_number,min_midi_number,int_to_note=PreprocessingTrainingData().preprocess_notes("D:\\Prem\\Sem1\\MM in AI\\Project\\Project\\Sonification-using-Deep-Learning\\CombinedData")
    print(max_midi_number)
    print(min_midi_number)
    print(int_to_note)
    network_input=network_input.cpu().numpy().tolist()
    network_output=network_output.cpu().numpy().tolist()
    
    final_array=[]
    for i in range(len(network_input)):
        temp=[]
        for j in range(len(network_input[i])):
            temp.extend(network_input[i][j])
        final_array.append(temp)
    
    df=pd.DataFrame(final_array)
    df.to_csv('network_input.csv', index=False, header=False)

    df=pd.DataFrame(network_output)
    df.to_csv('network_output.csv', index=False, header=False)
    # temp=[]
    # for i in range(len(network_input)):
    #     for j in range(len(network_input[i])):
    #         temp.extend(network_input[i][j])
    # temp=sorted(temp)
    # network_output=sorted(network_output)
    # print(Counter(temp))
    # print(Counter(network_output))
    # labels, values = zip(*Counter(network_output).items())
    # indexes = np.arange(len(labels))
    # width = 1

    # plt.bar(indexes, values, width)
    # plt.xticks(indexes + width * 0.5, labels)
    # plt.show()
    # labels, values = zip(*Counter(temp).items())
    # indexes = np.arange(len(labels))
    # width = 1

    # plt.bar(indexes, values, width)
    # plt.xticks(indexes + width * 0.5, labels)
    # plt.show()