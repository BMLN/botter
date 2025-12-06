from prompting.prompt import Prompt


system_prompt = Prompt("""Using answers contained in the context, give a comprehensive answer to the question that is similar to those examples.
Respond only to the question asked, response should be concise and relevant to the question.
If the answer wouldn't match the examples, do not give any answer at all.""")


user_prompt = Prompt("""Context:
{context}
---
Now here is the question you need to answer:

Question: {question}""")



