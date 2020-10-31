# srcForm1 srcMSD1 # srcForm2 srcMSD2 # ... # tgtMSD => tgtForm
# i.e. leave one out for input, and output is tgtForm

import os, sys, json, inspect, random

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import readdata

def reformat(trainlist, devlist, devdict, finname, foutname, pos2msdlist):
    """
    reformat the dev data into the input and output format for Transformer preprocessing

    :param trainlist: [(form, msd)]
    :param devlist: [(lemma, msd)]
    :param devdict: {(lemma, msd): form}
    :param finname: Transformer preprocessing input file
    :param foutname: Transformer preprocessing output file
    :return: None
    """
    with open(finname, 'w') as fin, open(foutname, 'w') as fout:
        for paradigm, devparadigm in zip(trainlist, devlist):
            # print(len(paradigm), len(devparadigm))
            if len(devparadigm) != 0:
                msd2form = {msd: form for form, msd in paradigm}
                pos = paradigm[0][1].strip().split(';')[0]
                pos = pos.split('.')[0]
                for item in devparadigm:
                    tgtmsd = item[1]
                    tgtform = devdict[item]

                    pnow = []
                    for msd in pos2msdlist[pos]:
                        if msd in msd2form:
                            if 'CANONICAL' in msd:
                                lemmainfo = [(msd2form[msd], msd)]
                            else:
                                pnow.append((msd2form[msd], msd))
                    if len(pnow) > 8:
                        random.shuffle(pnow)
                        pnow = pnow[:8]
                    pnow = lemmainfo + pnow
                    pnow += [('?', tgtmsd)]

                    input = []
                    for j in range(0, len(pnow)):
                        srcform, srcmsd = pnow[j]
                        input += [letter for letter in srcform] \
                                 + [srcmsd, '#']
                    output = [letter for letter in tgtform]
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

    devdir = dirnow + '/task0-data/' + lang_dir_dict[lang]
    fdevname = devdir + lang_fam_dict[lang] + '/' + lang + '.dev'
    pos2msdlist = readdata.getMSDlist(fname)

    devdict = readdata.getDevdict(fdevname)

    # outputdir = 'one_source/'
    outputdir = dirnow + '/'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    devin = outputdir + 'dev.' + lang + '.input'
    devout = outputdir + 'dev.' + lang + '.output'

    reformat(trainlist, devlist, devdict, devin, devout, pos2msdlist)
