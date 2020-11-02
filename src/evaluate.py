import sys, os

def read_predictions(fprediction):
    id2pred = {}
    with open(fprediction) as f:
        for line in f:
            if line[:2] == "H-":
                idx, score, pred = line.split("\t")
                idx = int(idx.split("-")[-1])
                pred = pred.strip().replace(" ", "").replace("<<unk>>", "?").replace("<unk>", "?").replace("_", " ")
                id2pred[idx] = pred
    return id2pred

def read_gold(fgold):
    idx = 0
    id2gold = {}
    with open(fgold) as f:
        for line in f:
            lemma, form, msd = line.split("\t")
            id2gold[idx] = form.strip()
            idx += 1
    return id2gold

def get_best_on_dev(lang, data_organization):
    pred_dir = os.path.join("checkpoints-"+data_organization, lang+"-predictions")
    file2acc = {}
    for item in os.listdir(pred_dir):
        if "dev-" in item:
            fname = os.path.join(pred_dir, item)
            with open(fname) as f:
                id2pred = {}
                id2gold = {}
                for line in f:
                    if line[:2] == "H-":
                        idx, score, pred = line.split("\t")
                        idx = int(idx.split("-")[-1])
                        pred = pred.strip().replace(" ", "").replace("<<unk>>", "?").replace("<unk>", "?").replace("_", " ")
                        id2pred[idx] = pred
                    elif line[:2] == "T-":
                        idx, gold = line.split("\t")
                        idx = int(idx.split("-")[-1])
                        gold = gold.strip().replace(" ", "").replace("<<unk>>", "?").replace("<unk>", "?").replace("_", " ")
                        id2gold[idx] = gold
            acc = eval(id2pred, id2gold)
            file2acc[item] = acc
    return max(file2acc.items(), key=lambda x:x[1])[0]

                        

def eval(id2pred, id2gold):
    guess = 0
    correct = 0
    for idx, gold in id2gold.items():
        if gold == id2pred[idx]:
            correct += 1
        guess += 1
    acc = round(100*correct/guess, 1)
    return acc

def main():
    lang = sys.argv[1]
    data_organization = sys.argv[2]
    dirnow = "./"
    best_on_dev = get_best_on_dev(lang, data_organization)
    fprediction = os.path.join(dirnow, "checkpoints-" + data_organization, lang + "-predictions", best_on_dev.replace("dev-", "test-"))
    fgold = os.path.join(dirnow, "task0-data/GOLD-TEST/" + lang + ".tst")
    id2pred = read_predictions(fprediction)
    id2gold = read_gold(fgold)
    acc = eval(id2pred, id2gold)
    print("Accuracy for {} test set: {}%".format(lang, acc))

if __name__ == "__main__":
    main()
