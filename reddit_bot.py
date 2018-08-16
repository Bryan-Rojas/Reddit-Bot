import praw
import config
import time
import os
import random

#Bot Log In Function
def bot_login():
    #Attempt to log in as username set in the config.py file dialouge.
    print("Logging in as " + config.username)

    #Creating Redditor (Aka Reddit Bot) Object with the help of Python Reddit API Wrapper.
    #To create the object we need the username and password of the application/script bot account.
    #We will also need the OAuth2 credentials provided when we created the application/script
    #from the reddit site itself. Make sure to add these credentials to the config.py file.
    #Credentials can be accessed from: reddit.com -> preferences -> apps -> under "developed applications"
    reddit_bot = praw.Reddit(username = config.username,
                            password = config.password,
                            client_id = config.client_id,
                            client_secret = config.client_secret,
                            user_agent = config.user_agent)

    #Try-catch block to notify users if they've been signed in succesfully.
    #If you receive failure message please check your config.py file and ensure you entered the correct information.
    try:
        print("Logged in as " + str(reddit_bot.user.me()))
    except:
        print("Failed to log in as " + config.username)

    #The Redditor/Bot object will be logged in and returned
    return reddit_bot


#Run Bot Function
#This function takes in the Redditor (Aka Reddit Bot) Object we created in bot_login().
#It also takes in a list for comments already replied to and a list of imgur link entensions.
def run_bot(reddit_bot, comments_replied_to, list_of_links):
    #Now that the we have the bot signed in, we must obtain comments so that the bot can do its job.
    #It will take comments from the following subreddit(s): aww
    print("Obtaining comments... please wait! :)")

    #Here it generates a random number and utilizes this random number to decide a random imgur link.
    #Using the random number, it picks that position/index in the list "link_extension"
    randnum = random.randint(0,len(list_of_links)-1)

    #Here is makes a string equal to the random position of the imgur link extension.
    link_extension = list_of_links[randnum]

    #It will look through all the recent comments (25) in any subreddits and looks for "!BirbMemePls"
    #inside relevant subreddits. Then it replies with a birb meme with its imgur link and adds it to the list
    #of comments replied so it doesn't reply multiple times to another text file.
    for comment in reddit_bot.subreddit('aww').comments(limit=25):
        if "!BirbMemePls" in comment.body and comment.id not in comments_replied_to:
            print("Birb Reddit Bot found a user who wants a birb meme! :) Comment ID: " + comment.id)
            comment.reply("CAW! CAW! " + str(comment.author) + " want a meme!" + " [Birb Meme Here :3](https://i.imgur.com/" + link_extension + ")")

            comments_replied_to.append(str(comment.id))
            print("Birb Reddit Bot successful replied to comment ID: " + comment.id + " and has been added to the replied-to list.")

            with open ("replied_comments_list.txt", "a") as file:
                file.write(comment.id + "\n")

    #Now the bot takes a break for a minute so it doesn't spam reddit with search requests.
    print("Birb Reddit Bot is now sleeping for 1 minute...")
    time.sleep(60)


#This function is to obtain the saved replied to comments from a text file.
def obtain_saved_comments():
    #If there is no file then it will create an empty on for you.
    if not os.path.isfile("replied_comments_list.txt"):
        comments_replied_to = []
    else:
        with open("replied_comments_list.txt", "r") as file:
            comments_replied_to = file.read()
            comments_replied_to = comments_replied_to.split("\n")

    return comments_replied_to

#Main method because I'm unable to break the habit of using C++ and Java
def main():
    #We're going to create our bot object now along with testing the sign in.
    birb_bot = bot_login()

    #Now here's a list that will be used to keep track of all the comments that were replied to already.
    #We're doing this to make sure it doesn't reply to the same comment again if the bot is ran again.
    comments_replied_to = obtain_saved_comments()

    #Here's a list that will contain the file location on imgur
    #It only contains the last part of the link because they all start with "https://i.imgur.com/"
    imgur_links = ['4liQxFP.jpg', '9CWZs9p.jpg', 'SNB2cq1.jpg', 'oefZu55.jpg', 'QuJrSut.png', 'BH1LPZu.jpg', 'X1ngCUP.jpg', '1pUemei.jpg', '5ns0rAq.jpg']

    #While loop that will never stop looping so this can be ran on a Raspberry PI 24/7 or on a web server
    while True:
        run_bot(birb_bot, comments_replied_to, imgur_links)

if __name__ == '__main__':
    main()
