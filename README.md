# Bayesian-link-prediction
A project aiming to use Bayesian method to resolve the link prediction problem.

There are 4 files in this repository:

1.File "Preprocessing.py" is to read the data file and calculate the time length.

2.File "K2algrithm.py" converted the temporal network to the Bayesian network by K2 algorithm.

3.File "TrainingModel.py" used the data and Bayesian network obtained from step2 to have Bayesian parameter learning and we got the posterial probability in the Bayesian network after this step.

4.File "Predicting.py" predict the edges in the test set and compute the precision index.


