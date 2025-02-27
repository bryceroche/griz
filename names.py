text = """
Some economists have responded positively to Bitcoin, including
Francois R. Velde, senior economist of the Federal Reserve in Chicago
who described it as "an elegant solution to the problem of creating a
digital currency." In November 2013 Richard Branson announced that
Virgin Galactic would accept Bitcoin as payment, saying that he had invested
in Bitcoin and found it "fascinating how a whole new global currency
has been created", encouraging others to also invest in Bitcoin.
Other economists commenting on Bitcoin have been critical.
Economist Paul Krugman has suggested that the structure of the currency
incentivizes hoarding and that its value derives from the expectation that
others will accept it as payment. Economist Larry Summers has expressed
a "wait and see" attitude when it comes to Bitcoin. Nick Colas, a market
strategist for ConvergEx Group, has remarked on the effect of increasing
use of Bitcoin and its restricted supply, noting, "When incremental
adoption meets relatively fixed supply, it should be no surprise that
prices go up. And that’s exactly what is happening to BTC prices."
"""

import nltk
#from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
text = """YOUR TEXT GOES HERE"""

for sent in nltk.sent_tokenize(text):
  tokens = nltk.tokenize.word_tokenize(sent)
  tags = st.tag(tokens)
  for tag in tags:
    if tag[1]=='PERSON': print (tag)
