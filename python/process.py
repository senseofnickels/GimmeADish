import json
import re

def get_restaurant_listings():
#returns a dictionary for fast cross-lookup from reviews
#key = business_id, value = listing json

    print "Loading restaurant listings..."

    f = open('restaurant_listings.json', 'r')
    listings = {}
    for line in f:
        decoded = json.loads(line)
        listings[decoded['business_id']] = decoded

    f.close()
    print "Done."
    return listings 

def get_restaurant_reviews(start = -1, limit = -1):
#returns a dictionary for fast cross-lookup from listings
#key = business_id, value = list of review jsons

    print "Loading restaurant reviews..."

    f = open('restaurant_reviews.json', 'r')
    
    reviews = {}
    i = -1
    for line in f:
        i+=1
        if i < start and start != -1:
            continue
        if i == limit and limit != -1:
            break
        
        decoded = json.loads(line)
        bus_id = decoded['business_id']
        if bus_id in reviews:
            reviews[bus_id].append(decoded)
        else:
            reviews[bus_id] = [decoded]

    f.close()
    print "Done."
    return reviews

def update_tf(tf_dict, full_string):
#returns an updated term frequency dictionary by tokenizing the given text
    tokens = [str(word) for word in re.findall(r'\w+', full_string.lower())]

    for token in tokens:
        if token in tf_dict:
            tf_dict[token] += 1
        else:
            tf_dict[token] = 1
            
    return tf_dict

def sort_tf(tf_dict):
#sorts the dictionary by value, highest to lowest
    s = sorted(tf_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)

    return s

def build_relevant_lists(sentences):
#returns a list of 'relevant' sentences and a list of 'not_relevant' sentences
    relevant = []
    not_relevant = []
    unsure = []

    print 'Full Review:'
    print sentences
    for sentence in sentences:
        print "\n'" + sentence + "'"
        choice = ''
        while choice != 'y' and choice != 'n' and choice != 'u':
            choice = raw_input('Is this sentence relevant? (y/n/u[nsure]) ')
            if choice == 'y':
                relevant.append(sentence)
            elif choice == 'n':
                not_relevant.append(sentence)
            elif choice == 'u':
                unsure.append(sentence)
    
    return relevant, not_relevant

def get_sentences_from_json(json_review):
    return [s.strip() for s in re.split(r'[.!;?]+', json_review['text']) if s != '']

def remove_stopwords(tf):
    sw = open('stoplist', 'r')

    sw.close()

def main():
    start = int(raw_input('Enter review number to start with: '))
    limit = int(raw_input('Enter review number to end with (or -1 to get all remaining reviews): '))
    
    listings = get_restaurant_listings()
    reviews = get_restaurant_reviews(start, limit)

    #[ {listing_verbatim}, {reviews_verbatim}, {termfreq}, [relev], [not_relev] ]
    tf = {}
    relevant = []
    not_relevant = []
    print 'Reviews loaded for: ' + str(reviews.keys())

    i = 0
    for reviewset in reviews.keys():
        for review in reviews[reviewset]:
            i += 1
            print '-----------------------------------------------------------'
            print '\n(Review '+str(i)+' of '+ str(limit - start) + ')'
            tf = update_tf(tf, review['text'])
            sentences = get_sentences_from_json(review)
            rel, not_rel = build_relevant_lists(sentences)
            relevant.extend(rel)
            not_relevant.extend(not_rel)

    #print relevants
    rel_filename = 'classifier-relevant-' + str(start) + '-' + str(limit) + '.txt'
    print 'Saving relevant sentences to ' + rel_filename
    rel_out = open(rel_filename, 'w')
    for rel in relevant:
        rel_out.write(rel + '\n')
    rel_out.close()

    #print not_relevants
    nrel_filename = 'classifier-notrelevant-' + str(start) + '-' + str(limit) + '.txt'
    print 'Saving non relevant sentences to ' + nrel_filename
    nrel_out = open(nrel_filename, 'w')
    for nrel in not_relevant:
        nrel_out.write(nrel + '\n')
    nrel_out.close()
    
if __name__ == '__main__':
    main()
