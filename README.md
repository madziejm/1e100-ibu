# 1e100 IBU

## Objectives

The projects is about dealing with multi aspect review sentiment. Multi aspect meaning, that one gives a numerical score for many aspects eg. taste, smell and overall score for a beer review.

Specific goals are:

Recovering overall rating score - pending
• Recovering per-aspect rating scores - pending
• Building sentiment lexicon – supposedly done
• Choosing the sentence that summarizes the review best -
pending
• Providing fancy-schmancy word-cloud visualization of
aspects, where word size reflects word's aspect and
sentiment influence (stolen examples at the right

- Create model for unsupervised latent aspect rating assignement
- Visualize results using CloudWords
- Create structure which allows utilizing any multi-aspect review dataset

## Model

We use simple, yet powerful method from
https://cseweb.ucsd.edu//~jmcauley/pdfs/icdm12.pdf paper by XXX.
Training proceeds alternately by xxx and gradient descent.

## Data

Got ratebeer.com dataset from [SNAP](https://snap.stanford.edu/data/web-RateBeer.html). The dataset is not publicly available as of 2021, but we managed to get it.
Introduced a new ocen-piwo.pl dataset by scrapping the website. We won't make it public, because of unknown copyright.
The data certainly needed to be parsed and tokenized.

## Results

We include two notebooks:
* for model and training notebook see [Notebook](1e100ibu.ipynb).
* for inference demo see [Notebook](example.ipynb).

## Lessons learned

At first we struggled with extremely suboptimal implementation caused by simple flaws in our code, eg. unnecessary tensor allocations. Nice lesson learned then.

LOGSUMEXP FTW
                                                                                                       
Signed up for GCP trial.

Spacy is nice after you make it work. Torchtext is not nice (returns list of int instead of LongTensor, isn't customisable)
                                                                                                       
## Further work

Understand and implement LDA and come up with a comparison. In fact deriving derivative for this problem ought to be easy, so 
Get to know how to work with both git and Jupyter Notebooks: which diff tool to use?
                                                                                                       
## Closing Remarks

Things seem to be straightforward described in simple terms. However we spent countless amount of time to debug probability computation and bugs introduced later on.

Flaws:
no baseline nor any accuracy.
training is still slow.                                                                                          
