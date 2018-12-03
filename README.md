
# ATIS_X_test
A modified version of the ATIS test set, which is used in paper of "[Concept Transfer Learning for Adaptive Language Understanding](http://aclweb.org/anthology/W18-5047)". It can be exploited to evaluate the generalization capability of slot filling and intent detection models.

## ATIS files
 * train.raw : training set with word features;
 * train.DIGIT : as what [http://deeplearning.net/tutorial/rnnslu.html] did, we also converted sequences of numbers with the string DIGIT i.e. 1984 is converted to DIGITDIGITDIGITDIGIT;
 * valid.raw : validation set with word features;
 * valid.DIGIT : validation set with DIGIT tokens;
 * test.raw : test set with word features;
 * test.DIGIT : test set with DIGIT tokens;
 * test_X.raw : ATIS_X_test with word features.
 * test_X.DIGIT : ATIS_X_test with DIGIT tokens.
 * The split of train and valid followed 'split 3' of [https://github.com/mesnilgr/is13]. The dataset with DIGIT tokens is recommended since it always gives better performance.

## How to generate test_X files
 * python 2.7
 * python generate_unmatched_test_set.py test.raw test_X.raw slot_values_train.json
 * python preprocess_on_rawdata.py test_X.raw > test_X.DIGIT

## Reference
 * Su Zhu and Kai Yu. Concept Transfer Learning for Adaptive Language Understanding. 19th Annual Meeting of the Special Interest Group on Discourse and Dialogue, Melbourne, Australia, 2018: 391-399.
