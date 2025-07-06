import pandas as pd
import os
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# Load .env file
load_dotenv()
API_KEY = os.getenv("WML_APIKEY")
PROJECT_ID = os.getenv("PROJECT_ID")

# Debug output
print("🔐 API Key Loaded:", API_KEY[:5] + "***")
print("📁 Project ID Loaded:", PROJECT_ID)

# Read prompt template
with open("prompts/sentiment_prompt.txt", "r") as file:
    prompt_template = file.read()

# Load review data
df = pd.read_csv("data/hotel_reviews.csv")
df["Sentiment"] = None
df["Topics"] = None

# Set generation parameters
params = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 100
}

# Load model
model = Model(
    model_id="google/flan-t5-xxl",  # 🔁 NEW working model
    params=params,
    credentials={
        "apikey": API_KEY,
        "url": "https://us-south.ml.cloud.ibm.com"  # Or your region
    },
    project_id=PROJECT_ID
)


# Run sentiment analysis
for i, row in df.iterrows():
    prompt = prompt_template.format(review_text=row["Review"])
    print(f"\n🧾 Prompt for review {i+1}:\n{prompt}")

    try:
        response = model.generate(prompt)

        raw_text = response["results"][0]["generated_text"]
        print("✅ Raw Text:", raw_text)
        lines = raw_text.strip().split("\n")

        sentiment_line = next((line for line in lines if "Sentiment:" in line), "")
        topics_line = next((line for line in lines if "Topics:" in line), "")

        df.at[i, "Sentiment"] = sentiment_line.replace("Sentiment:", "").strip()
        df.at[i, "Topics"] = topics_line.replace("Topics:", "").strip(" []")

    except Exception as e:
        print(f"❌ Error on review {i+1}: {e}")
        df.at[i, "Sentiment"] = "Error"
        df.at[i, "Topics"] = "Error"

# Save results
os.makedirs("output", exist_ok=True)
df.to_csv("output/results.csv", index=False)
print("\n✅ All reviews processed and saved to output/results.csv")
