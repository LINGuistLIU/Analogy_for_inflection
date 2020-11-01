# Analogy_for_inflection

This is the code and data we used for experiments in the following paper:

Ling Liu and Mans Hulden. 2020. [Analogy models for neural word inflection](). *COLING*.

1. reconstruct partial paradigms from shared task data:

    ```python src/get_paradigms.py```

2. train the models and make predictions:

    ```./src/runAll.sh <data_reformatting_method>```

    ```<data_reformatting_method>``` can be # change here for other data reformatting methods: ```1src```, ```1src1crosstable```, ```1src2crosstable```, ```2src```, or ```leave1outMSDchunk```.

    Details on training parameters for different data_organization_method can be found in Appendix A of the paper.

3. data hallucination:

    We used data hallucination implementation provided by the SIGMORPHON 2020 shared task 0, available [here: example/sigmorphon2020-shared-tasks/augment.sh](https://github.com/shijie-wu/neural-transducer/tree/f1c89f490293f6a89380090bf4d6573f4bfca76f). We conducted the data hallucination on the training data created with the ```1src``` data reformatting method.

4. evaluation:

    ```python src/evaluate.py <language> <data_organization_method>```

    