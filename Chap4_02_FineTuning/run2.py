from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# Load environment variables (assumes OPENAI_API_KEY is set in the .env file)
load_dotenv()

# Initialize OpenAI client
client = OpenAI()


# Define a function for chat completion
def chat_completion(prompt, model="gpt-4", temperature=0):
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return res.choices[0].message.content


# Lists for sectors, cities, and sizes
# l_sector = ['Grocery Stores', 'Restaurants', 'Fast Food Restaurants', 'Pharmacies', 'Service Stations (Fuel)',
#             'Electronics Stores']
# l_city = ['Brussels', 'Paris', 'Berlin']
# l_size = ['small', 'medium', 'large']
# l_sector = ['杂货店', '餐馆', '快餐店', '药店', '加油站', '电子产品商店']
# l_city = ['布鲁塞尔', '巴黎', '柏林']
# l_size = ['小型', '中型', '大型']
l_sector = ['餐馆', '加油站']
l_city = ['布鲁塞尔', '巴黎']
l_size = ['小型', '大型']

# Define the prompt template
# f_prompt = """
# Role: You are an expert content writer with extensive direct marketing experience. You have strong writing skills, creativity, adaptability to different tones and styles, and a deep understanding of audience needs and preferences for effective direct campaigns.
# Context: You have to write a short message in maximum 2 sentences for a direct marketing campaign to sell a new e-commerce payment service to stores.
# The target stores have the three following characteristics:
# - The sector of activity: {sector}
# - The city where the stores are located: {city}
# - The size of the stores: {size}
# Task: Writes the short message for the direct marketing campaign. To write this message, use your skills defined in your role! It is very important that the messages you produce take into account the product you want to sell and the characteristics of the store you want to write to.
# """
f_prompt = """
角色: 您是具有丰富直销经验的内容写作专家。您拥有强大的写作能力、创造力、适应不同语气和风格的能力，以及对受众需求和偏好的深入理解，以便进行有效的直接营销活动。
背景: 您需要为一个直销活动撰写最多两句的简短信息，以向商店销售一种新的电子商务支付服务。
目标商店具有以下三个特征：

 - 业务领域: {sector}
 - 商店所在城市: {city}
 - 商店规模: {size} 
 任务: 为直销活动撰写简短信息。撰写此信息时，请使用您在角色中定义的技能！您生产的信息必须考虑到您想要销售的产品以及您想要撰写的商店的特征。 """

# Create a DataFrame to store results
df = pd.DataFrame()

# Generate responses for each combination
for sector in l_sector:
    for city in l_city:
        for size in l_size:
            for i in range(3):  # Generate 3 variations for each combination
                prompt = f_prompt.format(sector=sector, city=city, size=size)
                response_txt = chat_completion(prompt, model='gpt-3.5-turbo', temperature=1)
                # Create a new row with prompt and completion
                new_row = {
                    'prompt': f"{sector}, {city}, {size}",
                    'completion': response_txt
                }
                print(f'new_row {new_row}')

                # Append the new row to the DataFrame
                df = pd.concat([df, pd.DataFrame([new_row])], axis=0, ignore_index=True)

# Save the results to a CSV file
# df.to_csv("out_openai_completion.csv", index=False)
df.to_csv("out_openai_completion2.csv", index=False)
# $ openai tools fine_tunes.prepare_data -f out_openai_completion2.csv
