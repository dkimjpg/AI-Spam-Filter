# About this repository:
This is just a repository for the Artificial Intelligence Spam Filter I coded. It's mainly just for showcasing my AI program.

# How this Spam Filter works:
To sum it up, it makes use of a Naive Bayes model to determine whether or not an email is spam or not. As for how Naive Bayes is used, it just trains on data that is given to it by calculating a bunch of 
probabilities and uses those probabilities to make a judgment if an email is spam or not. 

1. Now to be specific, first, it goes through every single token (which is just a string of characters) in the given training data (which are all email samples that are classified as either spam or not spam) and runs 
   the Laplace probability equation on every single token. Each token is added to a dictionary of probabilities (or updated with new values if it already exists in the dictionary) as well as an unknown token (which is
   added to the dictionary as \<UNK\>) which denotes a special word that substitutes for the unknown tokens in an email that have not been encountered during the first training session. 

   Now this should be run twice when first starting, since two dictionaries need to be initialized for the words that are known to be spam and for the words that are known to not be spam. These will help later when
   determining whether or not an email is spam.

2. After that's done running, the next thing to do is to go through the entire list of tokens and look at each token to see if it is in the spam dictionary or the not-spam dictionary. If the token is in the spam dictionary,
   add it to a spam counter that counts how many tokens are considered spam. Otherwise, just get the value of \<UNK\> in the spam dictionary and add that value to the spam counter. Oh, and this same process should
   be applied to the not-spam counter as well.
   
3. Now that all the tokens have been counted, it's time to compare the spam counter to the not-spam counter. Now technically, this is where an equation might come into play, but I've found that just comparing if
   the spam counter is larger than the not-spam counter should be reasonably sufficient enough to determine whether or not an email is spam. Simply put:
   -  Spam Counter > Not-Spam counter = The email is spam
   -  Spam Counter <= Not-Spam counter = The email is not spam 
   
   I know this might be a bit naive, this is basically a 50/50 kind of calculation after all, but I think it suffices for this example of a Spam Filter. Besides, if your email is 50% spam, I'd say that's a good
   indication that your email is probably spam, but I digress.

Now at this point, the AI has already determined if an email is spam or not, but there are also some extra functions that show what the most indicative tokens were for determining if an email was spam or not. There's
another equation is used for this, and the functions give back an amount of the top most indicative tokens based on what number the user puts into the function.

Other than that, that's the entire AI in a nutshell. I know it may not be the best explanation of how the entire AI works, but I think it gives a simple overview of how the Spam Filter works. There's a bit more I could 
improve on this explanation, like adding pictures of the equations I modeled this after, but I'll have to add that at some other time when I have the chance.
