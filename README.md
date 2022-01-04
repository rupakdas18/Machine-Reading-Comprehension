# Machine-Reading-Comprehension

**Program Details:** This is a reading comprehension test that consists of multiple choice
questions based on a short story.
**Code Usage:** The user should follow below format in a commandline
python machine-reader.py 0/1 mc500.(dev/test).tsv (dev/test).(0/1).txt
python machine-grader.py (dev/test).(0/1).txt mc500.(dev/test).ans (dev/test).(0/1).graded.txt
where,
0/1 is mode. 0 is baseline and 1 is enhanced version
mc500.(dev/test).tsv, file contains question
(dev/test).(0/1).txt, file contains predicted answer
mc500.(dev/test).ans, file contains actual answer
(dev/test).(0/1).graded.txt, provide the accuracy
**Program Algorithm (Reader):**
1) Mode 0:
  - for every question
    - preprocess the question, story and answer
    - for every option
      - preprocess the question, story and answer
      - make a sliding window. size = length of question + length of option
      - pass through the story and find overlap
      - find max number of overlap for each option
    - find the max overlap for all of those options. The option with max operlap is the answer.
2) Mode 1:
  - for every question
    - preprocess the question, story and answer
    - for every option
      - make a sliding window. size = length of question + length of option
      - pass through the story and find overlap
      - find max number of overlap for each option
    - find the max overlap for all of those options.
      - If there is only one option with maximum overlap, that option is answer
      - else(more than one option with maximum overlap) use enhanced ruled-based approach
      - if doesn't match with any rule-based approach then choose one option randomly with max overlap(not from all options)
