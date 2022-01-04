# -*- coding: utf-8 -*-
"""
Program Name: Tag You're It!
Author: Rupak Kumar Das
Course: CS 5242
Date: 11/08/21

Program Details: This is a reading comprehension test that consists of multiple choice 
questions based on a short story. 

Code Usage: The user should follow below format in a commandline
    python machine-reader.py 0/1 mc500.(dev/test).tsv (dev/test).(0/1).txt
    python machine-grader.py (dev/test).(0/1).txt mc500.(dev/test).ans (dev/test).(0/1).graded.txt
        where,
            0/1 is mode. 0 is baseline and 1 is enhanced version
            mc500.(dev/test).tsv, file contains question
            (dev/test).(0/1).txt, file contains predicted answer
            mc500.(dev/test).ans, file contains actual answer 
            (dev/test).(0/1).graded.txt, provide the accuracy

Program Algorithm (Reader):
    1) Mode 0:
        1.1) for every question
            1.1.1) preprocess the question, story and answer
            1.1.2) for every option 
                1.1.2.1) preprocess the question, story and answer
                1.1.2.2) make a sliding window. size = length of question + length of option
                1.1.2.3) pass through the story and find overlap
                1.1.2.4)find max number of overlap for each option
            1.1.3) find the max overlap for all of those options. The option with max operlap is the answer.
    2) Mode 1:
        2.1) for every question
            2.1.1) preprocess the question, story and answer
            2.1.2) for every option 
                2.1.1.1) make a sliding window. size = length of question + length of option
                2.1.1.2) pass through the story and find overlap
                2.1.1.3)find max number of overlap for each option
            1.1.3) find the max overlap for all of those options. 
                1.1.3.1) If there is only one option with maximum overlap, that option is answer
                1.1.3.2) else(more than one option with maximum overlap) use enhanced ruled-based approach
                1.1.3.3) if doesn't match with any rule-based approach then choose one option randomly with max overlap(not from all options)
   
"""
#import libraries
import argparse
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('averaged_perceptron_tagger')
import re
import random

# This function  
def getdata(mode,input_file):
    with open(input_file,'r') as trainfile:
        for passage in trainfile:
            line = passage.split("\t")
            passage = line[2] # This is the story
                        
            answer_list = []
            # 2.1) for every question
            for i in range (3,23,5): # # This is the questions  iteration             
                question = line[i]
                question = re.sub('one:','',question) # removing 'one:'
                question = re.sub('multiple:','',question) # removing 'multiple:'
                option = line[i+1],line[i+2],line[i+3],line[i+4] # all possible answer               
                option = "\t".join(option) # make a string with all option separated by tab
                ans = overlap(passage, question,option,mode) # This function is to find the answer
                answer_list.append(ans)
                            
            for value in answer_list: # Write the predicted answer
                f.write(value)
                f.write('\t')                
            f.write('\n')         

# This function processes the options                             
def option_process(text):
    #text = text.lower() # lowercase
    text = re.sub(r'[^\w\s]', '', text) # remove punctuation
    stop_words = stopwords.words('english') # to remove stopwords
    porter = PorterStemmer() # to stemming the words
    
    option_token = []
    for word in text.split('\t'): 
        tokenized = word_tokenize(word) # Tokenize the option
        filtered_words = tokenized
        #filtered_words = [word for word in tokenized if word not in stop_words]
        stemmed = [porter.stem(word) for word in filtered_words] # stemming
        option_token.append(stemmed)
        
    return option_token # return option as token
  
    
                
# This function processes the story and question            
def preprocess(text):
    #text = text.lower()
    stop_words = stopwords.words('english') # remove punctuation
    text = re.sub(r'[^\w\s]', '', text) # to remove stopwords
    porter = PorterStemmer() # to stemming the words
    tokenized = word_tokenize(text) # Tokenize
    filtered_words = tokenized
    #filtered_words = [word for word in tokenized if word not in stop_words] # remove stopwords
    stemmed = [porter.stem(word) for word in filtered_words] # stemming
    
    return stemmed # return story/question
       

# This function is to find the overlap
def overlap(passage, question,options,mode):  
    # 1.1.1) preprocess the question, story and answer
    passage_token = preprocess(passage) # preprocess the story
    question_token = preprocess(question) # preprocess the question
    option_token = option_process(options) # preprocess the options   
    answer_set = ['A','B','C','D'] # this list to represent the options as A, B, C, D
    passage_size = len(passage_token)
    answer_dic = {} # this dictionary stores each options and corresponding overlap
    
    # 2.1.2) for every option
    for i in range(0,4): # iterate option
        option = option_token[i]        
        
        #1.1.2.2) make a sliding window. size = length of question + length of option
        ques_ans_set = []
        ques_ans_set.extend(question_token) 
        ques_ans_set.extend(option) # create a option + question window
        window_size = len(ques_ans_set) # length of the window
        #window_size = 20
        
        max_match = 0
        # 1.1.2.3) pass through the story and find overlap between story and window
        for window in range(0,passage_size-window_size+1):
            temp = passage_token[window:window_size+window]
            count = 0
            matched = [] # to store overlap
            for val in temp: # 
                if val in ques_ans_set: #if overlap found
                    count = count+1
                    matched.append(val)            
            
            if(count)>max_match: # to find the max overlap for a option
                max_match = count                
                
            answer_dic[answer_set[i]] = int(max_match) # store the max overlap of each option

    
    if mode == "0": # if mode 0 is selected
        ans = mode0(answer_dic) 
        return ans
    
    else: # if mode 1 selected
    # to find if there is more than one option with maximum overlap
        test_val = list(answer_dic.values()) 
        max_val = max(test_val)
        max_count = test_val.count(max_val)        
        
        # if there is more than one option with maximum overlap, use mode 1
        if(max_count>1):
            rand_ans = []
            for val in answer_dic.keys():
                if max_val == answer_dic[val]:
                    rand_ans.append(val) # store the options with maximum overlap. we will randomly choose one  
                                            # if no rule-based approach works
            ans = mode1(passage, question,options,answer_dic,rand_ans) # call mode 1 function
            
        # if there is only one option with maximum overlap, use mode 0   
        else:
            ans = mode0(answer_dic)
    
    return ans

# find the option with maximum overlap       
def mode0(answer_dic):
    ans =  (max(answer_dic, key=answer_dic.get))
    return ans

# This function returns word with its corresponding parts-of-speech
def pos(option):
    pos = nltk.pos_tag(option.split()) # use nltk library to get pos
    pos_lst = []
    for j in range(len(pos)):
        pos_lst.append(pos[j][1]) # format: (word,POS)
        
    return pos_lst

# This function is to find if the expected POS is present in the option or not            
def find_pos_answer(options,tag,answer_dic): 
    answer_set = ['A','B','C','D']
    i = 0
    for option in options.split('\t'):
        pos_lst = pos(option)           
        if tag in pos_lst: # if POS matchs then return option number (A,B,C or D)
            return answer_set[i]
        else:
            continue
        i = i+1

# This function is to find Name entity               
def find_entity_answer(options,answer_dic,name_entity,rand_ans): 
    answer_set = ['A','B','C','D']
    i = 0
    for option in options.split('\t'):  # separate the options
        for word in option.split():
            if word in name_entity: # if name entity matchs
                return answer_set[i] # return answer
            else:
                return random.choice(rand_ans) # if not matchs return a random option from max overlaped options
        i = i +1;
        
       
          
# This function applies all the rule-based approachs    
def mode1(passage, question,options,answer_dic,rand_ans):
    answer_set = ['A','B','C','D']
    stop_words = stopwords.words('english')
    
    # If the question starts with 'who/Who'
    if re.match(r".([wW]ho).*",question):
        # ---------------  SYNTAX 1 ------------------------
        # if the question starts with who, the answer should indicate a person (NNP)
        ans = find_pos_answer(options,"NNP",answer_dic) # if NNP is found in the option, mark it as correct answer    
        if ans is None: #if NNP not found
            # ---------------  IE1 ------------------------
            # find the name entity. It should start with Uppercase.
            lst = re.findall('.{1}[A-Z][A-Za-z]*', passage)
            name_entity = []
            [name_entity.append(w.strip()) for w in lst if w.lower().strip() not in stop_words]
            ans = find_entity_answer(options,answer_dic,name_entity,rand_ans) # if name entity found, mark it as correct answer
            return ans    

        else:
            return ans
        # If the question starts with 'where/Where'
    elif re.match(r".([wW]here).*",question):
        # ---------------  SYNTAX 2 ------------------------
        # if the question starts with where, the answer should indicate a place (NN)
        ans = find_pos_answer(options,"NN",answer_dic) # if NN is found in the option, mark it as correct answer 
        if ans is None: # if NN not found
            # ---------------  IE2 ------------------------
            # find the location entity. It should start with Uppercase.
             lst = re.findall('.{1}[A-Z][A-Za-z]*', passage)
             name_entity = []
             [name_entity.append(w.strip()) for w in lst if w.lower().strip() not in stop_words]
             ans = find_entity_answer(options,answer_dic,name_entity,rand_ans) # if location entity found, mark it as correct answer
             return ans 
        else:
            return ans
    # If the question starts with 'when/When'
    elif re.match(r".([wW]hen).*",question):
        # ---------------  SYNTAX 3 ------------------------
        # if the question starts with where, the answer should indicate a time(assumed a month) (NN)
        ans = find_pos_answer(options,"NNP",answer_dic) # if NNP is found in the option, mark it as correct answer 
        if ans is None: # if NNP not found
            # ---------------  IE3 ------------------------
            # find the time entity. It should have a month name.
            month = ['January','February','March','April','May','June','July','August','September','October','November','December']
            i = 0
            for option in options.split('\t'):
                for word in option.split():
                    if word in month:
                        return answer_set[i] # if time entity found, mark it as correct answer
                    else:
                        return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
                i = i+1                        
        else:
            return  ans
        # If the question starts with 'how many/How many'
    elif re.match(r".([Hh]ow many).*",question):
        # ---------------  SYNTAX 4 ------------------------
        # If the question starts with 'how many/How many', it should indicate some number (CD)
        ans = find_pos_answer(options,"CD",answer_dic) # if CD is found in the option, mark it as correct answer 
        
        if ans is None: # if CD not found
            # ---------------  IE4 ------------------------
            # Find numeric value from the options
            lst = re.findall('.[0-9]+', passage)
            number_entity = []
            [number_entity.append(w.strip()) for w in lst if w.lower().strip() not in stop_words]
            ans = find_entity_answer(options,answer_dic,number_entity,rand_ans) # if numeric value found, mark it as correct answer
            return  ans
        
        else:
            return ans
    # If the question starts with 'how many/How many' it should indicate some number $ number
    elif re.match(r".([Hh]ow many).*",question):
        # ---------------  IE5 ------------------------
        # Find numeric value from the options
        lst = re.findall('.$[0-9]+', passage) # find a number followed by a $ sign
        number_entity = []   
        [number_entity.append(w.strip()) for w in lst if w.lower().strip() not in stop_words]
        ans = find_entity_answer(options,answer_dic,number_entity,rand_ans) # if numeric value found, mark it as correct answer
        return  ans
    
    # If the question starts with 'which/Which'
    elif re.match(r".([Ww]hich).*",question):
        # ---------------  SYNTAX 5 ------------------------
        # If the question starts with 'which/Which', it should indicate Nour (NN)
        ans = find_pos_answer(options,"NN",answer_dic ) #if NN is found in the option, mark it as correct answer
        if ans is None: # if NN not found
            return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
        else:
            return ans    
        
      # ---------------  QA 1 ------------------------ 
      # If the question starts with 'why/Why did', it should indicate a Verb (VB)
    elif re.match(r".([Ww]hy did).*",question):
        ans = find_pos_answer(options,"VB",answer_dic) #if VB is found in the option, mark it as correct answer
        if ans is None:
            return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
        else:
            return ans
        
         # ---------------  QA 2 ------------------------  
         # If the question starts with 'what/What did', it should indicate a Verb (VB)
    elif re.match(r".([Ww]hat did).*",question):
        ans = find_pos_answer(options,"VB",answer_dic)  #if VB is found in the option, mark it as correct answer
        if ans is None:
            return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
        else:
            return ans
        # ---------------  QA 3 ------------------------ 
        # If the question starts with 'what/What is', it should indicate a Noun (NN)
    elif re.match(r".([Ww]hat is).*",question):
        ans = find_pos_answer(options,"NN",answer_dic) #if NN is found in the option, mark it as correct answer
        if ans is None:
            return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
        else:
            return ans
        # ---------------  QA 4 ------------------------ 
        # If the question starts with 'whose/Whose is', it should indicate a Person (NNP)
    elif re.match(r".([Ww]hose).*",question):
        ans = find_pos_answer(options,"NNP",answer_dic) #if NNP is found in the option, mark it as correct answer
        if ans is None:
            return random.choice(rand_ans) # if not found, randomly choose one option from max overlaped as correct
        else:
            return ans
         # ---------------  QA 5 ------------------------ 
         # If the question starts with 'how/How did is', it should indicate a verb (VB)
    elif re.match(r".([Hh]ow did).*",question):
        ans = find_pos_answer(options,"VB",answer_dic) #if VB is found in the option, mark it as correct answer
        if ans is None:
            return random.choice(rand_ans) 
        else:
            return ans
        
    else:
        return random.choice(rand_ans) # rule not found, randomly choose one option from max overlaped as correct          
    
                
        
if __name__ == "__main__":
    
    print("This is a Machine Reading Comprehension developed by Rupak Kumar Das.")
    parser = argparse.ArgumentParser(description='Machine Reading Comprehension.') # This is the description
    parser.add_argument('Mode', type = str,help='The Mode of the program')
    parser.add_argument('InputFile', type = str,help='The name of the Input file') # Input File selection
    parser.add_argument('OutputFile', type = str,help='The name of the output file')
    args = parser.parse_args()
    if args.Mode and args.InputFile and args.OutputFile:
        mode = args.Mode
        input_file = args.InputFile
        output_file = args.OutputFile
        f = open(output_file,'w')
        getdata(mode,input_file)

        f.close()
    
    print("Done")
