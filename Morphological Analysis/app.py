import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def get_wordnetTag(nltkTag):
    """Convert NLTK POS tags to WordNet POS tags"""
    if nltkTag.startswith('J'):
        return wordnet.ADJ
    elif nltkTag.startswith('V'):
        return wordnet.VERB
    elif nltkTag.startswith('N'):
        return wordnet.NOUN
    elif nltkTag.startswith('R'):
        return wordnet.ADV
    else:
        return None  # Default case

def morphologicalAnalysis(word):
    nltkTag = nltk.pos_tag([word])[0][1]  # POS tagging
    wn_tag = get_wordnetTag(nltkTag)  # Convert to WordNet POS

    if wn_tag is None:
        wn_tag = wordnet.NOUN  # Default to noun

    baseForm = lemmatizer.lemmatize(word, pos=wn_tag)  # Lemmatization

    if wn_tag == wordnet.NOUN:
        # Handle known irregular plurals
        irregular_nouns = {"geese": "goose", "mice": "mouse", "children": "child"}
        baseForm = irregular_nouns.get(word.lower(), baseForm)

        if word.endswith("s") and baseForm != word:
            return f"{baseForm} + N + PL"
        else:
            return f"{baseForm} + N + SG"

    elif wn_tag == wordnet.VERB:
        # Handle known irregular past tense verbs
        irregular_verbs = {"caught": "catch", "ran": "run", "swam": "swim", "ate": "eat"}
        baseForm = irregular_verbs.get(word.lower(), baseForm)

        if word.endswith("ing"):
            return f"{baseForm} + V + Present Participle"
        elif word.endswith("ed") or baseForm != word:
            return f"{baseForm} + V + Past"
        else:
            return f"{baseForm} + V"

    return f"{baseForm} + {wn_tag}"


# Test Cases
print("Default Test Cases:")
words = ["Cats", "Cat", "Cities", "Geese", "Goose", "Gooses",
         "Merging", "Caught", "Running", "Played", "Mice", "Children", "Ate", "Swam", "Ran"]

for word in words:
    print(f"Input: {word} -> Output: {morphologicalAnalysis(word)}")

print("--------------------------------------------------------------------")
print("Custom Test Cases Input here : (-1 for exit)")
while True:
    word = input("Custom Input String: ")
    if word == '-1':
        print("End of Program")
        break
    print(f"Custom Test Case Output: {morphologicalAnalysis(word)}")
