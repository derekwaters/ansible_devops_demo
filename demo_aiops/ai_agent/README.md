# Server qwen with ollama

ollama pull qwen3:4b
ollama run qwen3:4b --keepalive 60m 

# Start Llama Stack

uv venv 
source .venv/bin/activate

uv run --with llama-stack llama stack list-deps starter | xargs -L1 uv pip install

To use local ollama:

OLLAMA_URL=http://localhost:11434 \
    uv run --with llama-stack llama stack run starter

Or to use an OpenAI compatible endpoint:

OPENAI_API_KEY=<key> \
OPENAI_BASE_URL=https://<endpoint>:443/v1 \
    uv run --with llama-stack llama stack run starter

# Start MCP Server

cd /home/derek/dev/mcp-server-aap/

export AAP_URL=https://aap25.localdomain
export AAP_TOKEN=7Kl1SoHRRhzMk8nqET6RNgVtPW4wG3
export AAP_PROJECT_ID=12
export AAP_VERIFY_SSL=false


mcp-proxy python server.py --port 8080 --host 0.0.0.0 --pass-environment --debug

# Run mcp-test

cd /home/derek/dev/llama-stack-test/

export REMOTE_AAP_MCP_URL="http://0.0.0.0:8080/sse"

uv run --with llama-stack-client,fire,requests,dotenv mcp-test.py

or


uv run --with llama-stack-client,fire,requests,dotenv agentic-aap-demo.py



# Script tests

What job templates are available in AAP?

===> Note that the listed templates only include the ones my account has access to! GUARDRAILS PT 1

What host inventories are available in AAP?
What job template could I use to solve a "disk full" error?
What inventory contains the host "app-db-02"?
Find a job template to solve the following error: '{ "type": "error", "host": "app-db-02", "message": "Disk /data is 95% full. Please ensure this device has sufficient space" }' If you find a solution, launch the job template with the relevant inventory. If you need an incident number, obtain one with the create_incident tool.

===> Policy issue GUARDRAILS PART 2

OK, try to launch that job, but pass the extra_var "change_number" of "CHG-00001" to meet the required policy.