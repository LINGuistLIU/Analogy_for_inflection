# sourceForm1 sourceMSD1 # sourceForm2 sourceMSD2 # targetMSD => targetForm

import os, sys, json, inspect

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
            # srcform, srcmsd = paradigm[0]
            if len(paradigm) == 1:
                tgtform, tgtmsd = paradigm[0]
                srcform1, srcmsd1 = paradigm[0]
                srcform2, srcmsd2 = paradigm[0]
                input = [letter for letter in srcform1] \
                        + [tag for tag in srcmsd1.split(';')] \
                        + ['#'] \
                        + [letter for letter in srcform2] \
                        + [tag for tag in srcmsd2.split(';')] \
                        + ['#'] \
                        + [tag for tag in tgtmsd.split(';')]
                output = [letter for letter in tgtform]
                fin.write(' '.join(input) + '\n')
                fout.write(' '.join(output) + '\n')
            elif len(paradigm) == 2:
                tgtform, tgtmsd = paradigm[0]
                srcform1, srcmsd1 = paradigm[1]
                srcform2, srcmsd2 = paradigm[1]
                input = [letter for letter in srcform1] \
                        + [tag for tag in srcmsd1.split(';')] \
                        + ['#'] \
                        + [letter for letter in srcform2] \
                        + [tag for tag in srcmsd2.split(';')] \
                        + ['#'] \
                        + [tag for tag in tgtmsd.split(';')]
                output = [letter for letter in tgtform]
                fin.write(' '.join(input) + '\n')
                fout.write(' '.join(output) + '\n')

                tgtform, tgtmsd = paradigm[1]
                srcform1, srcmsd1 = paradigm[0]
                srcform2, srcmsd2 = paradigm[0]
                input = [letter for letter in srcform1] \
                        + [tag for tag in srcmsd1.split(';')] \
                        + ['#'] \
                        + [letter for letter in srcform2] \
                        + [tag for tag in srcmsd2.split(';')] \
                        + ['#'] \
                        + [tag for tag in tgtmsd.split(';')]
                output = [letter for letter in tgtform]
                fin.write(' '.join(input) + '\n')
                fout.write(' '.join(output) + '\n')
            else:
                for i in range(0, len(paradigm)):
                    tgtform, tgtmsd = paradigm[i]
                    pnow = paradigm[:i] + paradigm[i + 1:]
                    for j in range(0, len(pnow) - 1):
                        srcform1, srcmsd1 = pnow[j]
                        for srcform2, srcmsd2 in pnow[j + 1:]:
                            input = [letter for letter in srcform1] \
                                    + [tag for tag in srcmsd1.split(';')] \
                                    + ['#'] \
                                    + [letter for letter in srcform2] \
                                    + [tag for tag in srcmsd2.split(';')] \
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
    trainlist, devlist, testlist = readdata.train_dev_test_list(fname)

    # outputdir = 'one_source/'
    outputdir = dirnow + '/'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    trainin = outputdir + 'train.' + lang + '.input'
    trainout = outputdir + 'train.' + lang + '.output'

    reformat(trainlist, trainin, trainout)