# srcForm1 # srcForm2 # ...  => tgtForm
# i.e. leave one out for input, and output is tgtForm
#       and not using MSD information

import os, sys, json, inspect, random

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import readdata

def reformat(trainlist, finname, foutname):
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
                srcform, srcmsd = paradigm[0]
                input = [letter for letter in srcform] + [tgtmsd, '#', tgtmsd, '#']
                output = [letter for letter in tgtform]
                fin.write(' '.join(input) + '\n')
                fout.write(' '.join(output) + '\n')
            else:
                lemma, lemmamsd = paradigm[0]
                for i in range(0, len(paradigm)):
                    tgtform, tgtmsd = paradigm[i]
                    if i == 0:
                        pnow = paradigm[1:]
                    else:
                        pnow = paradigm[1:i] + paradigm[i + 1:]
                    if len(pnow) > 8:
                        random.shuffle(pnow)
                        pnow = pnow[:8]
                    pnow = [(lemma, lemmamsd)] + pnow
                    pnow += [('?', tgtmsd)]
                    input = []
                    for j in range(0, len(pnow)):
                        srcform, srcmsd = pnow[j]
                        input += [letter for letter in srcform] \
                                + [srcmsd, '#']
                    # input += [tag for tag in tgtmsd.split(';')]
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

    reformat(trainlist, trainin, trainout)
