import argparse
import pickle
from spamClassifier import spamClassifier

spamclf = spamClassifier()


def main():
    parser = argparse.ArgumentParser(description="Classify email in spam or not spam")
    parser.add_argument("--message","-m",  help="Email message")
    args = parser.parse_args()
    message = args.message
    if not message:
        print("Please enter a email message")
        parser.parse_args(["-h"])
    else:
        labels = [
            "ham",
            "spam"
        ]
        result = spamclf.classify(message)[0]
        print(labels[result])


if __name__ == "__main__":
    main()






