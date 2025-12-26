from prompting.prompt import Prompt
from chatbot.interfaces.chatbot import Chatbot

from typing import override







# system_prompt = Prompt("""Using answers contained in the context, give a comprehensive answer to the question that is similar to those examples.
# Respond only to the question asked, response should be concise and relevant to the question.
# If the answer wouldn't match the examples, do not give any answer at all.""")


# user_prompt = Prompt("""Context:
# {context}
# ---
# Now here is the question you need to answer:

# Question: {question}""")



request_supportanswer_prompt = Prompt("""Du bist ein Support-System für die WLIB-Platform.
Du erhälst eine Kundenanfrage und eine Auswahl an vorgebenen Antworten.
Deine Aufgabe ist es den Inhalt aus den Vorgaben in einer neuen Antwort wiederzugeben, so dass sie auf die Kundenanfrage zugeschnitten ist.


Deine Vorgaben lauten dabei wie folgt:
- Schreibe alles auf Deutsch.
- Konzentriere dich nur auf fachlich/technisch Relevantes.
- Antworte AUSSCHLIESSLICH im JSON-Lines-Format: eine Zeile pro Ticket, genau in diesem Schema:
{{"Antwort": "..."}}
- ODER: falls du die Kundenanfrage NUR mit Hilfe der Auswahl an gelieferten Antwortvorgaben nicht ordentlich beantworten kannst, antworte AUSSCHLIESSLICH mit einer leeren Antwort im JSON-Lines-Format, genau in dem Schema:
{{}}

                                                                               
Hier ist die Auswahl an vorgegebenen Antworten: 
{samples}

Hier ist die Anfrage des Kunden auf die du Antworten sollst: 
{request}
""")
request_supportanswer_prompt.set_formatter(
    "samples", 
    lambda x: 
      str.join(
        "",
        [f"{"\n\n" if i > 0 else ""}Antwort {str(i+1)}:\n" + doc for i, doc in enumerate(x)]
      )
)



class JirabotInstructor(Chatbot.Instructor):
    
    @override
    def create_instructions(self, text, context):
      return {
         "prompt": request_supportanswer_prompt.format(
            request=text,
            samples=context
         )
      } | self.kwargs

