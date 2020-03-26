"""
    This file is responsible for create a webhook and register a webhook.
"""
import requests
from requests_oauthlib import OAuth1

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from config import ENVNAME, WEBHOOK_URL
from config import CREATE_WEBHOOK, SUBSCRIBE_WEBHOOK, RETRIEVE_WEBHOOK, DELETE_WEBHOOK

class TwitterWebhook:
    """
        This class is responsible for
        1. Create and Subscribe Webhook
        2. Retrieve a webhook
        3. Delete a webhook
        4. EXIT
    """
    @classmethod 
    def create_subscribe_webhook(cls, auth):
        """
            This method will create and register a webhook.
            Input:
                cls - class object
                auth - authentication object
            Output:
                json response which is collected from twitter.
                
        """
        create_response = requests.post(CREATE_WEBHOOK.format(ENVNAME),
        								data={'url': WEBHOOK_URL},
        								auth=auth)
        subscribe_response = requests.post(SUBSCRIBE_WEBHOOK.format(ENVNAME), auth=auth)
        return create_response.json()

    @classmethod
    def retrieve_webhook(cls, auth):
        """
            This method will register a webhook.
            Input:
                cls - class object
                auth - authentication object
            Output:
                json response which is collected from twitter.
        """
        response = requests.get(RETRIEVE_WEBHOOK, auth=auth)
        return response.json()

    @classmethod
    def delete_webhook(cls, auth):
        """
            This method will delete a webhook.
            Input:
                cls - class object
                auth - authentication object
            Output:
                String.
        """
        try:
            WEBHOOK_ID = cls.retrieve_webhook(auth)
            WEBHOOK_ID = WEBHOOK_ID["environments"][0]["webhooks"][0]["id"]
        except IndexError:
            return "No webhook is available to delete."
        response = requests.delete(DELETE_WEBHOOK.format(ENVNAME, WEBHOOK_ID), auth=auth)
        return "Webhook Deleted Successfully."

if __name__ == "__main__":

    """
        Here we are creating AUTH object which is authentication object which
        is required for registration of webhook to communicate with twitter.
    """
    AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    while True:
        print("***** M E N U *****")
        print("1. Create and Subscribe Webhook")
        print("2. Retrieve Webhook")
        print("3. Delete Webhook")
        print("4. EXIT")

        choice = int(input("Enter a number to choose option: "))

        if choice == 1:
            print(TwitterWebhook().create_subscribe_webhook(AUTH))
            print("Webhook Created and Subscribed Successfully.")

        elif choice == 2:
            print(TwitterWebhook().retrieve_webhook(AUTH))
            print("Webhook Retrieved Successfully.")

        elif choice == 3:
            print(TwitterWebhook().delete_webhook(AUTH))

        elif choice == 4:
            break

        else:
            print("Please choose correct option.")
