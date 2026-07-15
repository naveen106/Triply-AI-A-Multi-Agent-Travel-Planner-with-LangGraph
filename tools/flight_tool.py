import airportsdata
import pycountry
import os
import re
import certifi
from dotenv import load_dotenv

load_dotenv()

#If we are windows file system, we need to set the SSL_CERT_FILE and REQUESTS_CA_BUNDLE environment variables to the path 
# of the certifi certificate bundle. Because Windows does not have a default certificate store 
# like Linux and macOS do, and some libraries (like requests) rely on this environment variable
#  to find the certificate bundle.
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

API_KEY = os.getenv("AVIATION_API_KEY")


DEFAULT_ORIGIN_DATA =  os.getenv("DEFAULT_ORIGIN_DATA", "DAC") 
BASE_URL = "https://api.aviationstack.com/v1/flights"
AIRPORTS = airportsdata.load('IATA')  # Load IATA airport data

COUNTRY_ALIASES = {
    "USA": "United States",
    "USA": "United States of America",
    "USA": "America",
    "USA": "U.S.A",
    "UK": "United Kingdom",
    "UK": "England",
    "UAE": "United Arab Emirates",
    "DE":"Germany",
    "FR":"France",
    "ES":"Spain",
    "IT":"Italy",
    "CA":"Canada",
    "AU":"Australia",
    "BR":"Brazil",
    "TR":"Turkey",
    "MY":"Maylaysia",
    "TH":"Thailand",
    "ID":"Indonesiz",
    "NP":"Nepal",
    "QA":"Qatar",
    "UAE": "Dubai",
    "KSA": "Saudi Arabia",
    "PRC": "China",
    "ROC": "Taiwan",
    "DPRK": "North Korea",
    "ROK": "South Korea",
    "IN": "India",
    "JP": "Japan",
    "RU": "Russia",
    "VN": "Vietnam",
    "BD": "Bangladesh",
    "SG": "Singapore"
}

#Preferred main airport for country level search
COUNTRY_MAIN_AIRPORTS = {
    "US":"JFK",
    "UK":"LHR",
    "SA":"JED",
    "DE": "FRA",
    "FR": "CDG",
    "ES": "MAD",
    "IT": "FCO",
    "CA": "YYZ",
    "AU": "SYD",
    "BR": "GRU",
    "TR": "IST",
    "MY": "KUL",
    "TH": "BKK",
    "ID": "CGK",
    "NP": "BIR",
    "QA": "DOH",
    "UAE": "DXB",
    "KSA": "JED",
    "PRC": "PEK",
    "ROC": "TPE",
    "DPRK": "FNJ",
    "ROK": "ICN",
    "IN": "BOM",
    "JP": "HND",
    "RU": "SVO",
    "VN": "SGN",
    "BD": "DAC",
    "SG": "SIN"
}
