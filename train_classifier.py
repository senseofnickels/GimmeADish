import re
import math
import pickle

def remove_stop_words(tokens):
    stopwords = ['the','a','of','is','was','and','be', 'to', 'as', 'my', 'for', 'i', 'it', 'in']

    tokens = [ t for t in tokens if t not in stopwords]
    return tokens

def get_ngrams(sentence, n=1):
    start = '<'
    end = '>'
    tokens = [str(word) for word in re.findall(r'\w+', sentence.lower())]
    tokens = remove_stop_words(tokens)
    if len(tokens) == 0:
        return []
    for i in range(n-1):
        tokens.insert(0, start)
        tokens.append(end)
    return zip(*[tokens[i:] for i in range(n)])

def update_ngram_count(ngrams, ngram_class):
    for ngram in ngrams:
        if ngram in ngram_class:
            ngram_class[ngram] += 1
        else:
            ngram_class[ngram] = 1

    return ngram_class

def get_ngram_probabilities(ngrams, class_probability):
    total_count = sum_ngram_count(ngrams)
    for key in ngrams.keys():
        ngrams[key] = math.log((ngrams[key] + 1.0) / (len(ngrams) + 1.0))
    ngrams['*'] = math.log( 1.0  / (len(ngrams) + 1.0))
    return ngrams

def predict_class(sentence, relevant, not_relevant, n):
    rel_prob = 0.0
    not_rel_prob = 0.0

    ngrams = get_ngrams(sentence, n)

    for ngram in ngrams:
        print ngram
        
        if ngram in relevant:
            print 'Relevant:', relevant[ngram]
            rel_prob += relevant[ngram]
        else:
            print 'Relevant:(unseen)', relevant['*']
            rel_prob += relevant['*']

        if ngram in not_relevant:
            print 'Not Relevant:', not_relevant[ngram]
            not_rel_prob += not_relevant[ngram]
        else:
            print 'Not Relevant:(unseen)', not_relevant['*']
            not_rel_prob += not_relevant['*']

    print 'Probability that sentence is relevant:', rel_prob
    print 'Probability that sentence is not relevant:', not_rel_prob

    if rel_prob > not_rel_prob:
        return 'Relevant'
    else:
        return 'Not Relevant'

def sum_ngram_count(ngrams):
    return sum(ngrams.values())

def prepare_sentence(sentence):
    sentence = re.sub(r'[^\w^\s]', '', sentence)
    return sentence

def get_relevant_sentences(review, relevant, not_relevant, n):
    relevant_sentences = []
    for sentence in review:
        if predict_class(prepare_sentence(sentence), relevant, not_relevant, n) == 'Relevant':
            relevant_sentences.append(sentence)

    return relevant_sentences

def export_relevance(relevant, not_relevant):
    f = open('relevant-data.dat','wb')
    pickle.dump(relevant, f)
    f.close()

    f = open('not-relevant-data.dat','wb')
    pickle.dump(not_relevant, f)
    f.close()

def main():
    n = 1 #how many terms in n-gram
    
    relevant = {}
    rel_docs = []
    not_relevant = {}
    not_rel_docs = []
    
    
    f = open('classifier-relevant.txt','r')
    for line in f:
        line = prepare_sentence(line)
        rel_docs.append(line)
        ngrams = get_ngrams(line,n)
        relevant = update_ngram_count(ngrams, relevant)
    f.close()
    
    f = open('classifier-notrelevant.txt','r')
    for line in f:
        line = prepare_sentence(line)
        not_rel_docs.append(line)
        ngrams = get_ngrams(line,n)
        not_relevant = update_ngram_count(ngrams, not_relevant)
    f.close()

    rel_word_total = sum_ngram_count(relevant)
    not_rel_word_total = sum_ngram_count(not_relevant)

    rel_class_prob = float( len(rel_docs)) / (len(rel_docs)+len(not_rel_docs))
    not_rel_class_prob = float( len(not_rel_docs)) / (len(rel_docs)+len(not_rel_docs))

    relevant = get_ngram_probabilities(relevant, rel_class_prob)
    not_relevant = get_ngram_probabilities(not_relevant, not_rel_class_prob)

    print "Top 10 n-grams in 'relevant' class:\n"
    for i in sorted(relevant.iteritems(), key=lambda (k,v):(v,k), reverse = True)[:10]:
        print i
    print "Total number of tokens in 'relevant' class:", rel_word_total, '\n'

    print "Top 10 n-grams in 'not relevant' class:\n"
    for i in sorted(not_relevant.iteritems(), key=lambda (k,v):(v,k), reverse = True)[:10]:
        print i
    print "Total number of tokens in 'not relevant' class:", not_rel_word_total, '\n'

    review = ['7th time here and still has great service and friendly staff members.','This time around my cauliflower side was undercooked and had water in the bottom and was sent back.',"The Brussel sprouts were some of the best I've ever had, compared to Uchi in Austin's which are just as good.",'This time around I tried the lamb which is EH ok','would not order it again.',"Had little to no flavor and it didn't have a demi-glaze or anything to give it that BANG just kind of lamb chops on a plate....","Now the Lusty Lucy drink and cowboy rib-eye you can't go wrong with."]
    for s in get_relevant_sentences(review, relevant, not_relevant, n):
        print s + "\n"

    export_relevance(relevant, not_relevant)


if __name__ == '__main__':
    main()
