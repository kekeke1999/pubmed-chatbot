# PubMed Abstracts ChatBot

## Description

### Area

- **PubMed:**  Abstracts of the articles published between the years 2013 to 2023 that contain the word “intelligence” in the abstract’s text.

## Architecture 
![avatar](/architecture.png)

## Organization
![avatar](/organization.png)

Our system's architecture showcases a robust RAG-based QA framework, where we've harnessed the power of FastAPI to build our back-end, ensuring a high-performance API with automatic interactive documentation. The back-end is pivotal in orchestrating the workflow, receiving user inquiries via our OpenUI5 front-end interface, which offers a seamless and intuitive user experience. LangChain serves as an integration layer, leveraging OpenSearch for efficient hybrid retrieval and interfacing with OpenAI's GPT-3.5-turbo to utilize its advanced language model for generating precise answers. This setup forms a cohesive unit within Docker containers, providing a scalable and easily deployable solution.

## User Interface 

We use OpenUI 5 as the frontend framework and FastAPI as the backend framework to construct  the user-friendly interface. It’s designed to assist users in getting answers in the PubMed publications with ease. Here's how you can use our system:

1. **Query Input Box**: This is where you can type in your specific questions.  It's located just above the 'Send' button and has a placeholder text that says "Type a question..." to guide you.

2. **Publication Year Filter**: You can specify the range of publication years for your search. Just select the starting year ('From') and the ending year ('To') from the drop-down menus to narrow down your results to that timeframe.

3. **Keyword Search**: You can search for articles based on various criteria. By selecting an option from the 'Keyword' drop-down menu, such as 'journal', 'title', 'pmid', 'authors', or 'first author', you tell our system what aspect of the publications you want to focus on. For instance, choosing 'journal' will search for articles published in a specific medical journal.

4. **Value Input**: After selecting your keyword category, you can type your specific search term into the 'Value' box. If you chose 'journal' as your keyword, you'd enter the name of the journal here.

5. **Send Button**: Once you've set all your search parameters, hit the 'Send' button to execute your search. Our system will then retrieve publications that match your criteria and the use the retrieved documents and your question to generate the answer.

<div align="center">
    <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExenNvNGJtNWM3N3BrYXYzenV3enk3NjkyN2txaTIxNTh6OHNxY2I3ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dvKwzxlQUfWfO2CQOu/giphy.gif">
</div>

- Casual Questions

  ![Casual Questions](/screenshots/causal_question.png)

- Complex Questions

  ![Complex Questions](/screenshots/complex_question.png)

- Confirmation Questions

  ![Confirmation Questions](/screenshots/confirmation_question.png)

- Factoid Type Questions

  ![Factoid Type Questions](/screenshots/factoid-type_question.png)

- Hypothetical Questions

  ![Hypothetical Questions](/screenshots/hypothetical_question.png)

- List Questions

  ![Hypothetical Questions](/screenshots/hypothetical_question.png)

- With Constraints

  ![With Constraints](/screenshots/with_constraint.png)

  
## Set Up

All the necessary code for set up OpenSearch service and web application in the directory /app. Please check the [User Guide](/User_Guide.md) to set up system.

