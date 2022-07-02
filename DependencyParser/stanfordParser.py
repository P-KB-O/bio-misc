import os
import csv

from nltk.parse.corenlp import CoreNLPDependencyParser

# https://stackoverflow.com/questions/13883277/how-to-use-stanford-parser-in-nltk-using-python/51981566#51981566

java_path = 'java_path'
os.environ['JAVAHOME'] = java_path

os.environ['STANFORD_PARSER'] = '../stanford-parser-full-2020-11-17/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '../stanford-parser-full-2020-11-17/stanford-parser-4.2.0-models.jar'

"""
coreNLP server enable command 
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 &
"""
eng_parser = CoreNLPDependencyParser(url='http://localhost:9000')

with open('./data/pudmed/abstract0.csv', 'r') as fr, open('./data/pudmed/conlls/abstract0.conll', 'w+') as fw:
    read_csv = csv.reader(fr, dialect='excel')
    for line in read_csv:
        if 'PMID' in line:
            continue
        if line is None or line == "":
            continue
        else:
            sentences, = eng_parser.parse(line[-1].split(" "))
            fw.write(sentences.to_conll(10))
            fw.write('\n')
            fw.flush()
