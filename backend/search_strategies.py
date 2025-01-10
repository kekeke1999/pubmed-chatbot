from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    
    def __init__(self, client, model_id: str):
        self.client = client
        self.model_id = model_id

    @abstractmethod
    def search(self, query_parts: list[str], k: int, size: int) -> list[dict]:
        """Abstract method to execute a search query"""
        pass

    def create_search_body(self, query_text, k, size):
        """
        Create a basic search body that supports full-text search and semantic search
        """
        query = {
            "hybrid": {
                "queries": [
                    {"match": {"abstract": query_text}},  # Full-text search
                    {"neural": {"chunk_vector": {"query_text": query_text, "model_id": self.model_id, "k": k}}}  # Semantic search
                ]
            }
        }
        return {"_source": {"exclude": ["chunk_vector"]}, "size": size, "query": query}

    def add_term_filter(self, search_body, term, value):
        """
        Add a term filter to the search body
        """
        for q in search_body["query"]["hybrid"]["queries"]:
            q.setdefault("bool", {}).setdefault("filter", []).append({"term": {f"{term}.keyword": value}})

    def add_year_range_filter(self, search_body, from_year, to_year):
        """
        Add a publication year range filter to the search body
        """
        for q in search_body["query"]["hybrid"]["queries"]:
            q.setdefault("bool", {}).setdefault("filter", []).append({
                "range": {"publication_year": {"gte": from_year, "lte": to_year}}
            })

    def perform_search(self, search_body, index_name='pubmed', search_pipeline='nlp-search-pipeline'):
        """
        Execute the search query
        """
        try:
            response = self.client.search(body=search_body, index=index_name, params={'search_pipeline': search_pipeline})
            return response.get('hits', {}).get('hits', [])
        except Exception as e:
            raise RuntimeError(f"Search failed: {e}")


class BasicSearchStrategy(SearchStrategy):
    """Basic search strategy: Full-text and semantic search"""

    def search(self, query_parts, k, size):
        query_text = query_parts[0]

        # Create the basic search body
        search_body = self.create_search_body(query_text, k, size)
        return self.perform_search(search_body)


class TermSearchStrategy(SearchStrategy):
    """Search strategy with term filtering"""

    def search(self, query_parts, k, size):
        query_text, term, value = query_parts

        # Create the basic search body
        search_body = self.create_search_body(query_text, k, size)

        # Add field filter logic
        self.add_term_filter(search_body, term, value)

        return self.perform_search(search_body)


class YearRangeSearchStrategy(SearchStrategy):
    """Search strategy with publication year range filtering"""

    def search(self, query_parts, k, size):
        query_text, from_year, to_year = query_parts

        # Create the basic search body
        search_body = self.create_search_body(query_text, k, size)

        # Add publication year range filter logic
        self.add_year_range_filter(search_body, from_year, to_year)

        return self.perform_search(search_body)


class TermYearRangeSearchStrategy(SearchStrategy):
    """Search strategy with both term filtering and publication year range filtering"""

    def search(self, query_parts, k, size):
        query_text, term, value, from_year, to_year = query_parts

        # Create the basic search body
        search_body = self.create_search_body(query_text, k, size)

        # Add term filter logic
        self.add_term_filter(search_body, term, value)

        # Add publication year range filter logic
        self.add_year_range_filter(search_body, from_year, to_year)

        return self.perform_search(search_body)


class SearchStrategyFactory:
    BASIC_QUERY_LENGTH = 1
    TERM_QUERY_LENGTH = 3
    YEAR_RANGE_QUERY_LENGTH = 4
    TERM_YEAR_RANGE_QUERY_LENGTH = 5
    
    @staticmethod
    def get_strategy(query_parts, client, model_id):
        if len(query_parts) == BASIC_QUERY_LENGTH:
            return BasicSearchStrategy(client, model_id)
        elif len(query_parts) == TERM_QUERY_LENGTH:
            return TermSearchStrategy(client, model_id)
        elif len(query_parts) == YEAR_RANGE_QUERY_LENGTH:
            return YearRangeSearchStrategy(client, model_id)
        elif len(query_parts) == TERM_YEAR_RANGE_QUERY_LENGTH:
            return TermYearRangeSearchStrategy(client, model_id)
        else:
            raise ValueError("Invalid query format")
