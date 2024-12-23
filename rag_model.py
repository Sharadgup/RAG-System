import openai
from dotenv import load_dotenv
import os

load_dotenv()

class RAGModel:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")
        openai.api_key = self.api_key

        # Initialize your document store here (use a vector database in a real system)
        self.document_store = []  # Placeholder for demonstration

    def query(self, user_input):
        # Implement RAG logic
        context = self.retrieve_relevant_documents(user_input)
        response = self.generate_response(user_input, context)
        return response

    def retrieve_relevant_documents(self, query):
        # Dummy document retrieval logic (replace with real implementation)
        return "This is a relevant document for the query."

    def generate_response(self, query, context):
        # Generate response using OpenAI's GPT-3.5-turbo
        prompt = f"Context: {context}\n\nQuery: {query}\n\nResponse:"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message['content'].strip()
        except openai.error.OpenAIError as e:  # Corrected exception class usage
            return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    rag_model = RAGModel()
    user_query = "How do I take care of a Monstera plant?"
    response = rag_model.query(user_query)
    print("RAG Response:", response)
