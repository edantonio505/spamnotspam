from spamClassifier import spamClassifier
labels = [
    "ham",
    "spam"
]




spamClf = spamClassifier()




spam = """everything from solo up to dirty gang-bangs!         





everything from solo up to dirty gang-bangs!         

celebrities are no super-humans, just ordinary men and women who also
have passions and sins! they all have sex, masturbate, sometimes get way
too down and dirty for their names - but still they act like all the
others out there. luckily, thanks to some skilled paparazzies we have a
great collection of xxx pics with them in action! blowjobs, anal, oral,
cumshots and orgies! must see! join now http://total-portal.cn.st/?7m5tt96c08j7o2t !"""













print(spamClf.classify(spam))











