import argparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

################################################
#               IMPORTANT                      #
################################################
# 1. Do not print anything other than the ranked list of papers.
# 2. Do not forget to remove all the debug prints while submitting.




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-paper-title", type=str, required=True)
    parser.add_argument("--test-paper-abstract", type=str, required=True)
    args = parser.parse_args()

    # print(args)

    ################################################
    #               YOUR CODE START                #
    ################################################

    # Build corpus of existing papers
    dataset_dir = os.path.join(os.path.dirname(__file__), "dataset_papers")
    papers, docs = [], []   
    for folder in os.listdir(dataset_dir):
        fp = os.path.join(dataset_dir, folder)
        tfile = os.path.join(fp, "title.txt")
        afile = os.path.join(fp, "abstract.txt")
        if os.path.isdir(fp) and os.path.isfile(tfile) and os.path.isfile(afile):
            with open(tfile, 'r', encoding='utf-8', errors='ignore') as f:
                t = f.read().strip()
            with open(afile, 'r', encoding='utf-8', errors='ignore') as f:
                a = f.read().strip()
            papers.append(folder)
            docs.append(t + " " + a)

    # TF-IDF vectorization and similarity
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_mat = vectorizer.fit_transform(docs)
    test_doc = args.test_paper_title + " " + args.test_paper_abstract
    test_vec = vectorizer.transform([test_doc])
    sims = cosine_similarity(test_vec, tfidf_mat)[0]

    # Top-K predictions
    K = 10
    topk = sims.argsort()[::-1][:K]
    result = [papers[i] for i in topk]

    ################################################
    #               YOUR CODE END                  #
    ################################################


    ################################################
    #               DO NOT CHANGE                  #
    ################################################
    print('\n'.join(result))

if __name__ == "__main__":
    main()
