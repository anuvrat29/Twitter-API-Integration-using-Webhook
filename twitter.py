"""
    This code will take care of Twitter API Integration and Real time data connection.
"""
# pylint: disable=E0611
# pylint: disable=E0001
# pylint: disable=W0702
import re
import json
import base64
import hmac
import hashlib
from http import HTTPStatus
import requests
from flask import Flask, request
from requests_oauthlib import OAuth1

from webhook.config import DM_URL, TWEET_URL, BOT_ACCOUNT_ID
from webhook.config import CONSUMER_KEY, CONSUMER_SECRET
from webhook.config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET

APP = Flask(__name__)
AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class Listener:
    """
        This class contains all the methods which reads the messages and tweets from twitter
        and prepare reply to those texts. And replys back.
    """
    @staticmethod
    @APP.route("/twitter", methods=["GET"])
    def webhook():
        """
            This method will show if code is reachable or not.
        """
        return """<html><h1 align="center"> You are in Anuvrat Twitter API"""\
               + """ Integration Account </h1></html>"""

    @classmethod
    def replydm(cls, message, senderid):
        """
            This method will reply to direct message in twitter.
        """
        try:
            message = message.replace("\n", "\\n")
            json_msg = '{"event":{"type":"message_create","message_create":{"target":'\
                        + '{"recipient_id":"'+str(senderid)+'"},"message_data":{"text":'\
                        + '"'+str(message)+'"}}}}'
            response = requests.post(DM_URL, data=json_msg, auth=AUTH)
            response.close()
            return "Message Sent Successfully"
        except:
            return "Message Not Sent"

    @classmethod
    def replytweet(cls, message, postid):
        """
            This method will reply to tweet in public space.
        """
        try:
            json_msg = {"status": message, "in_reply_to_status_id": postid}
            response = requests.post(TWEET_URL, data=json_msg, auth=AUTH)
            response.close()
            return "Tweet Sent Successfully"
        except:
            return "Tweet Not Sent"

    @classmethod
    def twitter_response(cls, response):
        """
            This method will take care of routing of message in public and private chats.
        """
        if response["messagetype"] == "private":
            result = cls.replydm(response["requestmessage"], response["senderid"])
            print("Response: " + result + " to " + response["sendername"])
        else:
            reply = "@{} {}".format(response["screen_name"], response["requestmessage"])
            result = cls.replytweet(reply, response["postid"])
            print("Response: " + result + " to " + response["sendername"])

        return ("", HTTPStatus.OK)

    @staticmethod
    @APP.route("/twitter/webhook", methods=["GET"])
    def twittercrcvalidation():
        """
            This method will checked by twitter after some timeframe regularly.
        """
        sha256_hash_digest = hmac.new(CONSUMER_SECRET.encode("utf-8"),
                                      msg=request.args['crc_token'].encode("utf-8"),
                                      digestmod=hashlib.sha256).digest()
        return json.dumps({'response_token': 'sha256={}'\
                            .format(base64.b64encode(sha256_hash_digest).decode("utf-8"))})

    @staticmethod
    @APP.route("/twitter/webhook", methods=["POST"])
    def twittereventreceived():
        """
            This method will take care of fetch the real time direct message and tweet.
        """
        if "direct_message_indicate_typing_events" in request.get_json():
            return ("", HTTPStatus.OK)

        data = request.get_json()
        try:
            direct_message = data["direct_message_events"]
            senderid = str(direct_message[0]["message_create"]["sender_id"])
            if senderid != str(BOT_ACCOUNT_ID):
                text = str(direct_message[0]["message_create"]["message_data"]["text"])
                text = re.sub(r" http\S+", "", text)
                if text == "":
                    return ("", HTTPStatus.OK)

                reqparam = {
                    "messagetype": "private",
                    "requestmessage": text,
                    "senderid": senderid,
                    "sendername": str(data["users"][senderid]["name"])
                }
                print("\nRequest: " + str(reqparam))
                Listener().twitter_response(reqparam)
            return ("", HTTPStatus.OK)

        except:
            try:
                tweet = data["tweet_create_events"]
                if str(tweet[0]["user"]["id"]) != str(BOT_ACCOUNT_ID):
                    text = tweet[0]["text"]
                    text = re.sub("@.+? ", "", text)
                    reqparam = {
                        "messagetype": "public",
                        "requestmessage": text,
                        "postid": str(tweet[0]["id"]),
                        "sendername": str(tweet[0]["user"]["name"]),
                        "screen_name": str(tweet[0]["user"]["screen_name"])
                    }
                    print("\nRequest: " + str(reqparam))
                    Listener().twitter_response(reqparam)
            except:
                pass

        return ("", HTTPStatus.OK)

if __name__ == "__main__":
    APP.run(port=65000, debug=True)
