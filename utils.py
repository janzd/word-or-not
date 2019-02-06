import os, glob

from config import chars

def read_words(filepaths):
    if type(filepaths) == list:
        words = []
        for filepath in filepaths:
            with open(filepath) as f:
                words.extend([word.strip().upper() for word in f.readlines()])
    else:
        with open(filepaths) as f:
            words = [word.strip().upper() for word in f.readlines()]
    return words

def replace_chars(word):
    replacement = ['A', 'I', 'U', 'E', 'O', 'Y', 'N', 'A', '‘', 'AE']
    before = word
    for i, c in enumerate(['Ä', 'Ï', 'Ü', 'Ë', 'Ö', 'Ÿ', 'Ñ', 'Ã', "'", 'Œ']):
        if c in word:
            indices = [i for i, x in enumerate(word) if x == c]
            for ix in indices:
            	if c == 'Œ':
            		word = word[:ix] + ['A'] + ['E'] + word[ix+1:]
            	else:
                    word[ix] = replacement[i]
    return word

def remove_chars(word):
    chars_to_remove = ['-', '—', '”', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '_', '?', '\\', '!', '/', '=', '&', '(', ')', '<', ']', '+']
    for c in chars_to_remove:
        while c in word:
            word.remove(c)
    return word

def convert_to_char_seq(word):
    word = list(word)
    #print(word)
    word = replace_chars(word)
    word = remove_chars(word)
    #print(word)
    word = [chars.index(char) + 1 for char in word]
    return word

def get_longest_word_length(words):
    longest_word_length = 0
    for word in words:
        if len(word) > longest_word_length:
            longest_word_length = len(word)
    return longest_word_length

def pad_word(word, output_length):
    while len(word) < output_length:
        word.append(0)
    return word

def pad_words(words):
    longest_word_length = get_longest_word_length(words)
    words = [pad_word(word, longest_word_length) for word in words]
    return words

def create_result_subdir(result_dir):

    # Select run ID and create subdir.
    while True:
        run_id = 0
        for fname in glob.glob(os.path.join(result_dir, '*')):
            try:
                fbase = os.path.basename(fname)
                ford = int(fbase)
                run_id = max(run_id, ford + 1)
            except ValueError:
                pass

        result_subdir = os.path.join(result_dir, '%03d' % (run_id))
        try:
            os.makedirs(result_subdir)
            break
        except OSError:
            if os.path.isdir(result_subdir):
                continue
            raise

    return result_subdir