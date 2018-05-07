# CollectActiveTweets

To build a docker image, run the following command from the repo directory.

```
$ docker image build -t collect-active-tweets .
```

To run an instance of a container run the following command.

```
$ docker container run -it --rm -v <data-dir>:/data collect-active-tweets ./main.py part=4-4 path=/data/tweetConvo.dat del_path=data/DeletedSuspendedAccounts/ auth=males path_tweet=data/AccountTweets
```
