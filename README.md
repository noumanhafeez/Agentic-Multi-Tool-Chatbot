# Agentic Multi-Agent Chatbot System

An advanced **Agentic Multi-Agent Chatbot System** built using **LangGraph** and **LangChain** to enable intelligent, context-aware, and scalable conversational experiences.

The system uses a **multi-agent architecture** where specialized agents collaborate to reason, execute tasks, retrieve information, manage conversation state, and generate accurate responses dynamically.

Designed with modularity and extensibility in mind, this project demonstrates how modern **agentic AI systems** can solve complex tasks through structured workflows, tool usage, and Retrieval-Augmented Generation (RAG).

Additionally, the project integrates **LangSmith** for end-to-end observability, workflow tracing, debugging, and performance monitoring of agent executions.

---

## Features

- Multi-agent orchestration using **LangGraph**
- Dynamic routing and intelligent task delegation
- Multi-step reasoning and execution workflows
- Retrieval-Augmented Generation (**RAG**)
- Tool calling and external API integration
- Conversation memory and context tracking
- Stateful workflow management
- **LangSmith integration for tracing and debugging**
- Execution monitoring and agent observability
- Scalable and modular design
- Real-time conversational interaction
- Extensible agent and tool ecosystem

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Orchestration | LangGraph |
| LLM Framework | LangChain |
| Monitoring & Tracing | LangSmith |
| Backend | Python |
| API Layer | FastAPI |
| Retrieval | RAG |
| Storage | Vector Database |
| State Management | LangGraph State |
| Deployment | Docker |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/agentic-multi-agent-chatbot.git

cd agentic-multi-agent-chatbot
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create `.env`

```env
# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

# Search Tool
TAVILY_API_KEY=

# LLM Provider
GOOGLE_API_KEY=
```

---

### 5. Start Server

```bash
uvicorn backend.main:app --reload
```

Application URL:

```bash
http://localhost:8000
```

Swagger Documentation:

```bash
http://localhost:8000/docs
```

---

## LangSmith Observability

This project integrates **LangSmith** to monitor and improve agent performance.

Capabilities include:

- Agent execution tracing
- Workflow visualization
- Step-by-step debugging
- Latency monitoring
- Tool invocation tracking
- Prompt inspection
- Error analysis
- Evaluation and experimentation

Enable tracing by configuring:

```env
LANGSMITH_TRACING=true
```

Then view executions inside your LangSmith dashboard.

---

## How It Works

1. User submits a query  
2. Supervisor coordinates workflow execution  
3. Specialized agents process tasks  
4. Retrieval and tools are executed  
5. Memory updates maintain context  
6. LangSmith traces execution flow  
7. Final response is generated  

---

## API Example

### Request

```http
POST /chat
```

```json
{
  "message": "Explain Retrieval-Augmented Generation"
}
```

### Response

```json
{
  "response": "Generated response from agent workflow"
}
```

---

## Use Cases

- AI Assistants
- Customer Support Automation
- Enterprise Knowledge Systems
- Research Assistants
- Productivity Applications
- Agentic Workflow Systems
- Internal Business Copilots

---

## Future Improvements

- Multi-modal capabilities
- Long-term memory
- Autonomous planning agents
- Streaming responses
- Advanced evaluations with LangSmith
- Authentication and user sessions
- Agent benchmarking pipelines

---

## Contributing

Contributions are welcome.

```bash
Fork Repository

Create Feature Branch

Commit Changes

Open Pull Request
```

---

## License

This project is licensed under the **MIT License**.

---

## Author

### Nouman Hafeez

AI Engineer | Mobile App Developer | Web Data Engineer

Focused on building scalable AI systems, agentic workflows, and intelligent applications.