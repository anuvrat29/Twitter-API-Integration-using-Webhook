# Twitter-API-Integration-using-Webhook
This repository will help in twitter api integration to send or receive direct messages or tweets.

•	Step 1: Take Developer Access.

1.	Take developers access from Twitter for Bot Account. To whom you want to communicate, and this twitter handle (BOT_ACCOUNT_ID) will reply to you. Find this twitter handle id which is unique to every user.

•	Step 2: Create an app.

1.	Login to https://developer.twitter.com and login.
2.	Create an app in developer account.
3.	Remember to note down CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET this will require to take access on twitter account.

•	Step 3: Setup Environment.

1.	Go to dashboard page from developers’ page.
2.	Click on account activity API i.e. Setup DEV environment.
3.	Give any name to “Dev environment label” and select “App Name”.


•	Step 4: Edit config.py file.

1.	Paste all details into that file.
2.	Following details
    -	CONSUMER_KEY
    -	CONSUMER_SECRET
    -	ACCESS_TOKEN
    -	ACCESS_TOKEN_SECRET
    -	ENVNAME (Dev environment label)
    -	WEBHOOK_URL (Will discuss in next point)

•	Step 5: WEBHOOK_URL

1.	Run twitter.py in one command prompt.
2.	Now your code is running on http://127.0.0.1:65000 URL because I fixed 65000 port in code itself.
3.	Now task is to convert http to https request, and this is because your code always should be reachable to twitter for handshake.
4.	Twitter will perform handshake (to hit that URL to check whether code is reachable or not) with your code once in 24 hours, starting the last time the webhook URL was validated and twitter will always expect to get response in 3 seconds.
5.	I used ngrok server to convert http to https which is free of cost but not good into production environment.
6.	Once you converted http to https then take this proxy URL and append “/twitter/webhook” and assign to WEBHOOK_URL (discussed in last step).
7.	If you want to use different endpoints, then change in code and same append to proxy URL (https URL).

•	Step 6: Setup Connection with twitter.

1.	Make sure your twitter.py is running.
2.	Now goto webhook folder and run webhook.py in another command prompt.
3.	And follow the instructions.
4.	First choose “Create and Subscribe Webhook”. If any errors come, then check WEBHOOK_URL and ENVNAME.
5.	Second choose “Retrieve Webhook”.
6.	Whenever you want to down (stop) the bot then first you must delete existing webhook by choosing “Delete Webhook”.
7.	In case any error comes, and you are not able to delete webhook then delete environment name from developers account and give another name and assign in config file and create webhook.
