1. EGAA_Main.py-: Backend EGAA_Engine Code
2. streamlit_app.py-: Frontend code to execute user querries

Below codes are sample codes created while doing POC
3. db.ipynb-: Individual code for Database querying
4. V1_Rag_on_Pdf.ipynb-: Individual code for PDF File querying
********************************************************************************************************************************************************************************************************
1. EGAA_Main.py-: Backend EGAA_Engine Code-:

This code combines various tools and functionalities from the Langchain library to build a conversational AI agent capable of querying structured and unstructured data. Here's a breakdown of the important parts:

1. Libraries and Imports-: 
Langchain Agents and Tools: Imports necessary classes for creating SQL query agents, embedding models, document loaders, vector stores, and tools to interact with both SQL databases and unstructured document data (e.g., PDF files).
Chat Models: Uses ChatOpenAI to interact with OpenAI's GPT-3.5-turbo model.
2. LLM (Language Learning Model) Setup-: (Note-: Currently we are using OPEN AI gpt-3.5-turbo model, but in actual scenario we will be using In house LLM models)
The ChatOpenAI model from OpenAI is initialized with the gpt-3.5-turbo model to answer questions.
The model is configured with a low temperature=0 for deterministic responses, meaning it will give more focused answers without much variation.
3. Database Connection
PostgreSQL Database Connection: Uses the SQLDatabase class to connect to a PostgreSQL database. The connection URI (pg_uri) is formed using credentials like host, port, username, password, and database schema.
This SQL database will be queried for loan- and transaction-related questions.
4. Unstructured Data Loading and Vector Database Setup-: 
PyPDFLoader: Loads a PDF document (Loan.pdf) containing information about loans.
Text Splitting: The document is split into smaller chunks (using CharacterTextSplitter) for easier search and processing.
Embeddings and Vectorstore:
OpenAIEmbeddings: Generates embeddings from the text chunks using OpenAI’s embedding API.
Chroma: A vector database is created to store the document embeddings for fast retrieval during question-answering.
Retrieval-based QA: The retrieval_qa instance is used to perform question-answering on the document using the retrieval-based QA mechanism.
5. Tools for Data Querying-: 
Several tools are defined for interacting with both structured and unstructured data:
QuerySQLDataBaseTool: Queries the SQL database for structured data (like loan amounts, transactions).
InfoSQLDatabaseTool, ListSQLDatabaseTool, and QuerySQLCheckerTool: Tools that provide additional capabilities for interacting with and checking SQL queries.
unstructured_qa_tool: Queries unstructured data (from the loan document) to answer questions about loan policies or agreements.
6. Agent Creation-: 
An agent is created using Langchain’s REACT framework. This agent is designed to:
Choose between querying the SQL database for structured data (e.g., loan transactions) or the vector database (e.g., loan agreements or policies).
Follow a predefined prompt (system_prefix) with step-by-step reasoning and instructions for handling user questions.
7. System Prompt-: 
The system prompt outlines how the agent should decide which data source to use. It distinguishes between:
Structured Database: For loan transactions, amounts, repayment details, etc.
Unstructured Database: For loan agreements, legal clauses, and policies.
The agent first tries to fetch information from the unstructured data source (PDF documents) before accessing the structured SQL database.
8. Conversation Buffer Memory-: 
ConversationBufferMemory: A memory tool that stores previous conversations, allowing the agent to reference past interactions.
9. Agent Executor-: 
The AgentExecutor manages the agent’s interaction with both the tools and the conversation flow, with a limit on the number of iterations (max_iterations=150).
10. Interaction Function
The chat_with_agent function allows the agent to answer user questions by invoking the underlying tools and models.
11. Chat History-: 
The function get_session_history retrieves chat history from a local SQLite database to provide context for conversations across sessions.
12. Example Usage-: 
Functions like get_user_input_and_invoke_llm handle user input and invoke the agent to answer questions, which could be related to loans or loan policies.

********************************************************************************************************************************************************************************************************
2. streamlit_app.py-:
This code defines a Streamlit application that serves as a financial insights dashboard with an AI chatbot functionality. Here's an explanation of the key components:

1. Imports and Dependencies:
streamlit: Used to create the web-based interface.
pandas: Data manipulation library (not directly used in the code snippet but can be used for data analysis in the future).
plotly.express: A plotting library for interactive visualizations (also not directly used here).
PIL: Used for handling image uploads.
time: Allows for time delays, such as showing loading spinners.
The appv3 module imports the AI agent interaction functions invoke_llm_with_user_question and the Agent_Executor_Class.
2. Streamlit Configuration:
The app is configured using st.set_page_config, setting page title, icon, layout, and sidebar state.

3. Custom CSS Styling:
The st.markdown block contains custom CSS to improve the appearance of the app, adding gradients, customized sidebar, and a loading spinner animation for improved UX.

4. Loading Spinner and Agent Initialization:
The spinner is displayed if the app is in the loading phase (st.spinner('Loading...')), and a delay is introduced using time.sleep(2).
The agent object is initialized using the Agent_Executor_Class from appv3, which is saved into st.session_state to ensure the agent is not reinitialized unnecessarily.
This AI agent likely handles querying both structured (SQL) and unstructured (PDF) data, based on the earlier code.
5. Chat History Management:
The app maintains chat history using st.session_state.chat_history. It ensures that the chat messages persist across app reruns, enabling a smooth conversational flow.

6. Sidebar Features:
Navigation: A sidebar radio button allows the user to navigate between different pages ("Home", "Insights", "About Us").
Document Upload: Users can upload documents (PDF, DOCX, TXT). Uploaded files are acknowledged with a success message.
7. Main Content:
Chatbot Interface:
The app welcomes users with a title and description, introducing them to EGAA's loan management solution.
Users can interact with the AI assistant by typing questions into a chat input box. Their messages and responses are displayed in a chat-like format using st.chat_message.
The AI agent responds to user queries via the invoke_llm_with_user_question function, which processes the question and generates the appropriate financial or loan-related insight.
8. About Us Section:
This page provides information about the company EGAA and displays the team members, including placeholders for images and details about team roles.
9. Footer (Commented Out):
There is a placeholder for a footer section that includes copyright information, but it is currently commented out.


********************************************************************************************************************************************************************************************************
db.ipynb-: Individual code for Database querying

********************************************************************************************************************************************************************************************************
V1_Rag_on_Pdf.ipynb-: Individual code for PDF File querying