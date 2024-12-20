from opensearch_manager import OpenSearchManager
from retriever import CustomRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import os

API_KEY = os.getenv("api_key")
os.environ["OPENAI_API_KEY"] = API_KEY

def get_chain_result(question: str) -> str:
    """Get retrieval and answer results"""

    retriever = CustomRetriever()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.01, openai_api_key=API_KEY)
    template = """
        Role: You are a highly knowledgeable assistant specializing in scientific research, technical problem-solving, and detailed explanations. Your goal is to provide precise, context-based answers and only include relevant information.

        Instructions:
        1. Use the provided context to answer the question accurately. If you do not know the answer, clearly state, "I do not know," and do not attempt to guess or fabricate an answer.
        2. If the question text includes one or more '+++' markers, remove everything up to and including the last occurrence of '+++' from the question text. Then proceed with the remaining portion of the question. If there are no '+++' markers, use the question as it is.
        3. Ensure your response is concise and directly addresses the question, maintaining a professional tone.
        4. If you do not know the answer, state that you do not know, and do not attempt to guess or fabricate an answer.

        - **Context**: {context}
        - **Question**: {question}

        Example:
        Context:
        The user is researching ovarian aging reversal and has mentioned testing the effects of reduced Dox dosages in experiments on OSKM mice.

        Question:
        +++new+++How does reducing Dox dosage impact the safety and efficacy of ovarian aging reversal experiments in OSKM mice?

        Answer:
        Reducing Dox dosage can decrease the risk of toxicity and mortality in OSKM mice, as high doses have been associated with adverse effects. However, this may also reduce the induction efficiency of OSKM factors, potentially impacting the extent of ovarian aging reversal. Pilot studies to optimize the balance between safety and efficacy are recommended.

        Now, proceed with the provided context and question.
    """

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PromptTemplate(template=template, input_variables=["context", "question"])}
    )

    result = qa_chain.invoke({"query": question})
    return result["result"]

