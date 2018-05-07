FROM python

LABEL maintainer="Plinio Vargas <@PlinioHVargas>"

WORKDIR /src

RUN pip install python-twitter tweepy

COPY . .

RUN chmod a+x main.py

# ./main.py part=4-4  path=data/tweetConvo.dat    del_path=data/DeletedSuspendedAccounts/ auth=males path_tweet=data/AccountTweets
