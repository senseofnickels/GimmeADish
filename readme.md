Gimme A Dish! is a Yelp review processor which isolates what people are saying about particular dishes at a restaurant.

[classify.py]
This script loads the classifier probabilities created for the two classes ('relevant' and 'not-relevant') created with the train_classifier.py script. It then iterates through the dataset reviews, finding a list of relevant sentences for a given restaurant by using the Naive Bayes classifier. The relevant sentences are then used to build a term frequency table. The most frequently mentioned term is selected. We then build a list of reviews that mention the term, and iterate through the reviews building multiple n-grams with the words located before and after the select term. These n-grams are then used to build a second term frequency table. The purpose of the n-grams is to find full dish names in cases where it consists of multiple words. The n-grams and terms are then passed through a weighting function (score = tf * (# tokens in term)^2) that gives longer chains of repeating token sequences a higher score per term instance (purpose behind this is that longer chains of matched words are less likely, and thus more significant).

The results for each restaurant are then submitted to a MySQL database which will be queried by the website UI.


[train_classifier.py]
This script trains the classifier from a set of 'relevant' and a set of 'not-relevant' sample data (sentences output from process.py). This script loads 'classifier-relevant.txt' and 'classifier-notrelevant.txt' and builds a training set for the relevant and not-relevant classes.

After loading and training the classifier, it prompts the user to enter a sentence for classification. It then uses Naive Bayes (modified for n-gram structure) to classify the sentence into one of the two classes: relevant (reviewer talks about ordering a specific food item) and not relevant (reviewer talks about other things, like the atmosphere/cleanliness/random/generalizations of the food). It gives the result (with probabilities in logarithmic form, being added together) as well as showing the properties' probability contributions.

Our intent is to use this to isolate the sentences where people are talking about one of the restaurant's food items, and later work in our project will provide some linguistic processing to pull the food names from the classified sentences.


[filter_dataset.py]
This script filters from the files 'yelp_academic_dataset_business.json' and 'yelp_academic_dataset_review.json' only the reviews that are for restaurants. It expects that the files are located in the same folder as the script. It should take around 10 minutes or so, and will generate two new files called 'restaurant_listings.json' (~17 MB) and 'restaurant_reviews.json' (~620 MB).

It isn't necessary that you run this again, unless you want to run 'process.py' also. Neither of these are exactly necessary for the classifier to run, but were used for us to build the training set.


[build_training_sets.py]
This script is used to build the classifier's training set. When run, the script prompts the user for a start and end range in the list of reviews to process. It then loads the reviews in the range, splits them up into sentences, and asks the user to determine if the sentence is relevant or not (i.e. does it mention a specific food that the reviewer ordered). Once all selected reviews are processed, it produces two files beginning with the prefixes ('classifier-relevant' or 'classifier-notrelevant') and ending with the range of reviews it contains, e.g. 'classifier-relevant-0-20.txt' or 'classifier-relevant-22045-22070.txt'.

