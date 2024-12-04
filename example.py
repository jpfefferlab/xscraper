import xscraper as xs

#Start selenium, then manually login
#Wait until you are logged in, then execute the remaining functions.
driver = xs.start_selenium()

#Collect 5 tweets to the keyword christmas
christmas_tweets = xs.get_tweets_by_keyword(driver, 'christmas', 5)

#Collect 10 tweets of the user rovercrc
rover_tweets = xs.get_tweets_of_user(driver, 'rovercrc', 10)

#Get profile information for user roverrc
profile = xs.get_profile_details(driver, 'rovercrc')

#Collect 40 followers of the user roverrc
followers = xs.get_followers_of_user(driver, 'rovercrc', 40)

#Collect 30 followings of the user Shomburg
#As the user has only two followers, the function will print an "End of page reached" statement
followings = xs.get_followings_of_user(driver, 'SHomburg', 30)