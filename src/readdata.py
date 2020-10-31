import random

def train_dev_test_list(fname):
    """
    read the paradigm file and get the list of training slots (form, msd) and dev slots (lemma, msd) in each paradigm

    :param fname: paradigm file
    :return: trainlist is a list of lists, each element list is training slots in a paradigm
             devlist is a list of lists, each element list is dev slots in a paradigm
    """
    trainlist = []
    devlist = []
    testlist = []
    msd2formlist = {}
    with open(fname) as f:
        paradigm = []
        devparadigm = []
        testparadigm = []
        for line in f:
            if line.strip() == "":
                trainlist.append(paradigm)
                devlist.append(devparadigm)
                testlist.append(testparadigm)
                paradigm = []
                devparadigm = []
                testparadigm = []
            else:
                lemma, form, msd = line.rstrip('\n').split('\t')
                if form != '?' and form != '-' and form != '*':
                    paradigm.append((form, msd))
                    if msd in msd2formlist:
                        msd2formlist[msd].append(form)
                    else:
                        msd2formlist[msd] = [form]
                if form == '-':
                    devparadigm.append((lemma, msd))
                if form == '?':
                    testparadigm.append((lemma, msd))
        if paradigm != []:
            trainlist.append(paradigm)
            devlist.append(devparadigm)
            testlist.append(testparadigm)
    return trainlist, devlist, testlist, msd2formlist

def getParalleltgtform(msd2formlist, tgtmsd, tgtform):
    tgtformlist = []
    if tgtmsd in msd2formlist:
        tgtformlist = [form for form in msd2formlist[tgtmsd]]
    paraform = tgtform
    if len(set(tgtformlist)) > 1:
        while paraform == tgtform:
            randid = random.randint(0, len(tgtformlist)-1)
            paraform = tgtformlist[randid]
            # print(paraform, tgtform)
    else:
        paraform = ''
    return paraform

def getParalleltgtform_more(msd2formlist, tgtmsd, tgtform):
    tgtformlist = []
    if tgtmsd in msd2formlist:
        tgtformlist = [form for form in msd2formlist[tgtmsd]]
    paraform = tgtform
    if len(set(tgtformlist)) > 4:
        idset = []
        while paraform == tgtform or len(idset) < 4:
            randid = random.randint(0, len(tgtformlist)-1)
            paraform = tgtformlist[randid]
            if paraform != tgtform:
                if randid not in idset:
                    idset.append(randid)
            # print(paraform, tgtform)
        formlist = [tgtformlist[i] for i in idset]
    else:
        formlist = [item for item in tgtformlist if item != tgtform]

    return formlist

def getParalleltgtform_two(msd2formlist, tgtmsd, tgtform):
    tgtformlist = []
    if tgtmsd in msd2formlist:
        tgtformlist = [form for form in msd2formlist[tgtmsd]]
    paraform = tgtform
    if len(set(tgtformlist)) > 2:
        idset = []
        while paraform == tgtform or len(idset) < 2:
            randid = random.randint(0, len(tgtformlist)-1)
            paraform = tgtformlist[randid]
            if paraform != tgtform:
                if randid not in idset:
                    idset.append(randid)
            # print(paraform, tgtform)
        formlist = [tgtformlist[i] for i in idset]
    else:
        formlist = [item for item in tgtformlist if item != tgtform]

    return formlist


def getMSDlist(fname):
    pos2msdlist = {}
    msdlist = []
    pos = 'V'
    with open(fname) as f:
        for line in f:
            if line.strip() == '':
                pos2msdlist[pos] = msdlist
                msdlist = []
            else:
                lemma, form, msd = line.rstrip('\n').split('\t')
                msdlist.append(msd)
                pos = msd.strip().split(';')[0]
                pos = pos.split('.')[0]
        if msdlist != []:
            pos2msdlist[pos] = msdlist
    return pos2msdlist

def getDevdict(fname):
    """
    read the shared task dev data and return a dictionary {lemma-msd: form}

    :param fname: shared task dev file
    :return: dev_dict = {(lemma, msd): form}
    """
    dev_dict = {}
    with open(fname) as f:
        for line in f:
            lemma, form, msd = line.rstrip('\n').split('\t')
            lemma = lemma.replace(' ', '_')
            form = form.replace(' ', '_')
            msd = msd.replace(' ', '_')
            dev_dict[(lemma, msd)] = form
    return dev_dict
