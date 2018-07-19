"""This module implements the WordSub class, modelled after a recipe
in "Python Cookbook" (Recipe 3.14, "Replacing Multiple Patterns in a
Single Pass" by Xavier Defrang).

Usage:
Use this class like a dictionary to add before/after pairs:
    > subber = TextSub()
    > subber["before"] = "after"
    > subber["begin"] = "end"
Use the sub() method to perform the substitution:
    > print( subber.sub("before we begin") )
    after we end
All matching is intelligently case-insensitive:
    > print( subber.sub("Before we BEGIN") )
    After we END
The 'before' words must be complete words -- no prefixes.
The following example illustrates this point:
    > subber["he"] = "she"
    > print( subber.sub("he says he'd like to help her") )
    she says she'd like to help her
Note that "he" and "he'd" were replaced, but "help" and "her" were
not.
"""

from __future__ import print_function


# 'dict' objects weren't available to subclass from until version 2.2.
# Get around this by importing UserDict.UserDict if the built-in dict
# object isn't available.
try: dict
except: from UserDict import UserDict as dict

import re
import string
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

class WordSub(dict):
    """All-in-one multiple-string-substitution class."""

    def _wordToRegex(self, word):
        """Convert a word to a regex object which matches the word."""
        if word != "" and word[0].isalpha() and word[-1].isalpha():
            return "\\b%s\\b" % re.escape(word)
        else: 
            #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            return r"\b%s\b" % re.escape(word)
    
    def _update_regex(self):
        """Build re object based on the keys of the current
        dictionary.

        """
        #self._regex = re.compile("|".join(map(self._wordToRegex, self.keys())))
        temp_default = []
        for d in self._defaults:
            temp_default.append(d[0])
        self._regex = re.compile("|".join(map(self._wordToRegex, temp_default)))
        self._regexIsDirty = False

    def __init__(self, defaults = []):
        """Initialize the object, and populate it with the entries in
        the defaults dictionary.

        """
        self._regex = None
        self._regexIsDirty = True
        self._defaults = defaults
        for d in self._defaults:
            self[d[0]] = d[1]

    def __call__(self, match):
        """Handler invoked for each regex match."""
        return self[match.group(0)]

    """def __setitem__(self, i, y):
        self._regexIsDirty = True
        # for each entry the user adds, we actually add three entrys:
        super(type(self),self).__setitem__(i.lower(),y.lower()) # key = value
        super(type(self),self).__setitem__(string.capwords(i), string.capwords(y)) # Key = Value
        super(type(self),self).__setitem__(i.upper(), y.upper()) # KEY = VALUE"""
   
    def capitalise_i(self, response):
        cap_i = {'i ':'I ',' i ':' I ',' i':' I'}
        pattern = re.compile("|".join(map(re.escape, cap_i.keys())))
        result = pattern.sub(lambda mo: cap_i[mo.string[mo.start():mo.end()]], response)
        return result

    def sub(self, text, called_from='normal'):
        """Translate text, returns the modified text."""
        inp = text.lower()
        if self._regexIsDirty:
            self._update_regex()
        result = self._regex.sub(self, inp)
        return result
