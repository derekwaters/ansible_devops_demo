# for accessing the environment variables
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# for communication with Llama Stack
from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent
from llama_stack_client import NotFoundError
from llama_stack_client.lib.agents.react.agent import ReActAgent
from llama_stack_client.lib.agents.react.tool_parser import ReActOutput
from llama_stack_client.lib.agents.event_logger import EventLogger

# pretty print of the results returned from the model/agent
from termcolor import cprint
import sys
sys.path.append('.')

base_url = os.getenv("LLAMASTACK_URL", "http://0.0.0.0:8321")
aap_mcp_url = os.getenv("REMOTE_AAP_MCP_URL")
model_id = os.getenv("LLAMASTACK_MODEL_ID", "ollama/qwen3:4b")


client = LlamaStackClient(
    base_url=base_url,
    timeout=10.0 * 60.0
)

print(f"Connected to Llama Stack server")


models = client.models.list()

# Select the first ollama llm
# model_id = next(m for m in models if m.model_type == "llm" and m.provider_id == "ollama").identifier

temperature = float(os.getenv("TEMPERATURE", 0.0))
if temperature > 0.0:
    top_p = float(os.getenv("TOP_P", 0.95))
    strategy = {"type": "top_p", "temperature": temperature, "top_p": top_p}
else:
    strategy = {"type": "greedy"}

max_tokens = 5000

# sampling_params will later be used to pass the parameters to Llama Stack Agents/Inference APIs
sampling_params = {
    "strategy": strategy,
    "max_tokens": max_tokens,
}

stream = False

print(f"Inference Parameters:\n\tModel: {model_id}\n\tSampling Parameters: {sampling_params}\n\tstream: {stream}")



print(f"Using AAP URL {aap_mcp_url}")

try:
    client.toolgroups.unregister(toolgroup_id="mcp::ansible-aap-server")
except NotFoundError:
    print("Tool doesn't exist yet...")

registered_tools = client.tools.list()
registered_toolgroups = [t.toolgroup_id for t in registered_tools]
if "mcp::ansible-aap-server" not in registered_toolgroups:
    print("Registering the ansible-aap-server toolgroup")
    client.toolgroups.register(
        toolgroup_id="mcp::ansible-aap-server",
        provider_id="model-context-protocol",
        mcp_endpoint={"uri":aap_mcp_url},
    )
    registered_tools = client.tools.list()
    registered_toolgroups = [t.toolgroup_id for t in registered_tools]

print(f"Your Llama Stack server is registered with the following tool groups @ {set(registered_toolgroups)} \n")



model_prompt= """You are a helpful assistant. You have access to a number of tools.
Whenever a tool is called, be sure to return the Response in a friendly and helpful tone.
"""


#model_id = "deepseek-r1-0528-qwen3-8b-bnb-4bit" # "llama-4-scout-17b-16e-w4a16"
stream = True

#model_id = "llama3-2-3b"
#stream = False

agent = ReActAgent(
            client=client,
            model=model_id,
            tools=["mcp::ansible-aap-server", "builtin::websearch"],
            response_format={
                "type": "json_schema",
                "json_schema": ReActOutput.model_json_schema(),
            },
            sampling_params={"max_tokens":512},
        )

user_prompts = ["""What job templates are available in AAP?""",
                """What host inventories are available in AAP?""",
                """What job template would be good to solve a disk full error?"""
               """Examine the following JSON error message: 
{
   'error': 'disk full',
   'hostname': 'app-db-02',
   'message': 'Disk /data on app-db-02 is 95 percent full. Please free up space or expand the disk'
}

Determine whether AAP has a job template to solve this issue. If so, find the relevant host inventory that needs to be used, and launch the job template.
"""]

session_id = agent.create_session("web-session")

while True:
    # Display a prompt
    cprint("\n"+"="*50, "green")
    prompt = input("Please enter your request for the agent (Enter 'quit' or 'bye' to finish): ")

    if prompt.lower() == "quit" or prompt.lower() == "bye":
        break;

    cprint("\n"+"="*50, "green")
    cprint(f"prompt> {prompt} ", "green")

    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
        stream=stream
    )
    if stream:
        for log in EventLogger().log(response):
            log.print()
    else:
        print(response.steps)
        
cprint("\n"+"="*50, "green")
cprint("Thanks!", "green")