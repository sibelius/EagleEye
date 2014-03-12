'''

 Sibelius Seraphini
'''

import networkx as nx
import re

def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|VIA)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [ source.strip()
            for tuple in rt_patterns.findall(tweet)
                for source in tuple
                    if source not in ("RT", "via") ]


if __name__ == '__main__':
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
