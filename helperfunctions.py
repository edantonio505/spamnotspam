import tarfile
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define which dataset is going to be used.
# parse as many datasets as possible

path = os.getcwd()
enron_path = "{}/{}".format(path, "enron_raw")
spam_path = "{}/spam".format(enron_path)
ham_path = "{}/ham".format(enron_path)

# get enron

# download and extract tar files
def download_and_extract(link, path):
    filename = str(link.get('href')).split("/")[-1]
    file_path = "{}/{}".format(path, filename)
    f = requests.get(link.get('href'), allow_redirects=True)
    open(file_path, 'wb').write(f.content)
    tar = tarfile.open(file_path, "r:gz")
    tar.extractall(path)
    tar.close()    
    if os.path.isfile(file_path):
            os.unlink(file_path)
    



# download enron raw data
def download_enron_raw():
    url = "http://www2.aueb.gr/users/ion/data/enron-spam/"
    r = requests.get(url)
    list_of_ham = [
        "beck-s",
        "farmer-d",
        "kaminski-v",
        "kitchen-l",
        "lokay-m",
        "williams-w3"
    ]
    
    list_of_spam = [
        "BG",
        "GP",
        "SH",
    ]
    
    #Create directories where to save them
    list_of_paths = []
   
    list_of_paths.append(enron_path)
    list_of_paths.append(spam_path)
    list_of_paths.append(ham_path)

    for directory in list_of_paths:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Check the links 
    # download the dataset to the corresponding folder
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if link.text in list_of_ham:            
            download_and_extract(link, ham_path)
            
        if link.text in list_of_spam:
            download_and_extract(link, spam_path)    






def read_email_return_str(file_path):
    with open(file_path, encoding="ISO-8859-1") as f:
        return f.read()
        

        
        
def read_email_folders(path, email_type):    
    email_corpus = []
    dirs = os.listdir(path)
    is_spam = False
    value = "ham"
    if email_type == "spam":
        is_spam = True
        value = "spam"
    
    for email_dir in dirs:
        email_dir = "{}/{}".format(path, email_dir)
        
        #read the folders inside each folder 
        email_folders = os.listdir(email_dir)
        for email_folder in email_folders:
            email_paths = "{}/{}".format(email_dir, email_folder)
            emails = os.listdir(email_paths)
            
            #read each file inside the folders in emails
            for email in emails:
                file_path = "{}/{}".format(email_paths, email)
                if os.path.isdir(file_path):
                    spam_paths = os.listdir(file_path)
                    for spam_email_path in spam_paths:
                        email_corpus.append(read_email_return_str("{}/{}".format(file_path, spam_email_path)))
                else:
                    email_corpus.append(read_email_return_str(file_path))
    return email_corpus, [value for i in range(len(email_corpus))]




def parse_enron():
    emails = []
    types = []
    #parse ham
    emails, types = read_email_folders(ham_path, "ham")
    
    #parse spam
    email_types = read_email_folders(spam_path, "spam")
    emails += email_types[0]
    types += email_types[1]
    email_corpus = pd.DataFrame(dict({ "emails": emails,"types": types}))
    email_corpus.to_csv("{}/{}".format(enron_path, "enron_raw.csv"), index=False)
    return email_corpus







def get_enron_raw_dataset():
    filename = "{}/{}".format(enron_path, "enron_raw.csv")
    if os.path.isfile(filename):
        print("file exists")
        df = pd.read_csv(filename)
        return df
    else:
        if not os.path.isdir(enron_path):
            print("downloading enron raw dataset...")
            download_enron_raw()
        print("parsing enron raw dataset...")
        return parse_enron()
        







#Lighspam
def download_extract_lingspam():
    url = "http://www.aueb.gr/users/ion/data/lingspam_public.tar.gz"
    directory = "{}/{}".format(path, "lingspam")
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = str(url).split("/")[-1]
    file_path = "{}/{}".format(directory, filename)
    f = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(f.content)
    tar = tarfile.open(file_path, "r:gz")
    tar.extractall(directory)
    tar.close()
    if os.path.isfile(file_path):
            os.unlink(file_path)


def parse_lingspam():
    directory = "{}/{}".format(path, "lingspam")
    ligspam_bare_path = "{}/lingspam_public/bare".format(directory)
    lingspam_bare_content = os.listdir(ligspam_bare_path)

    email_corpus = dict({
        "emails": [],
        "types": []
    })

    for part in lingspam_bare_content:
        part_dir = "{}/{}".format(ligspam_bare_path, part)
        part_content = os.listdir(part_dir)

        for email in part_content:
            filename = "{}/{}".format(part_dir, email)

            if "spms" in filename:
                email_corpus["emails"].append(read_email_return_str(filename))
                email_corpus["types"].append("spam")
            else:
                email_corpus["emails"].append(read_email_return_str(filename))
                email_corpus["types"].append("ham")

    email_corpus = pd.DataFrame(email_corpus)
    email_corpus.to_csv("{}/lingspam.csv".format(directory), index=False)
    return email_corpus





def get_lingspam_dataset():
    directory = "{}/{}".format(path, "lingspam")
    filename = "{}/lingspam.csv".format(directory)

    if os.path.isfile(filename):
        print("file exists")
        df = pd.read_csv(filename)
        return df
    else:
        if not os.path.isdir(directory) or len(os.listdir(directory)) == 0:
            print("downloading lingspam dataset...")
            download_extract_lingspam()
        print("parsing lingspam dataset...")
        return parse_lingspam()
