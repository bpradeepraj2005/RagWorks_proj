# AI-Powered Personal Shopping Assistant (Multi-Agent Architecture)

An autonomous decision-making assistant built to handle complex shopping requirements including product research, live budget management, and delivery tracking. It uses a LangChain multi-agent framework to reason through tasks via the Model Context Protocol (MCP) and a local RAG Knowledge Base.

---

## 🏛️ Architecture Overview

The repository is fully refactored into a scalable service-oriented architecture:

- **`mcp_server/`**: A standalone FastMCP Server providing 8 robust shopping tools (Cart, Budget, Products, Delivery). Uses Python's `sqlite3` and dummy APIs to realistically model transactions.
- **`rag_engine/`**: A local ChromaDB vector database housing store policies, shipping guidelines, and warranties, embedded using `sentence-transformers`.
- **`agent_framework/`**: The "brain" of the system.
  - **Supervisor Agent**: Intelligently routes queries.
  - **Support Agent**: RAG-augmented agent resolving policy disputes.
  - **Shopping Agent**: Connects to the MCP Server via a strict standard I/O Client interface to execute market and budget tool operations.
  - **Guardrails**: Input/Output constraints protecting against malicious injection and restricted topics.

---

## 🚀 Setup Instructions

1. **Clone the repository and enter the directory.**
2. **Initialize a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate # (or venv/bin/activate on Mac/Linux)
   ```
3. **Install Dependencies:**
   ```bash
   pip install mcp requests pydantic langchain langchain-groq chromadb sentence-transformers pytest python-dotenv
   ```
4. **Environment Setup:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```
5. **Initialize Databases:**
   Run the seeder to populate realistic budgets, mock items, and order tracking histories.
   ```bash
   python mcp_server/seed_db.py
   ```

---

## 💻 Usage

To launch the beautiful Web UI (Graphical Interface), run:
```bash
streamlit run ui.py
```
This will automatically open the AI Chat application in your default web browser on `localhost:8501`.

**Example Queries you can try:**
- *"I have $1000 in my electronics budget. Can you search for a laptop, add it to my cart, and then check my budget?"* (Tests Shopping Agent + MCP)
- *"What is your return policy if I open the box?"* (Tests Support Agent + RAG)
- *"I want to buy a weapon."* (Tests Guardrails)
- *"Can you track my delivery for ORD-99911?"* (Tests Delivery Tracking Tools)

---

## 🧪 Testing

The repository uses `pytest` for rigorous unit and integration testing. Tests are isolated in the `tests/` directory.

To run all tests:
```bash
pytest tests/
```

---

## 📝 Evaluation Criteria Mapping (Grading Rubric)

1. **MCP (Model Context Protocol)**: Fulfilled natively. The `mcp_server` runs a FastMCP service. The agent accesses these tools over `stdio` strictly through `agent_framework/mcp_client.py`.
2. **RAG (Retrieval-Augmented Generation)**: Fulfilled via `rag_engine/vector_db.py`. Uses ChromaDB and `sentence-transformers` to encode and retrieve policy data.
3. **Agentic Frameworks & Multi-Agent**: Fulfilled via LangChain in `multi_agent.py`. A custom Supervisor router hands execution Context between a Shopping Agent (Tool Calling) and a Support Agent (RAG).
4. **Guardrails (Safety/Constraints)**: Fulfilled via `guardrails.py`. Blocks injection attempts, protects prompts, and declines restricted purchases automatically before hitting the LLM.
5. **Observability**: Fulfilled natively via `logging`. All actions (Agent routing, Guardrail trips, RAG similarity hits, and Tool Executions) append detailed timestamps to `logs/system_trace.log`.
6. **Testing**: Comprehensive tests verifying the API parser, Guardrails security boundaries, and RAG retrieval accuracy in the `tests/` directory.
