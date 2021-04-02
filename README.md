# Analogy_for_inflection

This is the code and data we used for experiments in the following paper:

Ling Liu and Mans Hulden. 2020. [Analogy models for neural word inflection](https://www.aclweb.org/anthology/2020.coling-main.257/). *COLING 2020*.

## Installation

This repository was tested on Python 3.6.10.

All dependencies can be installed as follows:

```pip install -r requirements.txt```

## Reconstruct partial paradigms from shared task data

```python src/get_paradigms.py```

## Train the models and make predictions

```bash src/runAll.sh <data_reformatting_method>```

```<data_reformatting_method>``` can be # change here for other data reformatting methods: ```1src```, ```1src1crosstable```, ```1src2crosstable```, ```2src```, or ```leave1outMSDchunk```.

Details on training parameters for different data_organization_method can be found in Appendix A of the paper.

## Data hallucination

We used data hallucination implementation provided by the SIGMORPHON 2020 shared task 0, available [here: example/sigmorphon2020-shared-tasks/augment.sh](https://github.com/shijie-wu/neural-transducer/tree/f1c89f490293f6a89380090bf4d6573f4bfca76f). We conducted the data hallucination on the training data created with the ```1src``` data reformatting method.

## Evaluation

```python src/evaluate.py <language> <data_organization_method>```

    
