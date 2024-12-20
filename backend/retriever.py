from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from search_strategies import SearchStrategyFactory
from opensearch_manager import OpenSearchManager

class CustomRetriever(BaseRetriever):

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        manager = OpenSearchManager()
        if not manager.client:
            raise RuntimeError("OpenSearch is not available")

        # Parse query and select search strategy
        query_parts = query.split('+++')
        strategy = SearchStrategyFactory.get_strategy(query_parts, manager.client, manager.model_id)
        
        # Execute search
        results = strategy.search(query_parts, k=100, size=2)
        return [Document(page_content=res['_source']['abstract']) for res in results]
