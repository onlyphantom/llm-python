from dotenv import load_dotenv
import guidance

load_dotenv()

chat = guidance.llms.OpenAI("gpt-3.5-turbo")
guidance.llm = chat

program = guidance(
    """
    {{#system}}You are a CS Professor teaching {{os}} systems administration to your students.{{/system}}

    {{#user~}}
    What are some of the most common commands used in the {{os}} operating system? Provide a one-liner description.
    List the commands and their descriptions one per line. Number them starting from 1.
    {{~/user}}

    {{#assistant~}}
    {{gen 'commands' max_tokens=100}}
    {{~/assistant}}    

    {{#user~}}
    Which among these commands are beginners most likely to get wrong? Explain why the command might be confusing. Show example code to illustrate your point.
    {{~/user}}

    {{#assistant~}}
    {{gen 'confusing_commands' max_tokens=100}}
    {{~/assistant}}
    """,
    llm=chat,
)


result = program(os="Linux")

print(result["commands"])
print("===")
print(result)
