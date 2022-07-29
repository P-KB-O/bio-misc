## CoreNLP usage

first, ensure >=JDK8 enviroment is installed on your device. secondly, download [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) and unzip it. check this [stackoverflow link](https://stackoverflow.com/a/51981566)

In fact, when I process immense amounts of data, directly parseing data by stanford CoreNLP, which would cost lots of time. [Spark](https://github.com/databricks/spark-corenlp) might be a good way. I'll take a shot.

enable CoreNLP server:
``` shell
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 &
```
and input **http://localhost:9000/** on you web browser, then you can paser some sentences.
<img width="1455" alt="image" src="https://user-images.githubusercontent.com/85916131/181723515-17f0b168-da0b-4fea-9462-e04a80127464.png">

 
## GDep parser

GDep parser is a dependency parser for biomedical text.

This software cannot acquire from web. I emailed to [Prof. Kenji Sagae](https://compling.ucdavis.edu/sagae/software.html), util now i haven't received a reply.
