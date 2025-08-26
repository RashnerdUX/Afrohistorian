from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

def semantic_split_text(
        text,
        metadata=None) \
        -> (
        list):
    """
    Split text into semantic chunks. Embedding also occurs here

    Args:
        text (document): The document to split.
        metadata (dict): Metadata to associate with each chunk. Defaults to None.
    Returns:
        list<str>: List of semantic chunks.
    """
    if metadata is None:
        metadata = {"source": "textbook", "author": "TOAA"}
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    # I need to pick between the "all-mpnet-base-v2" and
    # "sentence-transformers/all-MiniLM-L6-v2" models based on what we need
    # "all-mpnet-base-v2" is more accurate but larger, while
    # "sentence-transformers/all-MiniLM-L6-v2" is smaller and 5x faster.
    try:
        chunker = SemanticChunker(embeddings=embeddings)
        chunks = chunker.create_documents([text], metadatas=[metadata])
        print(f"Here's how the chunks look like: {chunks}")
        return chunks
    except Exception as e:
        print(f"Error splitting text into semantic chunks: {e}")
        return []

if __name__ == "__main__":
    """
    The sole purpose of this was to check if I needed to format the chunks 
    for Pinecone
    """
    with open ("sample.txt", "r") as file:
        text = file.read()
    chunks = semantic_split_text(text, metadata={"source": "sample.txt",
                                                 "author": "Kelvin Akhigbe"})
    print(f"Number of chunks created: {len(chunks)}")
    print(f"Chunks: {chunks}")
