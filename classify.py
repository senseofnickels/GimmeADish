import pickle
import json
import re
import MySQLdb
import time

def load_relevance(rel_file, not_rel_file):
    f = open(rel_file,'rb')
    relevant = pickle.load(f)
    f.close()

    f = open(not_rel_file, 'rb')
    not_relevant = pickle.load(f)
    f.close()
    return relevant, not_relevant

def prepare_sentence(sentence):
    sentence = re.sub(r'[^\w^\s]', '', sentence)
    return sentence

def remove_stop_words(tokens):
    stopwords = ['the','a','of','is','was','and','be', 'to', 'as', 'my', 'for', 'i', 'it', 'in']
    tokens = [ t for t in tokens if t not in stopwords]
    return tokens

def remove_stop_words_second(tokens):
    stopwords = ['had','few','piece','pieces','other','enjoy','packed','with','good','your','its','cooked','nothing','selection','decent','bar','quality','ive','drive','eaten','all','perfect','perfectly','each','loved','tasty','tasted','wasn','fun','pretty','layer','layers','dishes','recommend','delicious','variety','main','been','one','two','sides','some','still','done','tum','he','tried','an','has','ever','use','them','only','there','after','this','his','from','first','or','bland','best','no','idea','great','once','not','you','why','what','wife','stars','pricey','value','food','tastes','worst','taste','our','have','than','nice','yummy','through','take','well','that','but','order','ordered','their','she','like','yum','ok','time','went','they','here','are','were','very','fresh','ve','which','we','got','dish','lunch','dinner','breakfast','on','so','always','too','t','also','just','really','re','s']
    tokens = [ t for t in tokens if t not in stopwords]
    return tokens


def get_tokens(sentence):
    return [str(word) for word in re.findall(r'\w+', sentence.lower())]

def get_ngrams(sentence, n=1):
    start = '<'
    end = '>'
    tokens = get_tokens(sentence)
    tokens = remove_stop_words(tokens)
    if len(tokens) == 0:
        return []
    for i in range(n-1):
        tokens.insert(0, start)
        tokens.append(end)
    return zip(*[tokens[i:] for i in range(n)])

def predict_class(sentence, relevant, not_relevant, n):
    rel_prob = 0.0
    not_rel_prob = 0.0

    ngrams = get_ngrams(sentence, n)

    for ngram in ngrams:
        #print ngram
        
        if ngram in relevant:
            #print 'Relevant:', relevant[ngram]
            rel_prob += relevant[ngram]
        else:
            #print 'Relevant:(unseen)', relevant['*']
            rel_prob += relevant['*']

        if ngram in not_relevant:
            #print 'Not Relevant:', not_relevant[ngram]
            not_rel_prob += not_relevant[ngram]
        else:
            #print 'Not Relevant:(unseen)', not_relevant['*']
            not_rel_prob += not_relevant['*']

    #print 'Probability that sentence is relevant:', rel_prob
    #print 'Probability that sentence is not relevant:', not_rel_prob

    if rel_prob > not_rel_prob:
        return True
    else:
        return False

def get_sentences_from_json(json_review):
    return [s.strip() for s in re.split(r'[.!;?]+', json_review['text']) if s != '']

def get_relevant_sentences(review, relevant, not_relevant, n):
    relevant_sentences = []
    for sentence in review:
        if predict_class(prepare_sentence(sentence), relevant, not_relevant, n):
            relevant_sentences.append(sentence)
    return relevant_sentences

def sort_tf(tf):
    return sorted(tf.iteritems(), key=lambda(k,v):(v,k), reverse = True)

def update_tf(tf, sentences):
    for sentence in sentences:
        tokens = get_tokens(sentence)
        tokens = remove_stop_words(tokens)
        tokens = remove_stop_words_second(tokens)
        for token in tokens:
            if token in tf.keys():
                tf[token] += 1
            else:
                tf[token] = 1
    return tf

def isolate_full_term(token, rel_sentences, num_neighbors=4):
    #token = term to search around
    #rel_sentences = relevant sentences containing token
    #num_neighbors = distance to look nearby
    threshold = 2 #minimum number of common terms required to report

    #print token, rel_sentences

    #iterate through sentences containing token, get n-gram terms, update frequency
    tf = {}
    for sentence in rel_sentences:
        sentence = prepare_sentence(sentence)
        tokens = get_tokens(sentence)
        tokens = remove_stop_words(tokens)
        tokens = remove_stop_words_second(tokens)
        candidates = []
        #for loop gets n-grams for 2...num_neighbors
        for num_n in range(2, num_neighbors+2):
            #get n-grams 
            candidates = zip(*[tokens[i:] for i in range(num_n)])
            for candidate in candidates:
                #if target token is in candidate term, update frequency
                if token in candidate:
                    if candidate in tf:
                        tf[candidate] += 1
                    else:
                        tf[candidate] = 1

    #remove terms below threshold                    
    for term in tf.keys():
        if tf[term] < threshold:
            del tf[term]
            
    #get sorted list and return
    tf = sort_tf(tf)
    #sort secondarily by term token count
    tf.sort(key = lambda t: len(t[0]),reverse = True)
    return tf

def main():
    starttime = time.time()
    print 'Program started at', starttime
    n = 1 #DO NOT CHANGE--DEPENDENT ON CLASSIFIER DATA number of tokens used for classification

    #load classifier data
    relevant, not_relevant = load_relevance('relevant-data.dat', 'not-relevant-data.dat')

    #prepare database
    db = MySQLdb.connect(host="gimmeadish.chxtcfopqjbt.us-west-2.rds.amazonaws.com",
                         port=3306,
                         user="nicholsm",
                         passwd="csce470ISR")
    cur = db.cursor()
    
    cur.execute("DROP DATABASE IF EXISTS nicholsm;")
    cur.execute("CREATE DATABASE nicholsm;")
    cur.execute("USE nicholsm;")
    cur.execute("CREATE TABLE reviews (bus_id varchar(32) NOT NULL, dish_id int, dish_text varchar(50), dish_freq int, dish_reviews varchar(2000), token_results varchar(500));")
    cur.execute("CREATE TABLE rests (bus_id varchar(32) NOT NULL, name varchar(50), location varchar(50));");
    cur.execute("CREATE TABLE cats (bus_id varchar(32) NOT NULL, category varchar(50));")

    print 'created database schema'

    
    print 'Loading business listings (bus_id, city, name, categories)...'
    #load business listings
    f = open('restaurant_listings.json','r')
    rests = {} #maps business_id to name, city, and categories[]
    for line in f:
        decoded = json.loads(line)
        bus_id = decoded['business_id'].encode('ascii','ignore')
        city = decoded['city'].encode('ascii','ignore')
        name = decoded['name'].encode('ascii','ignore')
        categories = [s.encode('ascii','ignore') for s in decoded['categories']]
        rests[bus_id] = (name, city, categories)
    f.close()
    print 'Done.'

    print 'Loading business reviews...'
    #load business reviews
    f = open('restaurant_reviews.json', 'r')

    n_dishes = 1 #number of dishes to enter into database per restaurant
    n_dishreviews = 1 #number of review sentences per dish
    n_threshold = 3 #minimum number of dish term instances required to enter into database

    prev_bus_id = ''
    tf = {}
    reviews = []

    #statistical information
    stat_reviews = 0
    #stat_sentences = 0
    #stat_tokens = 0
    #total_tokens = {}
    #stat_relevant = 0

    #iterate through reviews
    for line in f:
        stat_reviews += 1
        if stat_reviews % 1000 == 0:
            print 'Reviews Processed: ' + str(stat_reviews)
            totsec = int(time.time() - starttime)
            hh = totsec / (60*60)
            totsec = totsec - 60*60*hh
            mm = totsec / 60
            totsec = totsec - 60*mm
            ss = totsec
            
            print 'Time elapsed: ' + str(hh) + 'h' + str(mm) + 'm' + str(ss) + 's'
            #print 'Sentences Processed: ' + str(stat_sentences)
            #print 'Relevant Sentences: ' + str(stat_relevant)
            #print 'Tokens Processed: ' + str(stat_tokens)
            #print ''
            db.commit()
        decoded = json.loads(line)
        bus_id = decoded['business_id'].encode('ascii','ignore')

        if bus_id != prev_bus_id: #we're at a different business, wrap up processing and add to database
            tf = sort_tf(tf)
            num_dishes = min(n_dishes, len(tf)) #iterate through tf list until maximum number of dishes is reached
            for i in range(num_dishes):
                #get reviews mentioning the token tf[i][0]
                dish_reviews = []
                
                for rev in reviews:
                    if tf[i][0] in prepare_sentence(rev).lower():
                        dish_reviews.append(rev.encode('ascii','ignore'))

                #isolate terms
                common_terms = isolate_full_term(tf[i][0], dish_reviews)

                dish_reviews = dish_reviews[0:min(len(dish_reviews),n_dishreviews)]
                token_results = []
                token_results.extend([ t for t in common_terms])
                token_results.extend([([t[0]],t[1]) for t in tf])
                token_results.sort(key = lambda t: (len(t[0])*len(t[0])*t[1]),reverse = True)
                token_results = token_results[:5]
                
                #add prev_bus_id, dish_id (i), dish_text (tf[i][0]), freq (tf[i][1]), dish_reviews.flatten
                if tf[i][1] >= n_threshold:
                    if i == 0: #only insert rests/cats once (if any terms pass threshold)
                        cur.execute('INSERT INTO rests VALUES (%s, %s, %s);', (prev_bus_id, rests[prev_bus_id][0], rests[prev_bus_id][1]))
                        for cat in rests[prev_bus_id][2]:
                            if cat not in ['Restaurants', 'Food','Bars','Nightlife','Lounges','Party & Event Planning','Event Planning & Services','Venues & Event Spaces','Active Life','Bowling','Pubs','Dive Bars','Dance Clubs','Sports Bars','Tea Rooms','Arts & Entertainment','Music Venues','Wine Bars','Grocery','Karaoke','Shopping Centers','Shopping','Outlet Stores','Caterers','Convenience Stores','Drugstores','Gastropubs','Hotels & Travel','Hotels','Jazz & Blues','Breweries','Performing Arts','Beer, Wine & Spirits','Fashion','Sporting Goods','Sports Wear','Cinema','Arcades','Pool Halls','Casinos','Food Delivery Services','Gift Shops','Flowers & Gifts','Health & Medical','Hospitals','Hookah Bars','Amusement Parks','Food Stands','Personal Chefs','Adult Entertainment','Herbs & Spices','Beauty & Spas','Gyms','Medical Spas','Fitness & Instruction','Day Spas','Specialty Schools','Cooking Schools','Colleges & Universities','Education','RV Parks','Automotive','Airports','Tours','Cafeteria','Champagne Bars','Wineries','Health Markets','Arts & Crafts','Landmarks & Historical Buildings','Personal Shopping','Public Services & Government','Festivals','Swimming Pools','Leisure Centers','Piano Bars','Internet Cafes','Kids Activities','Car Wash','Food Court','Beer Bar','Butcher','Country Dance Halls','Cultural Center','Golf']:
                                cur.execute('INSERT INTO cats VALUES (%s, %s);', (prev_bus_id, cat))
                    
                    #get sentences containing terms
                    term_reviews = []
                    for rev in reviews:
                        if ''.join(map(str,[x for x in token_results[0][0]])) in ''.join(map(str,get_tokens(prepare_sentence(rev)))):
                            term_reviews.append(rev.encode('ascii','ignore'))
                    term_reviews = term_reviews[0:min(len(term_reviews),n_dishreviews)]
                    term = ''.join(tuple_elem + ' ' for tuple_elem in token_results[0][0])
                    term_freq = token_results[0][1]
                    token_results_string = ""
                    for token_group in token_results:
                        token_results_string += '"' + ' '.join(x for x in token_group[0]) + '": ' + str(token_group[1]) + ' (x #tokens^2 = ' + str(len(token_group[0])*len(token_group[0])*token_group[1]) + ')<br>'
                    
                    cur.execute('INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s);', (prev_bus_id,str(i),term,term_freq,''.join(r+"\n" for r in term_reviews),token_results_string))
            tf = {}
            reviews = []
            prev_bus_id = bus_id
        
        review = get_sentences_from_json(decoded)
        #total_tokens = update_tf(total_tokens, review)
        #for tfkey in total_tokens.keys():
        #    stat_tokens += total_tokens[tfkey]
        #total_tokens = {}
        #stat_sentences += len(review)
        rel_sentences = get_relevant_sentences(review, relevant, not_relevant, n)
        #stat_relevant += len(rel_sentences)
        tf = update_tf(tf, rel_sentences)
        reviews.extend(rel_sentences)
    f.close()

    print 'Reviews Processed: ' + str(stat_reviews)
    #print 'Sentences Processed: ' + str(stat_sentences)
    #print 'Relevant Sentences: ' + str(stat_relevant)
    #print 'Tokens Processed: ' + str(stat_tokens)
    #print ''

    db.commit()
    
    
    pass

if __name__ == '__main__':
    main()
