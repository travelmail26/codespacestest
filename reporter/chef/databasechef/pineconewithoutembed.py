import os
from pinecone import Pinecone

# Replace with your Pinecone API key
api_key = "pcsk_6EcGgx_U35MgRmkm23gMgVFWgd3Z2pUQUC2CAVJ1oaHhiz6gH7RFQxUxZVJUTeJHYipBiW"

# Initialize Pinecone
pc = Pinecone(api_key=api_key)

# Define the index name and namespace
index_name = "example-index"
namespace = "example-namespace"

# Access the existing index
if index_name not in pc.list_indexes().names():
    raise ValueError(f"Index '{index_name}' does not exist. Please verify the index name.")

index = pc.Index(index_name)

# Define your query
query = "What is fruit?"

# Generate embedding for the query
query_embedding = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={
        "input_type": "query"
    }
)

# Search the index for the most similar vectors
results = index.query(
    namespace=namespace,
    vector=query_embedding[0].values,
    top_k=3,
    include_values=False,
    include_metadata=True
)

# Display results
print("\nSearch Results:")
if results.get("matches"):
    for match in results["matches"]:
        print(f"ID: {match['id']}, Score: {match['score']:.4f}")
        print(f"Text: {match['metadata']['text']}")
else:
    print("No matches found!")
