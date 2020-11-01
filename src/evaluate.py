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
    fprediction = os.path.join(dirnow, "checkpoints-" + data_organization, lang + "-predictions", "test-checkpoint_best.pt.txt")
    fgold = os.path.join(dirnow, "task0-data/GOLD-TEST/" + lang + ".tst")
    id2pred = read_predictions(fprediction)
    id2gold = read_gold(fgold)
    acc = eval(id2pred, id2gold)
    print("Accuracy for {} test set: {}%".format(lang, acc))

if __name__ == "__main__":
    main()
