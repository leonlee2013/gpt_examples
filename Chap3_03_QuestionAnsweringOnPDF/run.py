from dotenv import load_dotenv

load_dotenv()
from intentservice import IntentService, get_intent
from responseservice import ResponseService, generate_response
from dataservice import DataService

# Example pdf
pdf = 'files/ExplorersGuide.pdf'

data_service = DataService()

# Drop all data from redis if needed
data_service.drop_redis_data()

# Load data from pdf to redis
data = data_service.pdf_to_embeddings(pdf)

data_service.load_data_to_redis(data)

intent_service = IntentService()
response_service = ResponseService()

# Question 
question = 'Where to find treasure chests?'
# Get the intent
intents = get_intent(question)
# Get the facts
facts = data_service.search_redis(intents)
# Get the answer
answer = generate_response(facts, question)
print(answer)
