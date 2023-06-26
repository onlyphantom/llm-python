import random
from dotenv import load_dotenv
import guidance

load_dotenv()

# set the default language model that execute guidance programs
guidance.llm = guidance.llms.OpenAI("text-davinci-003")
# guidance.llm = guidance.llms.Transformers(
#     "stabilityai/stablelm-base-alpha-3b", device="cpu"
# )


program = guidance(
    """What are the top ten most common commands used in the {{os}} operating system? Provide 
    a one-liner description for each command.
    {{#block hidden=True}}
    A few example commands would be: 
    [1]: pwd prints the current working directory
    [2]: mv moves the file and can be used to rename a file 
    {{gen 'example' n=2 stop='"' max_tokens=20 temperature=0.8}}
    {{/block}}

    Here are the common commands: 
    {{#geneach 'commands' num_iterations=10}}
    [{{@index}}]: "{{gen 'this' stop='"'}}", Description: "{{gen 'description' stop='"'}}" 
    {{/geneach}}

    {{select 'flavor' options=quizflavor}}
    Explain the following commands for 🥇 {{randomPts}} points:
    {{#each (pickthree commands)}}
    {{@index+1}}. "{{this}}" 
    {{/each}}

    Use the commands you listed above as input, generate a valid JSON object that maps each command to its description.
    "{
        "{{os}}": [
            {{#geneach 'commands' num_iterations=1}}{{#unless @first}},{{/unless}}
                "{{gen 'this'}}"
            {{/geneach}}
    """
)

quizflavor = [
    "Quiz of the day!",
    "Test your knowledge!",
    "Here is a quiz!",
    "You think you know Unix?",
]

result = program(
    os="Linux",
    pickthree=lambda x: list(set(x))[:3],
    randomPts=random.randint(1, 5),
    quizflavor=quizflavor,
)

print(result["example"])
print("===")
print(result["commands"])
print("===")
print(result)
