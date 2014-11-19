import json
from math import sqrt

def gather_restaurants():
    rests = []
    busIDs = []
    reviews = []

    print 'Gathering business entries where \'categories\' contains \'Restaurants\'...'
    
    f = open('yelp_academic_dataset_business.json', 'r')
    out = open('restaurant_listings.json', 'w')
    i = 0
    for line in f:
        i+=1
        decoded = json.loads(line)
        if 'Restaurants' in decoded['categories']:
            rests.append(decoded)
            busIDs.append(decoded['business_id'])
            json.dump(decoded, out)
            out.write('\n')

    print 'Done. Found', len(rests), 'matches out of', i, 'entries.'

    f.close()
    out.close()
    
    f = open('yelp_academic_dataset_review.json', 'r')

    print 'Gathering reviews where \'business_id\' is in list of restaurants...'
    numrestrevs = 0
    out = open('restaurant_reviews.json', 'w')
    i = 0
    for line in f:
        i+=1
        decoded = json.loads(line)
        if decoded['business_id'] in busIDs:
            json.dump(decoded, out)
            out.write('\n')
            numrestrevs += 1
    f.close()
    out.close()
    
    print len(reviews)
    print 'Done. Found', numrestrevs, 'matches out of', i, 'reviews.'
    
    
if __name__ == '__main__':
    gather_restaurants()
