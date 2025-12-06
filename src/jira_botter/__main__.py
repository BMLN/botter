from chatbot.instances.generators import DeepinfraGenerator
from instructions import system_prompt, user_prompt






question = "Guten Tag, GUI kann sich nicht anmelden. Wann kann das Problem beheben?\nIch muss heute alle praktischen Aufgaben einreichen. Ich habe alle Aufgaben gemacht außer\ndie Fallstudie ""HCM""  .\nKönnen Sie mir helfen?\nDanke!!!"


context = [
    r"Hallo Zusammen, leider kann ich mich nicht im System anmelden, weil die Anmeldedaten offenbar nicht mehr funktionieren. (s. Screenshot) Können Sie mir bitte eine neue Anmeldenachricht für *Modul Rechnungswesen und Controlling: Mikrozertifikatskurs ""Rechnungswesen und Controlling in SAP S/4HANA""* zusenden?\n\n\n\nVielen Dank vorab und viele Grüße",
    r"Sehr geehrtes Support-Team,\n\nleider kann ich mich nicht in das SAP-System einloggen. Ich habe es mit den angegebenen Zugangsdaten versucht, jedoch ohne Erfolg.\nKönnten Sie mir bitte weiterhelfen?\n\nVielen Dank im Voraus für Ihre Unterstützung."
]

extr_context = [

    """20/Okt/25 7:14 AM;5e5e24b1459a810c9af29a67;Hallo Jens,
ich habe deinen Zugang entsperrt und das Passwort zurückgesetzt. Es lautet nun wieder:
tlestart
Gehe sicher, dass du bei der Anmeldung den Benutzer {{LEARN-126}} sowie den richtigen Mandanten auswählst.
Beste Grüße
Tim - WLIB-Support""",


    """22/Sep/25 8:29 PM;712020:dd7c0c98-1978-4958-99a8-3d0173a81a22;Hallo,

ich habe das Passwort Ihres Accounts zurückgesetzt.
Es lautet wieder: tlestart

Nach dem Einloggen können Sie wieder Ihr eigenes Passwort festlegen. 

Nach mehreren falschen Anmeldeversuchen wird das Konto gesperrt, leider werden die verbleibenden Versuche nicht im Login angezeigt. Ich persönlich empfehle die Verwendung eines Passwortmanagers, falls Sie dies nicht bereits tun, da dadurch häufig Tippfehler vermieden werden.

Mit freundlichen Grüßen

Giorgos.
"""

]













def joiner(docs):
    return str.join(
        "",
        [f"{"\n\n" if i > 0 else ""}Example {str(i)}:::\n" + doc for i, doc in enumerate(docs)]
    )



answer = DeepinfraGenerator("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo").generate(
    prompt=user_prompt.format(
        context=joiner(extr_context),
        question=question, 
    ), 
    system_prompt=system_prompt.format()
)

print(answer)


