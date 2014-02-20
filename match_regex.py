import re

'''
    Match a composed expression

    Example
        (traffic OR car OR vehicle)
        AND
        (accident OR collision OR crash)

    composed = [
        ['traffic', 'car', 'vehicle'],
        ['accident', collision','crash']
        ]

    February 11, 2014
    Sibelius Seraphini
'''
def match_regex(text, composed):
    text = text.lower() # Transform the text to lower case
    # \b - word boundary
    # Compile a regular expression for each OR group
    compiled = [re.compile('(\\b' + '\\b|\\b'.join(or_group) + '\\b)')
        for or_group in composed]

    match = True

    # Test each OR group
    for c in compiled:
        if c.search(text) == None: # Search for the regular expression of the OR group
            match = False
            break

    return match
