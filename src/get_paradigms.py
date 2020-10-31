# convert the shared task data into paradigms

import os, json
from collections import defaultdict

def _oneFile2paradigm(fname, lemma_paradigm, lemma_paradigm_filled, msdlist):
    count = 0
    with open(fname) as f:
        for line in f:
            lines = line.strip().split('\t')
            count += 1
            if len(lines) == 2:
                lemma, msd = lines
                form = '?'
            else:
                lemma, form, msd = lines
            # lemma = lemma.strip().replace(' ', '_')
            # form = form.strip().replace(' ', '_')
            # msd = msd.strip().replace(' ', '_')
            lemma = lemma.replace(' ', '_')
            form = form.replace(' ', '_')
            msd = msd.replace(' ', '_')

            lemma_paradigm_filled[lemma].append((form, msd))
            if '.dev' in fname:
                form = '-'
            lemma_paradigm[lemma].append((form, msd))
            msdlist.append(msd)
    if '.trn' in fname:
        print('train #:', count)
    elif '.dev' in fname:
        print('dev #:', count)
    else:
        print('tst #:', count)
    return lemma_paradigm, lemma_paradigm_filled, msdlist


def files2paradigm(ftrn_name, fdev_name, ftst_name):
    lemma_paradigm = defaultdict(list)
    lemma_paradigm_filled = defaultdict(list)
    msdlist = []
    lemma_paradigm, lemma_paradigm_filled, msdlist = _oneFile2paradigm(ftrn_name, lemma_paradigm, lemma_paradigm_filled, msdlist)
    lemma_paradigm, lemma_paradigm_filled, msdlist = _oneFile2paradigm(fdev_name, lemma_paradigm, lemma_paradigm_filled, msdlist)
    lemma_paradigm, lemma_paradigm_filled, msdlist = _oneFile2paradigm(ftst_name, lemma_paradigm, lemma_paradigm_filled, msdlist)
    msdlist = sorted(list(set(msdlist)))
    pos_msd_dict = defaultdict(list)
    for msd in msdlist:
        pos = msd.split(';')[0]
        if '.' in pos:
            pos = pos.split('.')[0]
        pos_msd_dict[pos].append(msd)
    for k, v in pos_msd_dict.items():
        print('->', k, len(v), v)
    return lemma_paradigm, lemma_paradigm_filled, pos_msd_dict

def _paradigm2output(paradigm, foutname, pos_msd_dict):
    paradigmcount = 0
    with open(foutname, 'w') as fout:
        for lemma, forms in paradigm.items():
            msd_form_dict = {}
            poslist = []
            for form, msd in forms:
                msd_form_dict[msd] = form
                pos = msd.strip().split(';')[0]
                if '.' in pos:
                    pos = pos.split('.')[0]
                if pos not in poslist:
                    poslist.append(pos)

            for posnow in poslist:
                canonicalform = lemma
                canonicalmsd = posnow+';CANONICAL'
                fout.write('\t'.join([canonicalform, canonicalform, canonicalmsd]) + '\n')
                msdlist = pos_msd_dict[posnow]
                for msd in msdlist:
                    if msd in msd_form_dict:
                        form = msd_form_dict[msd]
                    else:
                        form = '*'
                    fout.write('\t'.join([lemma, form, msd]) + '\n')
                fout.write('\n')
                paradigmcount += 1
    print('paradigm #:', paradigmcount)

def generate_paradigms(lemma_paradigm, lemma_paradigm_filled, msdlist, lang):
    paradigm_dir = 'paradigms/'
    os.makedirs(paradigm_dir, exist_ok=True)
    fparadigm_name = os.path.join(paradigm_dir, lang+'.paradigm')
    fparadigm_filled_name = os.path.join(paradigm_dir, lang + '.paradigm.filled')
    _paradigm2output(lemma_paradigm, fparadigm_name, msdlist)
    # _paradigm2output(lemma_paradigm_filled, fparadigm_filled_name, msdlist)

def process_one_language(dirname, lang):
    ftrn_name = os.path.join(dirname, lang+'.trn')
    fdev_name = os.path.join(dirname, lang + '.dev')
    ftst_name = os.path.join(dirname, lang + '.tst')
    lemma_paradigm, lemma_paradigm_filled, msdlist = files2paradigm(ftrn_name, fdev_name, ftst_name)
    generate_paradigms(lemma_paradigm, lemma_paradigm_filled, msdlist, lang)
    return

if __name__ == "__main__":
    # dirnow = "./"
    # known_dir = dirnow + "/task0-data/DEVELOPMENT-LANGUAGES/"
    # surprise_dir = dirnow + "/task0-data/SURPRISE-LANGUAGES/"
    #
    # langcount = 0
    # langcount = processDir(known_dir, langcount)
    # langcount = processDir(surprise_dir, langcount)

    lang2fam = json.load(open("src/lang2family.json"))
    lang2dir = json.load(open("src/lang2dir.json"))

    for lang, fam in lang2fam.items():
        print("...reconstruction paradigms for {}...".format(lang))
        langdir = os.path.join("task0-data", lang2dir[lang], fam)
        process_one_language(langdir, lang)
