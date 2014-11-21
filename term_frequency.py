import json
import re

def termcount():
    tf = {}
    
    f = open('restaurant_reviews.json', 'r')
    out = open('term_frequency.txt', 'w')
    
    for line in f:
        decoded = json.loads(line)
        text = decoded['text']
        tokens = [str(word) for word in re.findall(r'\w+', text.lower())]

        for token in tokens:
            if token in tf:
                tf[token] += 1
            else:
                tf[token] = 1

    tfsort = sorted(tf.iteritems(), key=lambda (k,v): (v,k))
    out.write(str(tfsort))

    f.close()
    out.close()
    
    
if __name__ == '__main__':
    termcount()
