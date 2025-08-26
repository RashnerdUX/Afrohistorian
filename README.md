# Afrohistorian

An AI-powered assistant specialized in African history, built using Retrieval-Augmented Generation (RAG) with Pinecone vector database and OpenAI's GPT models.

## Overview

Afrohistorian is designed to provide accurate and detailed information about various aspects of African history, including significant events, cultural practices, historical figures, and more. The system uses semantic search to retrieve relevant historical documents and generates contextual responses using advanced language models.

## Features

- **Semantic Document Search**: Uses HuggingFace embeddings for intelligent document retrieval
- **RAG Architecture**: Combines retrieved context with GPT-3.5-turbo for accurate responses
- **PDF Processing**: Converts PDF documents to text with core content extraction
- **FastAPI Integration**: RESTful API for easy integration
- **Vector Database**: Utilizes Pinecone for efficient similarity search

## Architecture

```
PDF Documents → Text Extraction → Semantic Chunking → Vector Embeddings → Pinecone Storage
                                                                              ↓
User Query → Vector Search → Context Retrieval → GPT Response → Final Answer
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RashnerdUX/Afrohistorian.git
cd Afrohistorian
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=afrohistorian
```

## Usage

### Command Line Interface

Run the interactive CLI:
```bash
python main.py
```

### FastAPI Server

Start the API server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `GET /`: Welcome message
- `POST /ask`: Submit a query about African history
  ```json
  {
    "query": "What constituted the Trans-saharan trade?"
  }
  ```

### Document Processing

#### Convert PDF to Text
```bash
python convert_to_txt.py <pdf_file> [output_file]
```

#### Upload Documents to Vector Database
```bash
python text_to_vector.py <text_file>
```

## Components

### Core Modules

- **`chat.py`**: Main chat functionality with RAG implementation
- **`text_to_vector.py`**: Vector database operations (upload/retrieval)
- **`split_text.py`**: Semantic text chunking using HuggingFace embeddings
- **`convert_to_txt.py`**: PDF to text conversion with content extraction
- **`main.py`**: CLI interface and FastAPI application

### Key Features

#### Semantic Text Splitting
Uses `SemanticChunker` with `all-mpnet-base-v2` embeddings to create meaningful document chunks that preserve context.

#### Smart PDF Processing
- Extracts core content from Introduction/Prologue to Conclusion/Epilogue
- Removes headers, footers, and page numbers
- Preserves chapter structure and formatting

#### Vector Search
- Similarity-based retrieval with configurable score threshold
- Top-k results for comprehensive context
- Metadata preservation for source attribution

## Configuration

### Embedding Models
The system uses HuggingFace embeddings with two model options:
- `all-mpnet-base-v2`: Higher accuracy, larger model
- `all-MiniLM-L6-v2`: Faster processing, smaller model

### Search Parameters
- **top_k**: Number of retrieved documents (default: 5)
- **score_threshold**: Minimum similarity score (default: 0.6)
- **temperature**: Response creativity (default: 0)

## Development

### Project Structure
```
Afrohistorian/
├── chat.py                 # Main RAG functionality
├── convert_to_txt.py       # PDF processing
├── main.py                 # CLI and API interface
├── requirements.txt        # Dependencies
├── split_text.py          # Text chunking
├── text_to_vector.py      # Vector operations
├── .env                   # Environment variables
└── .gitignore            # Git ignore rules
```

### Testing

The project includes pytest configuration for testing:
```bash
pytest
```

### Adding New Documents

1. Convert PDF to text:
   ```bash
   python convert_to_txt.py your_document.pdf
   ```

2. Upload to vector database:
   ```bash
   python text_to_vector.py your_document.txt
   ```

## Dependencies

Key libraries used:
- **LangChain**: RAG framework and document processing
- **Pinecone**: Vector database
- **OpenAI**: Language model API
- **HuggingFace**: Embedding models
- **FastAPI**: Web framework
- **PyPDF**: PDF processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

## Support

For questions or support, please email me at [akhigbek6@gmail.com](mailto:akhigbek6@gmail.com) or create an issue in the repository.

## Roadmap

- [ ] Support for more document formats
- [ ] Enhanced PDF processing with chapter detection
- [ ] Multi-language support
- [ ] Advanced query processing
- [ ] Web interface
- [ ] Batch document processing
- [ ] Performance optimization

---

*Built with ❤️ for African history education and research*
