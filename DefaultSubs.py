"""This file contains the default (English) substitutions for the
PyAIML kernel.  These substitutions may be overridden by using the
Kernel.loadSubs(filename) method.  The filename specified should refer
to a Windows-style INI file with the following format:

    # lines that start with '#' are comments

    # The 'gender' section contains the substitutions performed by the
    # <gender> AIML tag, which swaps masculine and feminine pronouns.
    [gender]
    he = she
    she = he
    # and so on...

    # The 'person' section contains the substitutions performed by the
    # <person> AIML tag, which swaps 1st and 2nd person pronouns.
    [person]
    I = you
    you = I
    # and so on...

    # The 'person2' section contains the substitutions performed by
    # the <person2> AIML tag, which swaps 1st and 3nd person pronouns.
    [person2]
    I = he
    he = I
    # and so on...

    # the 'normal' section contains subtitutions run on every input
    # string passed into Kernel.respond().  It's mainly used to
    # correct common misspellings, and to convert contractions
    # ("WHAT'S") into a format that will match an AIML pattern ("WHAT
    # IS").
    [normal]
    what's = what is
"""

defaultGender = [
    # masculine -> feminine
    ["he", "she"],
    ["him", "her"],
    ["his", "her"],
    ["himself", "herself"],
    # feminine -> masculine
    ["she", "he"],
    ["her", "him"],
    ["hers", "his"],
    ["herself", "himself"],
]

defaultPerson = [
    ["with you", "with me"],
    ["with me", "with you"],
    ["to you", "to me"],
    ["to me", "to you"],
    ["of you", "of me"],
    ["of me", "of you"],
    ["for you", "for me"],
    ["for me", "for you"],
    ["give you", "give me"],
    ["give me", "give you"],
    ["giving you", "giving me"],
    ["giving me", "giving you"],
    ["gave you", "gave me"],
    ["gave me", "gave you"],
    ["make you", "make me"],
    ["make me", "make you"],
    ["made you", "made me"],
    ["made me", "made you"],
    ["take you", "take me"],
    ["take me", "take you"],
    ["save you", "save me"],
    ["save me", "save you"],
    ["tell you", "tell me"],
    ["tell me", "tell you"],
    ["telling you", "telling me"],
    ["telling me", "telling you"],
    ["told you", "told me"],
    ["told me" , "told you"],
    ["are you", "am I"],
    ["am i", "are you"],
    ["you are", "I am"],
    ["i am", "you are"],
    ["i was", "you were"],
    ["you were", "I was"],
    ["your", "my"],
    ["my", "your"],
    ["yours", "mine"],
    ["mine", "yours"],
    ["yourself", "myself"],
    ["myself", "yourself"],
    ["you", "me"],
    ["me", "you"],
    ["i", "you"],
]

defaultPerson2 = [
    ["i was", "he or she was"],
    ["he was", "I was"],
    ["she was", "I was"],
    ["i am", "he or she is"],
    ["i", "he or she"],
    ["me", "him or her"],
    ["my", "his or her"],
    ["myself", "him or herself"],
    ["mine", "his or hers"],
]


# TODO: this list is far from complete
defaultNormal = [
    ["wanna", "want to"],
    ["gonna", "going to"],

    ["i'm", "I am"],
    ["i'd", "I would"],
    ["i'll", "I will"],
    ["i've", "I have"],
    ["you'd", "you would"],
    ["you're", "you are"],
    ["you've", "you have"],
    ["you'll", "you will"],
    ["he's", "he is"],
    ["he'd", "he would"],
    ["he'll", "he will"],
    ["she's", "she is"],
    ["she'd", "she would"],
    ["she'll", "she will"],
    ["we're", "we are"],
    ["we'd", "we would"],
    ["we'll", "we will"],
    ["we've", "we have"],
    ["they're", "they are"],
    ["they'd", "they would"],
    ["they'll", "they will"],
    ["they've", "they have"],

    ["y'all", "you all"],

    ["can't", "can not"],
    ["cannot", "can not"],
    ["couldn't", "could not"],
    ["wouldn't", "would not"],
    ["shouldn't", "should not"],

    ["isn't", "is not"],
    ["ain't", "is not"],
    ["don't", "do not"],
    ["aren't", "are not"],
    ["won't", "will not"],
    ["weren't", "were not"],
    ["wasn't", "was not"],
    ["didn't", "did not"],
    ["hasn't", "has not"],
    ["hadn't", "had not"],
    ["haven't", "have not"],

    ["where's", "where is"],
    ["where'd", "where did"],
    ["where'll", "where will"],
    ["who's", "who is"],
    ["who'd", "who did"],
    ["who'll", "who will"],
    ["what's", "what is"],
    ["what'd", "what did"],
    ["what'll", "what will"],
    ["when's", "when is"],
    ["when'd", "when did"],
    ["when'll", "when will"],
    ["why's", "why is"],
    ["why'd", "why did"],
    ["why'll", "why will"],

    ["it's", "it is"],
    ["it'd", "it would"],
    ["it'll", "it will"],
]
