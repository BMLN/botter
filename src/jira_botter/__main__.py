from sys import exit
from os import environ

from time import sleep
from signal import signal, SIGINT




from chatbot.interfaces.chatbot import Chatbot
from chatbot.instances.knowledgebases import WeaviateKB
from chatbot.instances.vectorizers import HFVectorizer
from chatbot.instances.matchers import WeaviateKeyMatcher
from chatbot.instances.generators import DeepinfraGenerator


from .instructions import JirabotInstructor

from .servicedesk import Jira, JiraServicedesk
from .controller import Controller





from logging import getLogger, basicConfig, INFO as LOG_INFO
logger = getLogger()









if __name__ == "__main__":
    basicConfig(level=LOG_INFO)





    #configuration
    configuration = {
        "jira_url": environ.get("JIRA_URL", None),
        "jira_auth_email": environ.get("JIRA_AUTH_EMAIL", None),
        "jira_auth_token": environ.get("JIRA_AUTH_TOKEN", None),
        
        "jira_servicedesk": environ.get("JIRA_SERVICEDESK", None),


        "chatbot_kb_host": environ.get("CHATBOT_KB_HOST", None),
        "chatbot_kb_port": environ.get("CHATBOT_KB_PORT", None),
        "chatbot_kb_collection": environ.get("CHATBOT_KB_COLLECTION", None),
        
        "chatbot_encoder_model": environ.get("CHATBOT_ENCODER_MODEL", None),

        "chatbot_generator_model": environ.get("CHATBOT_GENERATOR_MODEL", None),
        "chatbot_generator_apikey": environ.get("CHATBOT_GENERATOR_APIKEY", None),


        "update_freq": environ.get("UPDATE_FREQ", None)
    }

    if not all(list(configuration.values())[:-1]):
        logger.warning(f"didnt provide all variables: Missing { [ str.upper(key) for key, value in list(configuration.items())[:-1] if not value ]}")
        exit(1)
    





    #setup
    #jira
    jira = Jira(
        configuration["jira_url"], 
        {
            "email": configuration["jira_auth_email"], 
            "api_token": configuration["jira_auth_token"]
        }
    )
    servicedesk = JiraServicedesk(
        jira, 
        configuration["jira_servicedesk"]
    )
    
    #chatbot
    knowledgebase = WeaviateKB(
        configuration["chatbot_kb_host"], 
        configuration["chatbot_kb_port"], 
        configuration["chatbot_kb_collection"]
    )
    vectorizer = HFVectorizer(configuration["chatbot_encoder_model"])
    matcher = WeaviateKeyMatcher("text")
    instructor = JirabotInstructor()
    generator = DeepinfraGenerator(
        configuration["chatbot_generator_model"],
        configuration["chatbot_generator_apikey"], 
    )

    chatbot = Chatbot(
        knowledgebase,
        vectorizer,
        matcher,
        instructor,
        generator
    )

    #controls
    controller = Controller(
        servicedesk, 
        chatbot,
        **({"update_freq": configuration["update_freq"]} if configuration["update_freq"] else {})
    )





    #and.. run with it
    controller.start()

    signal(
        SIGINT,
        lambda sig, frame: controller.stop() or exit(0)
    )

    while True:
        sleep(13370000)
