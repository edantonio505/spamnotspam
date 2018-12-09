import argparse
import pickle



def main():
    parser = argparse.ArgumentParser(description="Classify email in spam or not spam")
    parser.add_argument("--message","-m",  help="Email message")
    args = parser.parse_args()
        
    message = args.message
    
    if not message:
        print("Please enter a email message")
        parser.parse_args(["-h"])
    





if __name__ == "__main__":
    main()






