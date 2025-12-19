import unittest
from unittest.mock import MagicMock

from os import environ
from typing import override

from src.jira_botter.servicedesk import Jira, JiraServicedesk
from time import sleep







from src.jira_botter import controller











#TODO
class ControllerTest(unittest.TestCase):

    class MockController(controller.Controller):
        @override
        def processTicket(self, ticketid):
            controller.logger.info(f"jira_bot posted a message to {ticketid}")
        






class IntegrationTest(unittest.TestCase):

    class ReadonlyServicedesk(JiraServicedesk):
        @override
        def postMessageTo(self, ticketid, message, public=True):
            pass
    
        
    
    
    def test_jiraintegration_update(self):
        to_test = controller.Controller.update


        #args
        sd = IntegrationTest.ReadonlyServicedesk(**
            {
                "jira": 
                    Jira(**{
                        "jira_url": environ.get("JIRA_URL"),
                        "auth": {
                            "email": environ.get("JIRA_AUTH_EMAIL"),
                            "api_token": environ.get("JIRA_AUTH_TOKEN")
                        }
                    }),
                "name": environ.get("JIRA_SERVICEDESK")
            }
        )
        cb = MagicMock()
        cb.respond.return_value = "<mock response>"
        
        args = {
            "self": controller.Controller(
                sd,
                cb
            )
        }


        
        #test
        with self.assertLogs() as log_manager:
            to_test(**args)

        self.assertTrue(any("jira_bot updated" in x for x in log_manager.output))





        
    
    def test_jiraintegration(self):
        to_test = controller.Controller.start


        #args
        sd = IntegrationTest.ReadonlyServicedesk(**
            {
                "jira": 
                    Jira(**{
                        "jira_url": environ.get("JIRA_URL"),
                        "auth": {
                            "email": environ.get("JIRA_AUTH_EMAIL"),
                            "api_token": environ.get("JIRA_AUTH_TOKEN")
                        }
                    }),
                "name": environ.get("JIRA_SERVICEDESK")
            }
        )
        cb = MagicMock()
        cb.respond.return_value = "<mock response>"
        

        
        #test
        with self.assertLogs() as log_manager:
            tester = controller.Controller(sd, cb, 5)

            to_test(tester)
            sleep(2)

            tester.stop()
            sleep(2)

        
        self.assertTrue(any("setup jira_bot" in x for x in log_manager.output))
        self.assertTrue(any("jira_bot updated" in x for x in log_manager.output))
        self.assertTrue(any("jira_bot stopped updating tickets" in x for x in log_manager.output))
        self.assertTrue(any("jira_bot stopped processing tickets" in x for x in log_manager.output))

