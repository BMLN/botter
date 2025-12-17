import unittest
from chatbot.instances.generators import DeepinfraGenerator






from src.jira_botter import instructions







class InstructionTest(unittest.TestCase):

    def test1(self):
        to_test = instructions.request_supportanswer_prompt


        
        args = [
            "openai/gpt-oss-120b",
            350,
            0.4,
            "Guten Tag, GUI kann sich nicht anmelden. Wann kann das Problem beheben?\nIch muss heute alle praktischen Aufgaben einreichen. Ich habe alle Aufgaben gemacht außer\ndie Fallstudie ""HCM""  .\nKönnen Sie mir helfen?\nDanke!!!",
            [
                """Hallo James,
ich habe deinen Zugang entsperrt und das Passwort zurückgesetzt. Es lautet nun wieder:
password123
Gehe sicher, dass du bei der Anmeldung den Benutzer {{NUTZER-123}} sowie den richtigen Mandanten auswählst.
Beste Grüße
Karl - WLIB-Support""",

            """Hallo,

ich habe das Passwort Ihres Accounts zurückgesetzt.
Es lautet wieder: password123

Nach dem Einloggen können Sie wieder Ihr eigenes Passwort festlegen. 

Nach mehreren falschen Anmeldeversuchen wird das Konto gesperrt, leider werden die verbleibenden Versuche nicht im Login angezeigt. Ich persönlich empfehle die Verwendung eines Passwortmanagers, falls Sie dies nicht bereits tun, da dadurch häufig Tippfehler vermieden werden.

Mit freundlichen Grüßen

Harald.
"""
            ]
        ]



        #test
        result = DeepinfraGenerator(model=args[0]).generate(
            prompt=to_test.format(
                request=args[3],
                samples=args[4]
            ),
            max_length=args[1],
            temperature=args[2]
        )
        self.assertEqual(type(result), str)
