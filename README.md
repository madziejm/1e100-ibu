# 1e100 IBU

## Project description

Reviews we encounter on the web often consist of textual description and numerical aspect scores typically presented with stars that mark how much one liked some aspects of an item being reviewed, eg. for beer one could rate aroma, palate (when discussing taste in a broader sense), head (foam), etc.  
The project is about exploring various approaches dealing with multi-aspect review sentiment.
Multi-aspect means, that one gives a numerical score for many aspects eg. taste, smell and overall score for a beer review.

## Objectives

Specific goals are to:

* Represent dataset of reviews in a structured way
* Recover overall rating score
* Recover per-aspect rating scores
* Predict aspect that sentence of a review is about
* Build sentiment lexicons, ie. groups of words discussing aspects or having positive sentiment towards some aspect
* Provide fancy-schmancy word-cloud visualization of aspect lexicon, where word size reflects word's aspect or sentiment influence

## Methods

The main inspiration for our project was ["Learning Attitudes and Attributes from Multi-Aspect Reviews"](https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm12.pdf) by Julian McAuley, Jure Leskovec, Dan Jurafsky. We appreciated that the authors provide a simple, yet powerful and interpretable method that we can use. Using the latest neural models would probably be overkill and not much educative, considering the fact that this is a project for a Machine Learning class. Along with the paper, there was a 5 million beer review dataset published too.

### Aspect assignment and sentiment/aspect lexicons task

This follows the paper mentioned before.

The weights yielded when training for this task are highly interpretable can be used for building aspect lexicons. We present them in the form of word clouds that are highly eyesome.

### Rating prediction task

We tried a paper-like approach and vector embeddings. The latter is just KNN for average/max pooled reviews.

We mapped reviews to vectors using both FastText and distilled BERT. [FAISS library](https://github.com/facebookresearch/faiss) was used to index the mapped sentences. We copped with converting at most 1M reviews because of the high memory footprint.


### Hunga-Bunga

We felt a bit lost along the way with this task, so we considered SOTA (state of the art) [Hunga Bunga search](https://github.com/ypeleg/HungaBunga), but the code is not maintained and even if you fix it, it's too slow even for MNIST.

## Data

* At first, we got a 3M ratebeer.com reviews dataset from [SNAP](https://snap.stanford.edu/data/web-RateBeer.html). The dataset is not publicly available as of 2021, but we managed to get it.
* Later on, we introduced a new ca. 50K Polish beer reviews dataset by scrapping [ocen-piwo.pl](https://ocen-piwo.pl). We won't make it public because of unknown copyright.

See dataset representation code for dataset samples.

The data certainly needed to be parsed and tokenized. We opted to use models available in the SpaCy NLP toolkit for tokenization and sentence split. We used the TorchText Vocab class for indexing words where needed.

## Results

All of the examples, methods and results are described in detail in the single [project Jupyter notebook](https://github.com/madziejm/1e100-ibu/blob/master/1e100ibu.ipynb).

## Lessons learned

* At first, we struggled with extremely suboptimal implementation caused by simple flaws in our code, eg. unnecessary tensor allocations. General advice is to use library code when possible and follow precisely official framework tutorials when available. Nice lesson learned anyway
* When implementing log-softmax on our own for no explainable reason we got blocked by numerical issues. They can be solved using the log-sum-exp trick. One should use library log-softmax if available, regardless
* We needed to sign up for the GCP trial in order to run time-consuming computations. Now we know how to use it for hosting a Jupyter notebook
* Spacy is nice after you make it work, but it's overkill for our use. Torchtext is not nice (for example it returns a list of ints where we needed of LongTensor, isn't customisable), but it works
* Simple or even obvious models can present really valuable results because as we noticed the distributions of ratings that people give are rather exploitable and easy to infer

## Further work

* Understand and implement LDA and come up with a comparison
* Understand training rating model from the paper that uses SVM
* Get rid of PyTorch and find derivatives analytically, which shouldn't be hard
* Learn what is a proper way to represent data, so it's automatically pipelined to GPU for better performance (grep code for coalesce to see the issue)
* Get to know how to work with both git and Jupyter Notebooks: which diff tool to use?
* Automate experiments further on our own or by learning PyTorch Lightning or a similar library that makes training easier. Run the segmentation many times and pick the model with the lowest validation NLL. Experiment on which stochastic optimization method performs best
* Extend to other domains (similar like wine or different like products)
* Remove duplicate code

## Closing Remarks

Things seem to be straightforward when described in simple terms. However, we misunderstood some stuff and spent countless amounts of time debugging probability computation and other bugs introduced. On the other hand, we got some satisfying results and even introduced our own modifications and ideas. 

Flaws:
* No baseline nor any accuracy, so we can't give full results.
* Training could be faster, as mentioned before. It takes ca. 6 hours for SNAP Ratebeer on GCP 4-core instance. This dataset is quite big on the other hand.
