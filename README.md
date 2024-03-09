# Proportional-STAR-Voting-with-Runoffs
I made a Proportional STAR Voting Python Program, except it has one on one runoffs after every round. Instead of the highest scored candidate in a round winning a round, the top 2 candidates in a round face off in a runoff. A ballot's weighted runoff vote goes to the candidate it gave more points to.
I thought it was weird regular Proportional STAR Voting didn't have automatic one on one runoffs, since "Automatic Runoff" is half the acronym. I thought it would be good to make sure a majority of the people in a proportion preferred the winning candidate. 

Use: Just copy and paste the code into a Python Interpreter, run, and the program will ask you how many candidates are running, what their names are, how many seats can be won, and what the ballot scores are.

Output: The program will output the scores of the candidates each round, how many runoff votes they got, and who the winners are.

Credits: I used the algorithm used for regular Proportional STAR / Allocated Score from https://electowiki.org/wiki/Allocated_Score for the regular allocated score part. I then added an algorithm to count runoff votes.
