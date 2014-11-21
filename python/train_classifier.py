import re
import math

def remove_stop_words(tokens):
    stopwords = ['the','a','of','is','was','and','be', 'to', 'as', 'my', 'for', 'i', 'it',]

    tokens = [ t for t in tokens if t not in stopwords]
    return tokens

def get_ngrams(sentence, n=1):
    start = '<'
    end = '>'
    #tokenize
    tokens = [str(word) for word in re.findall(r'\w+', sentence.lower())]
    #tokens = remove_stop_words(tokens)
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

def main():
    n = 2 #how many terms in n-gram
    
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

    sentence = ''
    while sentence != 'q':
        sentence = raw_input("Enter a sentence to test (or 'q' to quit): ")
        print predict_class(prepare_sentence(sentence), relevant, not_relevant, n)


if __name__ == '__main__':
    main()
