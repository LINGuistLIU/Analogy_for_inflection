# srcForm1 srcMSD1 # srcForm2 srcMSD2 # ... # tgtMSD => tgtForm
# i.e. leave one out for input, and output is tgtForm

import os, sys, inspect, random

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import readdata

def reformat(trainlist, finname, foutname, msd2formlist):
    """
    convert the training data in paradigms to the format needed for Transformer preprocessing

    :param trainlist: list of paradigms
    :param finname: input data for Transformer
    :param foutname: output data for Transformer
    :return: None
    """
    with open(finname, 'w') as fin, open(foutname, 'w') as fout:
        for paradigm in trainlist:
            if len(paradigm) == 1:
                tgtform, tgtmsd = paradigm[0]
                paraform = readdata.getParalleltgtform(msd2formlist, tgtmsd, tgtform)
                srcform, srcmsd = paradigm[0]
                input = [letter for letter in srcform] \
                        + [tag for tag in srcmsd.split(';')] \
                        + ['#'] \
                        + [letter for letter in paraform] \
                        + [tag for tag in tgtmsd.split(';')] \
                        + ['#'] \
                        + [tag for tag in tgtmsd.split(';')]
                output = [letter for letter in tgtform]
                fin.write(' '.join(input) + '\n')
                fout.write(' '.join(output) + '\n')
            else:
                for i in range(0, len(paradigm)):
                    tgtform, tgtmsd = paradigm[i]
                    pnow = paradigm[:i] + paradigm[i + 1:]
                    for srcform, srcmsd in pnow:
                        paraform = readdata.getParalleltgtform(msd2formlist, tgtmsd, tgtform)
                        if paraform != '':
                            input = [letter for letter in srcform] \
                                    + [tag for tag in srcmsd.split(';')] \
                                    + ['#'] \
                                    + [letter for letter in paraform] \
                                    + [tag for tag in tgtmsd.split(';')] \
                                    + ['#'] \
                                    + [tag for tag in tgtmsd.split(';')]
                        else:
                            input = [letter for letter in srcform] \
                                    + [tag for tag in srcmsd.split(';')] \
                                    + ['#'] \
                                    + [tag for tag in tgtmsd.split(';')]
                        output = [letter for letter in tgtform]
                        fin.write(' '.join(input) + '\n')
                        fout.write(' '.join(output) + '\n')


if __name__ == "__main__":

    lang = sys.argv[1]
    dirnow = sys.argv[2]

    datadir = dirnow + "/paradigms/"

    fname = datadir + lang + '.paradigm'
    trainlist, devlist, testlist, msd2formlist = readdata.train_dev_test_list(fname)

    # outputdir = 'one_source/'
    outputdir = dirnow + '/'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    trainin = outputdir + 'train.' + lang + '.input'
    trainout = outputdir + 'train.' + lang + '.output'

    reformat(trainlist, trainin, trainout, msd2formlist)
