# repo-eventdetection
The following repo "repo-eventdetection" is an implementation of the following paper "Event detection in Twitter: A keyword volume approach", by Ahmad Hany Hossny,Lewis Mitchell.
Link to the paper: arXiv:1901.00570 (https://arxiv.org/abs/1901.00570).

Execution Order:
1. PreProcessingTweets.py
2. GetWordPairs.py
3. WordPairEventCountMatrix.py -- Single Processor
4. WordPairEventCountMatrixPool.py -- Multi Processor
5. FeatureSelectionJaccard.py -- Building Features
6. Try Differnt Machine Learning Models