# srcForm1 srcMSD1 # srcForm2 srcMSD2 # ... # tgtMSD => tgtForm
# i.e. leave one out for input, and output is tgtForm

import os, sys, json, inspect, random

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import readdata

def reformat(trainlist, devlist, finname, foutname):
    with open(finname, 'w') as fin, open(foutname, 'w') as fout:
        for paradigm, devparadigm in zip(trainlist, devlist):
            # print(len(paradigm), len(devparadigm))
            if len(devparadigm) != 0:
                # lemmaform, lemmamsd = paradigm[0]
                for item in devparadigm:
                    tgtmsd = item[1]
                    # tgtform = devdict[item]
                    tgtform = '-'
                    output = [letter for letter in tgtform]
                    for srcform, srcmsd in paradigm:
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
                        fin.write(' '.join(input) + '\n')
                        fout.write(' '.join(output) + '\n')

if __name__ == "__main__":

    lang = sys.argv[1]
    dirnow = sys.argv[2]

    lang_fam_dict = json.load(open(dirnow + '/src/lang2fam.json'))
    lang_dir_dict = json.load(open(dirnow + '/src/lang2dir.json'))

    paradigmdir = dirnow + "/paradigms/"

    fname = paradigmdir + lang + '.paradigm'
    trainlist, devlist, testlist, msd2formlist = readdata.train_dev_test_list(fname)

    outputdir = dirnow + '/'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    testin = outputdir + 'test.' + lang + '.input'
    testout = outputdir + 'test.' + lang + '.output'

    reformat(trainlist, testlist, testin, testout)
