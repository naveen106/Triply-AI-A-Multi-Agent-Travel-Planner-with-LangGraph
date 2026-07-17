import certifi
import os
from dotenv import load_dotenv

load_dotenv()

#for setting the SSL certificate file path to the certifi package's certificate bundle. 
# This is useful for ensuring that HTTPS requests made by the application use a trusted set 
# of root certificates, which can help prevent SSL/TLS errors when making secure connections 
# to external services.
os.environ["SSL_CERT_FILE"] = certifi.where() 
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where() #for setting the CA bundle path for the requests library to the certifi package's certificate bundle. This ensures that HTTPS requests made using the requests library use a trusted set of root certificates, which can help prevent SSL/TLS errors when making secure connections to external services.

from typing import TypedDict, Annotated #for type hinting and defining structured data types
import operator #for sorting the dictionary based on values
import uuid #for generating unique identifiers

import psycopg #for PostgreSQL database connection
from psycopg.rows import dict_row #for returning query results as dictionaries

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import(
    AnyMessage,
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq
from groq import Groq
from groq import BadRequestError
from tools.tavily_tool import tavily_search, exa_search
from tools.flight_tool import search_flights

def get_database_url():
    """
    Get the database URL from environment variables.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set. Please add your Render PostgreSQL database URL to the .env file.")

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please add your Groq API key to the .env file.")


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    # model="llama-3.1-8b-instant",
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7,
    max_tokens=2048,
)


def _compact_text(value: str, limit: int = 20000) -> str:
    """Trim long tool output so the LLM prompt stays within request limits."""
    text = str(value or "")
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[truncated]"

class TravelState(TypedDict):
    """
    A TypedDict representing the state of a travel-related conversation.
    """
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls_made:int


# =============================
#         FLIGHT AGENT
#==============================

def flight_agent(state:TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)

    return {
        "flight_results":flight_data,
        "messages":[AIMessage(content="Flight results have been fetched successfully.")],
        "llm_calls_made":state.get("llm_calls_made", 0) + 1
    }

# =============================
#         HOTEL AGENT
#==============================

def hotel_agent(state:TravelState):
    query = state["user_query"]
    hotel_data = exa_search(query) #also try tavily search after checking if this is working correctly

    return {
        "hotel_results":hotel_data,
        "messages":[AIMessage(content="Hotel results have been fetched successfully.")],
        "llm_calls_made":state.get("llm_calls_made", 0) + 1
    }

# =============================
#       ITINERARY AGENT
#==============================

def itinerary_agent(state:TravelState):
   
    query = state["user_query"]
    flight_results = state.get("flight_results","")
    hotel_results = state.get("hotel_results","")
    

    compact_flight_results = _compact_text(flight_results, 2500)
    compact_hotel_results = _compact_text(hotel_results, 2500)

    itinerary_prompt = f"""
    User Query: {query}
    
    Flight Results: {compact_flight_results}
    
    Hotel Results: {compact_hotel_results}
    
    Please create a practical itinerary, budget-aware and easy to follow.
    """

    try:
        itinerary_response = llm.invoke([
            SystemMessage(content="You are an expert travel planner."),
            HumanMessage(content=itinerary_prompt),
        ])
    except BadRequestError:
        itinerary_response = AIMessage(content="I could not generate the itinerary because the provided travel data was too large for the model request.")
    
    itinerary_text = itinerary_response.content if itinerary_response else "No itinerary generated."

    return {
        "itinerary":itinerary_text,
        "messages":[itinerary_response],
        "llm_calls_made":state.get("llm_calls_made", 0) + 1
    }



# ==================================
#       FINAL RESPONSES AGENT
#===================================

def final_agent(state:TravelState):
    compact_flight_results = _compact_text(state.get("flight_results", ""), 2000)
    compact_hotel_results = _compact_text(state.get("hotel_results", ""), 2000)
    compact_itinerary = _compact_text(state.get("itinerary", ""), 2000)

    final_prompt = f"""
    Generate the final travel response for the user.
    User Request: {state['user_query']}
    Flights: {compact_flight_results}
    Hotels: {compact_hotel_results}
    Itinerary: {compact_itinerary}

    Format the final answer beautifully usint these sections:

    1. Trip Summary
    2. Flight Details
    3. Hotel Details
    4. Day-By-Day Itinerary
    5. Estimated Budget
    6. Final Recommendations

    Important:
    - Be clear and practical.
    - Mention that live flight API may not provide ticket prices if pricing is unavailable.
    - Keep the response not too lengthy and useful for real travel planning.

    """

    try:
        response = llm.invoke([
            SystemMessage(content="You are a professional AI travel booking assistant."),
            HumanMessage(content=final_prompt),
        ])
    except BadRequestError:
        response = AIMessage(content="I could not generate the final travel response because the request was too large for the model.")
    
    return {
        "messages": [response],
        "llm_calls_made" : state.get("llm_calls_made",0)+1
    }



# =============================
#         BUILD GRAPH
#==============================
    
graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)



# =============================
#   PostgreSQL Checkpointer
#==============================

DATABASE_URL = get_database_url()

_conn = psycopg.connect(DATABASE_URL, autocommit=True, row_factory=dict_row)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

travel_graph = graph.compile(checkpointer = checkpointer)


# =============================
#       Function for FastAPI
#==============================

def run_travel_agent(user_input:str, thread_id: str | None = None):
    if not thread_id:
        thread_id = f"user_u{uuid.uuid4().hex}"

    config = {
        "configurable": {"thread_id": thread_id}
    }

    result = travel_graph.invoke({
        "messages":[HumanMessage(content=user_input)],
        "user_query": user_input,
        "flight_results":"",
        "hotel_results":"",
        "itinerary":"",
        "llm_calls_made":0
    },config=config)

    final_answer = result["messages"][-1].content

    return {
            "thread_id":thread_id,
            "messages":[HumanMessage(content=user_input)],
            "answer": final_answer,
            "flight_results":result.get("flight_results",""),
            "hotel_results":result.get("hotel_results",""),
            "itinerary":result.get("itinerary",""),
            "llm_calls_made":result.get("llm_calls_made",0)
        }
    