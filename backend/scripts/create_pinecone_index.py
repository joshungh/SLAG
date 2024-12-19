import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

def create_index():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENVIRONMENT")
    )
    
    # Create index if it doesn't exist
    if "slag-index" not in pinecone.list_indexes():
        pinecone.create_index(
            name="slag-index",
            dimension=1536,  # Claude's embedding dimension
            metric="cosine"
        )
        print("Index created successfully")
    else:
        print("Index already exists")

if __name__ == "__main__":
    create_index() 