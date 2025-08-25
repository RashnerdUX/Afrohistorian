from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

def semantic_split_text(text):
    """
    Split text into semantic chunks. Embedding also occurs here

    Args:
        text (document): The document to split.
    Returns:
        list<str>: List of semantic chunks.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    # I need to pick between the "all-mpnet-base-v2" and
    # "sentence-transformers/all-MiniLM-L6-v2" models based on what we need
    # "all-mpnet-base-v2" is more accurate but larger, while
    # "sentence-transformers/all-MiniLM-L6-v2" is smaller and 5x faster.
    try:
        chunker = SemanticChunker(embeddings=embeddings)
        chunks = chunker.create_documents(text)
        return chunks
    except Exception as e:
        print(f"Error splitting text into semantic chunks: {e}")
        return []
