from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GOOGLE_API_KEY']=os.getenv['GOOGLE_API_KEY']
os.environ['TAVILY_API_KEY']=os.environ['TAVILY_API_KEY']