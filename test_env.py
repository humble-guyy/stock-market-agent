import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Print API key to check if it loads correctly
print(os.getenv("OPENAI_API_KEY"))
