#!/usr/bin/env python3

from Conversation import Conversation
from time import strftime
import sys
import os
import re
import Utilities.ConvertDataType as conv
from TweetClass import TweetClass
from Utilities.FilePartition import make_partition, get_partition_range


"""
CollectActiveTweets.py: From a captured set of conversations (Verified Media Personalities - VMP) the script extract a
                        list of handles that interacted in the conversations. If a list of deleted and suspended is 
                        provided, it removes those handles from the list. The final script objective is to retrieve
                        max number of tweets allowed via the Twitter API, and store those tweets in a given path. 
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Mar 30, 2018 at 10:38'
__email__ = 'pvargas@cs.odu.edu'


def main(**kwarg):
    """

    :param kwarg: a dictionary containing the path of the files where the deleted/suspended accounts will be stored.
                  path: is of the file where the capture conversations are stored.

                  sus_del_path: is the folder where the deleted and suspended account will be stored.
    :return: None

    """
    path = kwarg['path']
    path_tweets = kwarg['path_tweet']

    print('\nLoading conversations ...')
    observed = Conversation(path)

    interacting_handles = observed.all_conversation_elements_set()
    number_handles = len(interacting_handles)
    print('Number of Twitter accounts interacting in all conversations: {:,}'.format(number_handles))

    tweet = TweetClass(path_tweets, params['auth'])
    deleted_accounts = []
    suspended_accounts = []
    del_sus_accounts = []
    del_files = []
    sus_files = []
    regex_deleted = re.compile('deleted_\\d{8}\\..*')
    regex_suspended = re.compile('suspended_\\d{8}\\..*')

    if tweet.handle_with_tweets:
        print('\nNumber of Twitter accounts with recorded tweets: {}'.format(tweet.handle_with_tweets))

    else:
        print('\nCould not find any Twitter accounts with recorded tweets.')

    if 'del_path' in params:
        print('Obtaining deleted/suspended Twitter accounts from provided path: {}'.format(params['del_path']))

        del_sus_files = os.listdir(params['del_path'])
        if del_sus_files:
            # obtain deleted accounts
            del_files = [m.group(0) for l in del_sus_files for m in [regex_deleted.search(l)] if m]
            print('\nFound {} files with deleted accounts.'.format(len(del_files)))
            del_files.sort()
            updated_deletion = del_files[-1]
            print('Using most recent file <{}> to load deleted accounts ...'.format(updated_deletion))

            with open(params['del_path'] + updated_deletion) as fh:
                for handle in fh:
                    deleted_accounts.append(handle.strip())
                    del_sus_accounts.append(handle.strip())

            print('Found {:,} Twitter accounts that were deleted ...'.format(len(deleted_accounts)))

            # obtain suspended accounts
            sus_files = [m.group(0) for l in del_sus_files for m in [regex_suspended.search(l)] if m]
            print('\nFound {} files with suspended accounts.'.format(len(sus_files)))
            sus_files.sort()

            updated_suspension = sus_files[-1]
            print('Using most recent file <{}> to load suspended accounts ...'.format(updated_suspension))

            with open(params['del_path'] + updated_suspension) as fh:
                for handle in fh:
                    suspended_accounts.append(handle.strip())
                    del_sus_accounts.append(handle.strip())

            print('Found {:,} Twitter accounts that were suspended ...'.format(len(suspended_accounts)))

            print('\nCombining deleted and suspended Twitter accounts ...')
            print('Number of combine deleted/suspended accounts is {:,}'.format(len(del_sus_accounts)))

            interacting_handles = set(interacting_handles) - set(del_sus_accounts)
            print('\nConsidering ONLY {:,} Twitter Accounts to collect MAX number of tweets'.format(len(interacting_handles)))
            interacting_handles = list(interacting_handles)

    else:
        print('No deleted/suspended Twitter accounts was provided. Retrieving tweets from all interacting accounts ...')

    interacting_handles.sort()
    number_handles = len(interacting_handles)
    start = 0
    end = number_handles

    if 'auth' in kwarg:
        print('Auth={}'.format(kwarg['auth']))
    else:
        print('Auth=None')

    if 'part' in kwarg:
        print('Partition: {}'.format(kwarg['part']))
        value = kwarg['part'].split('-')
        number_partitions = int(value[1])
        bloc_part = int(value[0])

        blocks = make_partition(number_handles, number_partitions)
        work_range = get_partition_range(blocks, bloc_part)

        start = work_range[0]
        if len(work_range) == 1:
            end = number_handles
        else:
            end = work_range[1]

    print('Collecting tweets from the Twitter account {:,} to {:,} ...'.format(start, end))

    for counter, handle in enumerate(interacting_handles):
        if start <= counter < end:
            data = tweet.get_tweets(handle)
            print('Capture {:,} tweets for {}'.format(len(data), handle))
            tweet.save(handle, data)


if __name__ == '__main__':
    """
    Parameters for the script are:
    :path: path to the file where all capture conversations are stored. The conversations will be uploaded into memory.
           The uploaded object will contain the handles that interacted in the conversations. This is a MANDATORY
           parameter.
           
    :tweet_path: path of folder where tweets are stored. This is a MANDATORY parameter.

    :del_path: this parameter is the folder where the discovered deleted and suspended accounts are stored.
                A file containing a list of handles will be save in the folder with the following format:
                deleted_YYMMDD.dat & suspended_YYMMDD.dat - if <del_path> parameter is not provided all Twitter accounts
                interacting in the conversations will considered. 

    :part: this is an optional parameter. If provided, the list of interacting Twitter accounts will be broken in (n)
           parts. The parameter has the format d1-d2. Where d2 is an integer that represents the number of parts the list
           will be broken into. While d1 is the section that will be inspected.

           Ex: A conversation containing 100 handles could be broken in two pieces. Then, passing the parameter
               part=1-2 indicates that the running instance will work with elements 0-49. Another instance could run
               concurrently (part=2-2) to work elements 50-100.
               
    :auth: this parameter provides the authorization account which interact the Twitter API. These authorization accounts
           are present in the module [twitter_apps.Keys.py]. An entry for the account contains the values for:['consumer_key'],
           ['consumer_secret'], ['access_token_key'], and ['access_token_secret'].

    running example: python3 CollectActiveTweets.py part=1-10 path=data/verifiedUserDataset/tweetConvo.dat 
                     del_path=data/DeletedSuspendedAccounts/ auth=males
    """
    if len(sys.argv) < 3:
        print('\nNot enough arguments..', file=sys.stderr)
        print('File where conversations are contained is required ...', file=sys.stderr)
        print('Usage: python3 CollectActive.py path=path-to-conversations path_tweet=path-where-tweets-reside <del_path="path-to-del-sus-folder>',
              file=sys.stderr)
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[1:])

    if 'path' not in params or 'path_tweet' not in params:
        print('\npath and path_tweet are MANDATORY parameters', file=sys.stderr)
        print('Usage: python3 CollectActive.py path=path-to-conversations path_tweet=path-where-tweets-reside <del_path=path-to-del-sus-folder>',
              file=sys.stderr)
        sys.exit(-1)

    if not os.path.isfile(params['path']):
        print('\nCould not find file: {}'.format(params['path']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['path_tweet']):
        print('\nCould not find folder where tweets reside: {}'.format(params['path_tweet']), file=sys.stderr)
        sys.exit(-1)

    # add / to end of folder path if not given
    if params['path_tweet'][-1] != '/':
        params['path_tweet'] = params['path_tweet'] + '/'

    if params['del_path'] and not os.path.isdir(params['del_path']):
        print('\nCould not find folder: {}'.format(params['del_path']), file=sys.stderr)
        sys.exit(-1)

    # add / to end of folder path if not given
    if params['del_path'] and params['del_path'][-1] != '/':
        params['del_path'] = params['del_path'] + '/'
        print(params['del_path'])

    if 'part' in params:
        part = params['part'].split('-')
        if len(part) != 2:
            print('\nParameter <part> MUST have two integers between a dash. Ex: part=1-10', file=sys.stderr)
            sys.exit(-1)

        try:
            value0 = int(part[0])
            value1 = int(part[1])

        except ValueError:
            print('\nParameter <part> MUST have two integers between a dash. Ex: part=1-10', file=sys.stderr)
            sys.exit(-1)

    main(**params)

    sys.exit(1)
