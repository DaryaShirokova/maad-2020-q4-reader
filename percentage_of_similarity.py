import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words


stop_words = get_stop_words('english')


def clean_string(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text


def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)

    return cosine_similarity(vec1, vec2)[0][0]


s1 = "To Sherlock Holmes she is always THE woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind. He was, I take it, the most perfect reasoning and observing machine that the world has seen, but as a lover he would have placed himself in a false position. He never spoke of the softer passions, save with a gibe and a sneer. They were admirable things for the observer--excellent for drawing the veil from men's motives and actions. But for the trained teasoner to admit such intrusions into his own delicate and finely adjusted temperament was to introduce a distracting factor which might throw a doubt upon all his mental results. Grit in a sensitive instrument, or a crack in one of his own high-power lenses, would not be more disturbing than a strong emotion in a nature such as his. And yet there was but one woman to him, and that woman was the late Irene Adler, of dubious and questionable memory. I had seen little of Holmes lately. My marriage had drifted us away from each other. My own complete happiness, and the home-centred interests which rise up around the man who first finds himself master of his own establishment, were sufficient to absorb all my attention, while Holmes, who loathed every form of society with his whole Bohemian soul, remained in our lodgings in Baker Street, buried among his old books, and alternating from week to week between cocaine and ambition, " \
     "the drowsiness of the drug, and the fierce energy of his own keen nature. He was still, as ever, deeply attracted by the study of crime, and occupied his immense faculties and extraordinary powers of observation in following out those clews, and clearing up those mysteries which had been abandoned as hopeless by the official police. "

s2 = "to Sherlock Holmes she is always the woman I have seldom heard him " \
     "mention " \
     "or any other name in his eyes she eclipses and predominates the whole of her " \
     "sex " \
     "it was not that he felt any emotion akin to love for Irene Adler all " \
     "emotion " \
     "send that one particularly where at heart to his cold precise but " \
     "admirably " \
     "mind he was I take it the most perfect reasoning and observing machine that the " \
     "world has " \
     "but as a lover he would have placed himself in a false position he never " \
     "spoke " \
     "after passions save with a guy been a snare they were admirable things for the " \
     "Observer " \
     "excellent for drawing the veil from Men's motives and actions but for the " \
     "trained Reasoner to add " \
     "intrusions into his own delicate and finely adjusted temperament was to " \
     "introduce " \
     "correcting factor which might throw it out upon all this medal results in a " \
     "sense " \
     "cement or a crack in one of his own high power lenses would not be more " \
     "disturbing than a " \
     "emotion in a nature such as his and yet there was but one woman to " \
     "him " \
     "woman was the late Irene Adler of dubious and questionable memory " \
     "seen little of homes lately my marriage had drifted us away from each other my " \
     "own " \
     "happiness and the home centered interests which rise up around the man who first " \
     "finds himself " \
     "master of his own establishment what's the fishing to absorb all my attention " \
     "while home " \
     "who loads every form of society with his whole Bohemian Soul remained in " \
     "our " \
     "things in Baker Street buried among his old books and alternating from " \
     "week-to-week between " \
     "Kane and ambition the drowsiness of the drug and the fierce energy of its own " \
     "Keen " \
     "he was still has ever deeply attracted by the study of crime " \
     "an occupied his immense faculties and extraordinary powers of observation " \
     "pulling out those Clues and clearing up those Mysteries which had been abandoned " \
     "this Hopeless by the " \
     "police "


texts = [s1, s2]
cleaned = list(map(clean_string, texts))
vectorizer = CountVectorizer().fit_transform(cleaned)
vectors = vectorizer.toarray()
csim = cosine_similarity(vectors)


print(cosine_sim_vectors(vectors[0], vectors[1]))