from dotenv import load_dotenv

load_dotenv()
from intentservice import IntentService
from responseservice import ResponseService
from dataservice import DataService

# Example pdf
pdf = 'files/ExplorersGuide.pdf'

# data_service = DataService()

# Drop all data from redis if needed
# data_service.drop_redis_data()

# Load data from pdf to redis
# data = data_service.pdf_to_embeddings(pdf)

# data_service.load_data_to_redis(data)

intent_service = IntentService()
response_service = ResponseService()

# Question 
question = '哪里可以找到宝箱？'
# Get the intent
intents = get_intent(question)
print("intents", intents)
# Get the facts
# facts = data_service.search_redis(intents)
# Get the answer
facts = "在雷锋塔上"
answer = generate_response(facts, question)
print(answer)
