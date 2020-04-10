### Friweb

**By Brieuc Loussouarn, Etienne Wallet and Hamza Kadiri at CentraleSupélec.**

This project is a search engine based on TF-IDF. The engine will use the dataset that can be found [here](http://web.stanford.edu/class/cs276/pa/pa1-data.zip).


### Installation

After installing the required dependencies with 

```
$ pip install -r requirements.txt
```

run the command below to download the dataset and some librairies from NLTK:
```
$ python download.py
```

### Search engine and Query

To use the search engine, enter the command:

```
$ python main.py
```
and then follow the instructions given on the console.

**Example output** : 

[![screenshot](https://raw.githubusercontent.com/EtWnn/friweb/master/assets/query_exemple.PNG)](https://raw.githubusercontent.com/EtWnn/friweb/master/assets/query_exemple.PNG)

> Warning: The first run of the engine will also include the computation of the search indexes. This can take some time.

### Test accuracy

To test the accuracies for the 8 queries present in ```tests_data/queries```, enter the command : 


```
$ python test.py
```