import openai
from dotenv import load_dotenv
import os

load_dotenv()

class RAGModel:
    def __init__(self):
        self.client = openai
        # Initialize your document store here
        self.document_store = []

    def query(self, user_input):
        # Implement RAG logic here
        context = self.retrieve_relevant_documents(user_input)
        response = self.generate_response(user_input, context)
        return response

    def retrieve_relevant_documents(self, query):
        # Implement document retrieval logic
        # For simplicity, we'll just return a dummy context
        return "This is a relevant document for the query."

    def generate_response(self, query, context):
        prompt = f"Context: {context}\n\nQuery: {query}\n\nResponse:"
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message['content'].strip()

        except openai.OpenAIError as e:  # Corrected exception class usage
            print(f"Error occurred: {e}")
            return "An error occurred while generating the response."
