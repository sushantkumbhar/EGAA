# from langchain.agents import create_sql_agent, initialize_agent
# from langchain.agents.agent_types import AgentType
from langchain.chains import RetrievalQA
# from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader


from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool, QuerySQLCheckerTool

# Set up retrieval for unstructured data
OPENAI_API_KEY=""
HUGGINGFACE_API_KEY=""



#define llm
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

host = 'localhost'
port = '5432'
username = 'postgres'
password = 'postgres'
database_schema = 'test8'
# Create SQLite connection and cursor
# conn = sqlite3.connect(sqlite_file)
# cursor = conn.cursor()
pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_schema}"
db = SQLDatabase.from_uri(pg_uri)

# Set up tool for querying unstructured data
loader = PyPDFLoader('./Documents/Loan.pdf')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# print('Texts: ',texts)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Chroma.from_documents(texts, embeddings)

retriever = vectorstore.as_retriever()
retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

unstructured_qa_tool = Tool(
    name="Unstructured Data QA",
    func=retrieval_qa.invoke,
    description="Useful for answering questions about loan information from the PDF document. This tool uses a retrieval-based QA system to find relevant information in the unstructured text of the loan document. If anything regarding compliance or policy or information is asked please query this tool"
)

# # Initialize the agent with both tools
# tools = [db_query_tool, ]

tools = [unstructured_qa_tool, QuerySQLDataBaseTool(db = db), InfoSQLDatabaseTool(db = db), ListSQLDatabaseTool(db = db), QuerySQLCheckerTool(db = db, llm = llm)]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

from langchain.agents import AgentExecutor, create_react_agent



# # Example usage
system_prefix = """You are an agent designed to interact with a document repository ans a SQL database.
The AI assistant has access to two types of data sources:
1. **Vector Database**: Contains unstructured data such as loan agreements, disputes, loan tenure details, terms of contracts, legal provisions, and other textual information from legal documents stored as vector embeddings.
2. **Structured Database**: Contains detailed information related to loans and transactions (e.g., loan amounts, interest rates, loan start and end dates, repayment schedules, transaction dates, and amounts).

Please refer to below instructions for accessing unstructured data in the Vector Database-
The document repository contains information about loan agreement and policies
Given an input question, create a semantically correct query that will be used to fetch relevant information then look at the results of the query.

Please refer to below instructions for accessing structured data in the SQL Database-
Given an input question, create a syntactically correct postgres query to run, then look at the results of the query.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 15 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
Please reason step-by-step through the following process:
1. What is the user asking?
2. Run describe queries to understand tables and schemas first.
3. Figure out what tables and columns are relevant?
4. Are any joins, filters, or conditions required?
5. Formulate and execute the SQL query based on the information.

You have access to the following tools for interacting with the database:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {tool_names}
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

NEVER, I repeat NEVER return proxy values like '$XXXX', return actual values when asked for.

ALWAYS make the first query, at the start of chain, to the unstructured data tool, so as to have better context for answering the question.
If the question does not seem related to the database, just return "I don't know" as the answer.
If you see you are repeating yourself, just provide final answer and exit.

Based on the user's prompt, the AI assistant must decide:
- **For loan and transaction-related queries**, the assistant retrieves and processes structured data from the relational database. These queries might include details about loan status, payments, amounts, interest rates, or transactional history.
- **For loan agreement or contract-related queries**, the assistant fetches relevant information from the vector database, summarizes important clauses, terms, tenure, disputes, or specific contractual conditions related to loans.

Ensure that the AI provides appropriate data insights depending on the data source used, follows the specified data format.

"""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prefix),
        ("human", "{input}"),
        ("system", "{agent_scratchpad}"),
    ]
)

agent = create_react_agent(
    llm, tools, full_prompt
)

# # Function to interact with the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=150)

last_k_messages = 4


from langchain_community.chat_message_histories import SQLChatMessageHistory

def get_session_history(session_id):
    chat_message_history = SQLChatMessageHistory(
    session_id=session_id, connection = "sqlite:///memory.db", table_name = "local_table"
    )

    messages = chat_message_history.get_messages()
    chat_message_history.clear()
    
    for message in messages[-last_k_messages:]:
        chat_message_history.add_message(message)
    
    print("chat_message_history ", chat_message_history)
    return chat_message_history

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
# )
def chat_with_agent(user_input):
    response = agent.invoke(user_input)
    return response

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool, QuerySQLCheckerTool


def get_user_input_and_invoke_llm():
    while True:
        user_question = input("Please enter your question (or 'quit' to exit): ")
        if user_question.lower() == 'quit':
            break
        try:
            # input_element = {
            #     "input": user_question,
            #     "tool_names": [tool.name for tool in tools],
            #     "tools": [tool.name + " - " + tool.description.strip() for tool in tools],
            #     "agent_scratchpad": [],
            #     "system_prefix": system_prefix
            # }
            
            # prompt_val = full_prompt.invoke(input_element)
            answer = agent_executor.invoke({"input": user_question})
        except IndexError:
            print("An error occurred: IndexError - list index out of range")
            answer = {"output": "Sorry, I encountered an error while processing your question. Please try again."}
        print("\nAnswer:", answer['output'])
        print("\n" + "-"*50 + "\n")

def invoke_llm_with_user_question(user_question: str):
    answer = agent_executor.invoke({"input": user_question})
    print(f'Answer of the question {user_question} is : \n {answer}')
    return answer['output']

print('SUCCESSFUL')
