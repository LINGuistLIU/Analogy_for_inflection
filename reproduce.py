import json

langlist = [line.strip() for line in open("src/langlist")]
langdict = json.load(open("src/lang2family.json"))

newlangdict = {}
for lang in langlist:
    newlangdict[lang] = langdict[lang]

json.dump(newlangdict, open("src/lang2family_now.json", "w"), indent=4)
print(len(langdict.keys()))


langdict = json.load(open("src/lang2dir.json"))

newlangdict = {}
for lang in langlist:
    newlangdict[lang] = langdict[lang]

json.dump(newlangdict, open("src/lang2dir_now.json", "w"), indent=4)
print(len(langdict.keys()))