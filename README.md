# Analogy_for_inflection

This is the code and data we used for experiments in the following paper:


1. reconstruct partial paradigms from shared task data:

    ```python src/get_paradigms.py```

2. train the models and make predictions:

    ```./src/runAll.sh <data_organization_method>```

    ```<data_organization_method>``` can be # change here for other data organizations: ```1src```, ```1src1crosstable```, ```1src2crosstable```, ```2src```, or ```leave1outMSDchunk```.

    Details on training parameters for different data_organization_method can be found in Appendix A of the paper.

3. evaluation:

    ```python src/evaluate.py <language> <data_organization_method>```

    