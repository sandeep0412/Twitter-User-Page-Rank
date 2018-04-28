import json
import time
from pathlib import Path
import os
import numpy as np
import tweepy
from memory_profiler import profile

def loadfiles(api):
    my_file = Path("accounts.json")
    print(my_file)
    accounts = dict()
    myFriends = api.friends_ids()
    checkedFriends = []
    return accounts, myFriends, checkedFriends

def run(username, consumer_key, consumer_secret, access_token, access_token_secret):
    FriendJson = []
    data = '"links:"'
    FriendJson.append(data)
    myname = username
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    minimumFollowers = 15
    print (consumer_key)
    timeBefore = time.time()
    accounts, myFriends, checkedFriends = loadfiles(api)
    callsCount = 1
    print("checked friends: ", len(checkedFriends),
          "remaining: ", (len(myFriends) - len(checkedFriends)))
    try:
        for followerID in myFriends:
            print(followerID)
            if followerID not in checkedFriends:
                # print("API calls= ", callsCount)
                if callsCount % 15 == 0:
                    continue;
                checkedFriends.append(followerID)
                friendsOfFriend = api.friends_ids(followerID, count=2000)
                callsCount += 1
                print("your friend: ", followerID, " follows ",
                      len(friendsOfFriend), " people")
                for friendOfFriendID in friendsOfFriend:
                    account = str(friendOfFriendID)
                    data ={}
                    data['source'] = followerID
                    data['target'] = friendOfFriendID
                    FriendJson.append(data)
                    if account in accounts:
                        accounts[account] += 1
                    else:
                        accounts[account] = 1
                    print("\t friendOfFriend ", account, " is followed by ",
                          accounts[account], " friends")
            else:
                continue
            np.array(checkedFriends).dump(open('checked.npy', 'wb'))
            with open('accounts.json', 'w') as fp:
                json.dump(accounts, fp)
            with open('graph.json', 'w') as gf:
                json.dump(FriendJson, gf)
    except Exception as e:
        print(str(e))
    saveaccounts(accounts, myFriends, myname, api)
    timeAfter = time.time() - timeBefore
    print("total time taken: ", timeAfter, " seconds")
    return True

def saveaccounts(accounts, myFriends, myname, api):
    minimumFollowers=2
    print("filtering accounts gathered")
    filteredAccounts = {k: v for k,
                        v in accounts.items() if v >= minimumFollowers}
    # dict of user names
    addedUsernames = dict()
    print("transforming IDs into usernames")
    myUsername = myname
    NodeJson = []
    data = '"nodes:"'
    NodeJson.append(data)
    for account in filteredAccounts:
        try:
            user = api.get_user(account)
            username = user.screen_name
            bio = user.description
            avatar = user.profile_image_url
            followers = user.followers_count
            name = user.name
            following = user.friends_count
            print("ID: ", account, " user: ", username)
            data={}
            data['id'] = account
            data['value'] = filteredAccounts[account]
            NodeJson.append(data)
            if username == myUsername:
                continue
            else:
                addedUsernames[username] = {}
                addedUsernames[username]['id'] = account
                addedUsernames[username]['count'] = filteredAccounts[account]/followers
                addedUsernames[username]['bio'] = bio
                addedUsernames[username]['avatar'] = avatar
                addedUsernames[username]['followers'] = followers
                addedUsernames[username]['name'] = name
                addedUsernames[username]['following'] = following
        except Exception as e:
            print(str(e))
        continue
    # save just in case
    with open('addedUsernames.json', 'w') as fp:
        json.dump(addedUsernames, fp)
    with open('graph1.json','w') as fp:
        json.dump(NodeJson, fp)
        # sort by most mutual friends
    print("sorting accounts")
    sortedAccounts = sorted(addedUsernames.items(),
                            key=lambda x: x[1]['count'], reverse=True)
    print("saving file..")
    with open('sortedAccounts.json', 'w') as fp:
        json.dump(sortedAccounts, fp)

#while not run():
#    run()
#    time.sleep(15)
