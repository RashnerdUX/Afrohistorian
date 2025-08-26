from langchain_core.prompts import PromptTemplate
from text_to_vector import retrieve_vector_from_pinecone
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from decouple import config

# The standard function to run the Afrohistorian application
def afrohistorian(text:str) -> dict:
    """
    Main function to run the Afrohistorian application.
    """

    template = """
    You are Afrohistorian, an AI assistant that specializes in African history. 
    Your task is to provide accurate and detailed information about various aspects of African history, including significant events, cultural practices, historical figures, and more.
    
    Here are some documents for context: {context}
    Based on the provided documents, please answer the following question: {question}
    """

    try:
        # Initialize the prompt template
        prompt = PromptTemplate.from_template(template)

        # Get the context for the answer from Pinecone
        result = retrieve_vector_from_pinecone(query=text, index_name="afrohistorian", top_k=5)
        context = result["results"]

        # Initialize the language model
        open_api_key = config("OPENAI_API_KEY", default="my-openai-api-key")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,
                         openai_api_key=open_api_key)

        # Create the final prompt with context and question
        final_prompt = prompt.format(context=context, question=text)

        # Get the response from the language model
        response = llm.invoke(final_prompt)

        """
        TODO:Let's use RAG chain to improve the response quality.\
        output_parser = StrOutputParser()
        rag_chain = prompt | llm | output_parser
        for chunk in rag_chain.stream(final_prompt):
            print(chunk, end="", flush=True)
        """
        print(response)
        return {
            "message": "Success",
            "response": response,
        }
    except Exception as e:
        print(f"Error in Afrohistorian: {e}")
        return {
            "message": str(e),
            "response": None
        }

# An advanced stream version that uses LCEL for streaming responses
def afrohistorian_stream(text: str) -> dict:
    """
    Main function to run the Afrohistorian application.
    """

    template = """
    You are Afrohistorian, an AI assistant that specializes in African history. 
    Your task is to provide accurate and detailed information about various aspects of African history, including significant events, cultural practices, historical figures, and more.

    Here are some documents for context: {context}
    Based on the provided documents, please answer the following question: {question}
    """

    try:
        # Initialize the prompt template
        prompt = PromptTemplate.from_template(template)

        # Get the context for the answer from Pinecone
        result = retrieve_vector_from_pinecone(
            query=text, index_name="afrohistorian", top_k=5
        )
        context = result["results"]

        # Initialize the language model
        open_api_key = config("OPENAI_API_KEY", default="my-openai-api-key")
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0, openai_api_key=open_api_key
        )

        # Get the response from the language model
        output_parser = StrOutputParser()
        rag_chain = prompt | llm | output_parser
        for chunk in rag_chain.stream({"context": context, "question": text}):
            print(chunk, end="", flush=True)
            yield {
                "message": "Success",
                "response": chunk,
            }
    except Exception as e:
        print(f"Error in Afrohistorian: {e}")
        return {"message": str(e), "response": None}
