# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_6EcGgx_U35MgRmkm23gMgVFWgd3Z2pUQUC2CAVJ1oaHhiz6gH7RFQxUxZVJUTeJHYipBiW")

# Define a sample dataset where each item has a unique ID and piece of text
data = [
    {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
    {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
    {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
    {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
    {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
    {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
]

# Convert the text into numerical vectors that Pinecone can index
embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[d['text'] for d in data],
    parameters={"input_type": "passage", "truncate": "END"}
)

# Validate the embeddings structure
print("Generated Embeddings:")
for emb in embeddings.data:
    print(emb)

# Create a serverless index
index_name = "example-index"

existing_indexes = pc.list_indexes()
if index_name not in [index.name for index in existing_indexes]:
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# Target the index where you'll store the vector embeddings
index = pc.Index("example-index")

# Prepare the records for upsert
# Each contains an 'id', the embedding 'values', and the original text as 'metadata'
records = [
    {
        "id": d["id"],
        "values": emb["values"],
        "metadata": {"text": d["text"]}
    }
    for d, emb in zip(data, embeddings.data)
]

# Upsert the records into the index
try:
    index.upsert(
        vectors=records,
        namespace="example-namespace"
    )
    print("Upsert successful!")
except Exception as e:
    print(f"Upsert failed: {e}")

# Wait for the upserted vectors to be indexed
time.sleep(10)

# Check the index stats
stats = index.describe_index_stats()
print("Index Stats:")
print(stats)

# Define your query
query = "Tell me about the tech company known as Apple."

# Convert the query into a numerical vector that Pinecone can search with
query_embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
)

# Search the index for the three most similar vectors
results = index.query(
    namespace="example-namespace",
    vector=query_embedding[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)

# Print the results
print("\nSearch Results:")
if results.get('matches'):
    for match in results['matches']:
        print(f"ID: {match['id']}, Score: {match['score']:.4f}")
        print(f"Text: {match['metadata']['text']}")
else:
    print("No matches found!")
