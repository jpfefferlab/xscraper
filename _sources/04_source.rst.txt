Source Data
============

In this section, you can see the metadata, which can be collected with the XScraper. 

Profile metadata
-----------------

A set containing the metadata to a user profile. This includes the users given name and username, biography (bio), location, link to his/her website, the creation date of the profile, as well as the number of followers, followings and post of the user. 
	
**Example response**:

.. code-block::

 {'given_name': 'Crypto Rover',
 'user_bio': '#Bitcoin Crypto YouTuber (160k SUBS) | Founder of @cryptoseacom All my posts are not financial advice.',
 'user_location': 'Bitcoin 🤩🌙',
 'number_of_followers': 982372,
 'number_of_following': 558,
 'number_of_posts': 38783,
 'user_website': 'https://t.co/xGVGcK2Xcv',
 'username': 'rovercrc',
 'user_join_date': '24.01.2021'}

Tweet metadata
----------------
   
A set containing the metadata of a tweet (or reply/quote). This includes the tweets text, author (username), statistics (number of replies, reposts, likes, bookmarks and views), creation date (time), and a link to the tweet.
	 
**Example response**:

.. code-block::

      {'text': 'i miss melania’s decor \n\nmake christmas decorations great again!!',
      'username': 'jackunheard',
      'link': 'https://x.com/jackunheard/status/1863720296844329040',
      'replies': 183,
      'reposts': 461,
      'likes': 5493,
      'bookmarks': 46,
      'views': 54802,
      'time': '2024-12-02t23:01:59.000z'}
