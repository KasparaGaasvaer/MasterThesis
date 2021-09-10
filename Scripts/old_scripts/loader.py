import numpy as np
import os
import gzip
import shutil
from scipy.io import loadmat

class Loader:
    """
    def __init__(self, tweettype):
        keys = ["created_at", "id", id_str, text, source, truncated, in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, in_reply_to_screen_name, user, coordinates, place, quoted_status_id, quoted_status_id_str, is_quote_status, quoted_status, retweeted_status, quote_count, reply_count, retweet_count, favorite_count, entities, extended_entities, favorited,retweeted, possibly_sensitive, filter_level, lang, matching_rules, current_user_retweet,scopes, withheld_copyright, withheld_in_countries, withheld_scope, geo]
    """

    def __init__(self, fname):
        self.matname = fname
        matr = loadmat(fname)
