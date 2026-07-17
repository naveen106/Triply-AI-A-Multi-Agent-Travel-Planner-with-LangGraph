#for testing functions and files working properly or not.

from tools.tavily_tool import tavily_search
from tools.tavily_tool import exa_search
from backend import run_travel_agent
# res = tavily_search("Best Hotels in India")

# res = exa_search("Best Hotels in India")
# print(res)

# user_input = input("Enter travel request: ")
user_input = "Plan a complete 7 days trip from India to Nepal including flights, hotels and sightseeing under 2 lakh rupees."
response = run_travel_agent(
    user_input=user_input,
    thread_id="test_user"
)

print("\n\nFINAL RESPOSNE\n\n")
print(response["answer"])