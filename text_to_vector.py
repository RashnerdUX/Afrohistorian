from langchain_pinecone import PineconeVectorStore
import sys
import os
from decouple import config

from split_text import semantic_split_text

def save_vector_to_pinecone(vectors, index_name="afrohistorian"):
    """
    Save vectors to a Pinecone index.

    Args:
        vectors (list<Embeddings>): List of vectors to save.
        index_name (str): Name of the Pinecone index.
    """
    # Get the Pinecone API key and environment from environment variables
    pinecone_api_key = config("PINECONE_API_KEY", default="my-pinecone-api-key")
    print(f"Debug: Pinecone API Key: {pinecone_api_key}")
    try:
        PineconeVectorStore(index_name=index_name, embedding=vectors,
                            pinecone_api_key=pinecone_api_key)
        return True
    except Exception as e:
        print(f"Error saving vectors to Pinecone: {e}")
        return False


def retrieve_vector_from_pinecone(query:str, index_name:str="afrohistorian",
                                  top_k:int=5) -> dict:
    """
    Retrieve vectors from a Pinecone index based on a query.

    Args:
        query (str): The query string to search for.
        index_name (str): Name of the Pinecone index.
        top_k (int): Number of top results to retrieve.

    Returns:
        list<Embeddings>: List of retrieved vectors.
    """
    # TODO: Consider removing the k parameter and always using score_threshold
    # to filter results based on relevance.
    # Get the Pinecone API key and environment from environment variables
    pinecone_api_key = config("PINECONE_API_KEY", default="my-pinecone-api-key")
    try:
        vector_store = PineconeVectorStore(index_name=index_name, pinecone_api_key=pinecone_api_key)
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k, "score_threshold": 0.6,}
        )
        results = retriever.invoke(input=query)
        return {
            "status": "Success",
            "error": None,
            "results": results
        }
    except Exception as e:
        print(f"Error retrieving vectors from Pinecone: {e}")
        return {
            "status": "Error",
            "error": str(e),
            "results": []
        }

def main():
    """
    Main function to handle command line arguments
    It will take a text and upload it to pinecone
    1. It will split the text into semantic chunks
    2. It will embed the chunks using HuggingFaceEmbeddings
    3. It will save the vectors to pinecone
    4. It will print the status of the operation
    """
    # Ensure a file path is provided
    if len(sys.argv) < 2:
        print("Usage: python text_to_vector.py <text_file>")
        sys.exit(1)

    # Set the file path when running script
    file_path = sys.argv[1] if len(sys.argv) > 1 else None

    # Confirm that the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        sys.exit(1)

    # Confirm that the file is a .txt file
    # TODO: Check for txt file only for now, but later we can add support for pdf
    if not file_path.endswith('.txt'):
        print(f"Error: File {file_path} is not a .txt file")
        sys.exit(1)
    # Open and read txt file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into semantic chunks
    chunks = semantic_split_text(text)
    if not chunks:
        print("Error: No chunks created from the text")
        sys.exit(1)

    # Save the vector chunks to pinecone
    status = save_vector_to_pinecone(chunks)

    if status:
        print(f"Successfully uploaded {len(chunks)} chunks to Pinecone")
    else:
        print("Error uploading chunks to Pinecone")
        sys.exit(1)

if __name__ == "__main__":
    input("Please input the path to the text file you want to "
                      "embed and upload to Pinecone:\n")
    main()