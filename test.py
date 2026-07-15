#for testing functions and files working properly or not.

from tools.tavily_tool import tavily_search
from tools.tavily_tool import exa_search
# res = tavily_search("Best Hotels in India")

res = exa_search("Best Hotels in India")
print(res)