from .servicedesk import JiraServicedesk
from chatbot.interfaces.chatbot import Chatbot



from time import sleep
from queue import Queue
from threading import Thread, Event
import atexit


import datetime

from logging import getLogger

logger = getLogger()





class Controller():

    def __init__(self, servicedesk: JiraServicedesk, chatbot: Chatbot, update_freq=60):
        self.servicedesk = servicedesk
        self.chatbot = chatbot
        self.ticket_queue = Queue(maxsize=1337)
        self.update_freq = update_freq
        self.updated = datetime.datetime.now() - datetime.timedelta(days=30)
        logger.info(f"setup jira_bot on {servicedesk.project.get("projectName", None)}({servicedesk.jira.jira_url})")

        self.worker_processing = None
        self.worker_updates = None
        self._signal = Event()


    def __del__(self):
        self.stop()

        logger.info(f"jira_bot was shutdown - {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}")





    def update(self):
        updated = datetime.datetime.now()

        changedTickets = self.servicedesk.fetchTickets()
        changedTickets = [ x for x in changedTickets if (datetime.datetime.fromisoformat(x.get("updated", None)).timestamp() or datetime.datetime.now().timestamp()) > self.updated.timestamp() ]

        
        for x in changedTickets: 
            self.ticket_queue.put(x)


        self.updated = updated

        logger.info(f"jira_bot updated - {str(self.updated.strftime("%Y-%m-%d %H:%M"))}")



    def processTicket(self, ticketid):
        ticket = self.servicedesk.fetchTicket(ticketid)

        if (messages := ticket.get("messages")):   #should always be true however
            if messages[-1]["author"] == ticket["creator"] and messages[-1]["author"] != self.servicedesk.jira.accountId:
                logger.info(f"jira_bot is processing ticket {ticketid}")

                #create response
                inquiry = messages[-1]["text"] #last message only? Need testing for best contextwindow
                response = self.chatbot.respond(inquiry) #"here it would invoke a chatrequest" 

                #post response
                self.servicedesk.postMessageTo(ticket["id"], "---!AUTOMATED MESSAGE! CURRENTLY IN TESTING! ONLY CONTAINS END-TO-END COURSE DATA!---\n" + response, False) #for current testing stage
                    
                logger.info(f"jira_bot posted a message to {ticketid}")






    def start(self):
        logger.info(f"starting jira_bot on {self.servicedesk.project.get("projectName", None)}({self.servicedesk.jira.jira_url})")


        #producer
        def processingworker_start():
            while True:
                #halts and waits due to queue 
                ticket = self.ticket_queue.get() 
                
                try:
                    if ticket is self._signal: 
                        break

                    self.processTicket(ticket["id"])
                                
                except Exception as e:
                    logger.error(f"jira_bot couldn't process ticket {ticket["id"]}: {e} ")
                                
                finally:
                    self.ticket_queue.task_done()
                
            logger.info(f"jira_bot stopped processing tickets - {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}")


        #consumer
        def updateworker_start():
            while self._signal.is_set():
                try:
                    self.update()
                    
                except Exception as e:
                    logger.warning(f"jira_bot failed to update - {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}: {type(e)}")

                sleep(self.update_freq)

            logger.info(f"jira_bot stopped updating tickets - {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}")

            


        self.worker_processing = Thread(
            name="jira_bot-processor",
            target=processingworker_start,
            daemon=True
        )
        self.worker_updates = Thread(
            name="jira_bot-updater",
            target=updateworker_start,
            daemon=True
        )
        
        self._signal.set()
        self.worker_processing.start()
        self.worker_updates.start()





    def stop(self):
        self._signal.clear()
        self.ticket_queue.put_nowait(self._signal)

        if self.worker_updates:
            self.worker_updates.join()

        if self.worker_processing:
            self.worker_processing.join()
        

