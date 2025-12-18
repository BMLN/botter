import unittest
from os import environ






from src.jira_botter import servicedesk









class JiraTest(unittest.TestCase):
    
    
    def test_auth(self):

        to_test = servicedesk.Jira

        #args
        args = {
            "jira_url": environ.get("JIRA_URL"),
            "auth": {
                "email": environ.get("JIRA_AUTH_EMAIL"),
                "api_token": environ.get("JIRA_AUTH_TOKEN")
            }
        }


        #test
        self.assertIsNotNone(to_test(**args))









class ServicedeskTest(unittest.TestCase):

    def test_auth_for_project(self):
            
        to_test = servicedesk.JiraServicedesk

        #args
        args = {
            "jira": 
                servicedesk.Jira(**{
                    "jira_url": environ.get("JIRA_URL"),
                    "auth": {
                        "email": environ.get("JIRA_AUTH_EMAIL"),
                        "api_token": environ.get("JIRA_AUTH_TOKEN")
                    }
                }),
            "name": environ.get("JIRA_SERVICEDESK")
        }


        #test
        self.assertIsNotNone(to_test(**args))



    def test_fetchTickets(self):

        to_test = servicedesk.JiraServicedesk.fetchTickets

        #args
        args = [
            servicedesk.JiraServicedesk(**
                {
                    "jira": 
                        servicedesk.Jira(**{
                            "jira_url": environ.get("JIRA_URL"),
                            "auth": {
                                "email": environ.get("JIRA_AUTH_EMAIL"),
                                "api_token": environ.get("JIRA_AUTH_TOKEN")
                            }
                        }),
                    "name": environ.get("JIRA_SERVICEDESK")
                }
            ) 
        ]


        #test
        self.assertIsNotNone(to_test(*args))

        
        