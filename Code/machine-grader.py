# -*- coding: utf-8 -*-
"""
This Program compares 2 files and provide accuracy
"""
import argparse

# Open 2 files
def open_file(filename):
    ans_list = []
    with open(filename) as file:
        for line in file:
            line = line.rstrip()
            ans_list.append(line.split('\t'))

    return ans_list

# Find the accuracy
def accuracy(correct,predict):
    corr = 0
    for i in range (len(correct)):
        for j in range(0,4):
            if(correct[i][j] == predict[i][j]):
                corr = corr +1
    size = len(correct)*4
    
    print("Accuracy= ",(corr/size))
    f.write("Accuracy = ")
    f.write(str(corr/size))
    f.write('\n')

    # Write in expected format
    for i in range (len(correct)):
        incorrect = 0
        
        f.write(str(correct[i]))
        f.write('|')
        f.write(str(predict[i]))
        f.write('|')
        for j in range(0,4):
            
            
            if(correct[i][j] != predict[i][j]):
                incorrect = incorrect + 1
        f.write(str(incorrect))   
        f.write('\n')              
        
                
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Machine Reading Comprehension') # This is the description
    parser.add_argument('Predict', type = str,help='The name of the Predicted file') # Input File selection
    parser.add_argument('Correct', type = str,help='The name of the gold answe file')
    parser.add_argument('OutputFile', type = str,help='The name of the output file')
    args = parser.parse_args()
    if  args.Predict and args.Correct and args.OutputFile:
        
        predict_file = args.Predict
        correct_file = args.Correct
        outputFile = args.OutputFile
        
        correct = open_file(predict_file)
        predict = open_file(correct_file)  
        
        f = open(outputFile,'w')
        accuracy(correct,predict)
        f.close()
    
    