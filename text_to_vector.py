from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import sys
import os
from dotenv import load_dotenv
from decouple import config

from split_text import semantic_split_text

def save_vector_to_pinecone(documents, index_name="afrohistorian"):
    """
    Save vectors to a Pinecone index.

    Args:
        documents (list<Documents>): List of vectors to save.
        index_name (str): Name of the Pinecone index.
    """
    # Load environment variables from a .env file
    load_dotenv()

    # Access environment variables directly using os.getenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", index_name)

    # Check if API key and index name were loaded
    if not pinecone_api_key or not pinecone_index_name:
        print(
            "Error: Pinecone API key or index name not found in environment variables."
        )
        return False

    print(f"Debug: Using Pinecone Index: {pinecone_index_name}")

    try:
        # Initialize the embeddings model
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        # Initialize the vector store using the loaded environment variables
        vector_store = PineconeVectorStore(index_name=pinecone_index_name,
                                           embedding=embeddings,)
        print(f"Debug: Pinecone Vector Store initialized: {vector_store}")

        # Add documents to the Pinecone index
        # This is the only code unchanged
        vector_store.add_documents(documents=documents)
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
    # Load environment variables from a .env file
    load_dotenv()

    # Access environment variables directly using os.getenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", index_name)

    # Check if API key and index name were loaded
    if not pinecone_api_key or not pinecone_index_name:
        print(
            "Error: Pinecone API key or index name not found in environment variables."
        )
        return {
            "status": "Error",
            "error": "Pinecone API key or index name not found in environment variables.",
            "results": []
        }
    print(f"Debug: Using Pinecone Index: {pinecone_index_name}")


    try:
        # Initialize the embeddings model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        # Initialize the vector store using the loaded environment variables
        print("Initializing Pinecone Vector store...")
        vector_store = PineconeVectorStore(index_name=index_name,
                                           embedding=embeddings,
                                           pinecone_api_key=pinecone_api_key)
        print("Pinecone Vector Store initialized.")

        # Retrieve documents from the Pinecone index
        print("Retrieving documents from Pinecone...")
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
    chunks = semantic_split_text(text, metadata={"source": file_path,
                                                 "author": "Multiple",
                                                 "title": "West African "
                                                          "History", "year":
                                                     "2018"})
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

def check_vector_store():
    """
    Check if the Pinecone vector store is accessible.
    """
    question = "What constituted the Trans-saharan trade?"
    result = retrieve_vector_from_pinecone(query=question,
                                           index_name="afrohistorian", top_k=1)
    if result["status"] == "Success":
        print("Pinecone vector store is accessible.")
        print("Vector store returned the following results:")
        for res in result["results"]:
            print(res)
    else:
        print(f"Error accessing Pinecone vector store: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"Accessing {sys.argv[1]} for text input...")
    input("Please confirm if the file_path argument is set correctly. Press Enter to continue...")
    main()