from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    """Base class for search strategies"""

    def __init__(self, client, model_id: str):
        self.client = client
        self.model_id = model_id

    @abstractmethod
    def search(self, query_parts: list[str], k: int, size: int) -> list[dict]:
        pass

    def create_search_body(self, query_text, k, size, term_filter=None, year_range=None):
        query = {
            "hybrid": {
                "queries": [
                    {"match": {"abstract": query_text}},
                    {"neural": {"chunk_vector": {"query_text": query_text, "model_id": self.model_id, "k": k}}}
                ]
            }
        }
        if term_filter:
            term, value = term_filter
            for q in query["hybrid"]["queries"]:
                q.setdefault("bool", {}).setdefault("filter", []).append({"term": {f"{term}.keyword": value}})
        if year_range:
            from_year, to_year = year_range
            for q in query["hybrid"]["queries"]:
                q.setdefault("bool", {}).setdefault("filter", []).append({
                    "range": {"publication_year": {"gte": from_year, "lte": to_year}}
                })
        return {"_source": {"exclude": ["chunk_vector"]}, "size": size, "query": query}

    def perform_search(self, search_body, index_name='pubmed', search_pipeline='nlp-search-pipeline'):
        try:
            response = self.client.search(body=search_body, index=index_name, params={'search_pipeline': search_pipeline})
            return response.get('hits', {}).get('hits', [])
        except Exception as e:
            raise RuntimeError(f"Search failed: {e}")


class BasicSearchStrategy(SearchStrategy):
    def search(self, query_parts, k, size):
        query_text = query_parts[0]
        search_body = self.create_search_body(query_text, k, size)
        return self.perform_search(search_body)


class TermSearchStrategy(SearchStrategy):
    def search(self, query_parts, k, size):
        query_text, term, value = query_parts
        search_body = self.create_search_body(query_text, k, size, term_filter=(term, value))
        return self.perform_search(search_body)


class YearRangeSearchStrategy(SearchStrategy):
    def search(self, query_parts, k, size):
        query_text, from_year, to_year = query_parts
        search_body = self.create_search_body(query_text, k, size, year_range=(from_year, to_year))
        return self.perform_search(search_body)


class TermYearRangeSearchStrategy(SearchStrategy):
    def search(self, query_parts, k, size):
        query_text, term, value, from_year, to_year = query_parts
        search_body = self.create_search_body(query_text, k, size, term_filter=(term, value), year_range=(from_year, to_year))
        return self.perform_search(search_body)


class SearchStrategyFactory:
    @staticmethod
    def get_strategy(query_parts, client, model_id):
        if len(query_parts) == 1:
            return BasicSearchStrategy(client, model_id)
        elif len(query_parts) == 3:
            return TermSearchStrategy(client, model_id)
        elif len(query_parts) == 4:
            return YearRangeSearchStrategy(client, model_id)
        elif len(query_parts) == 5:
            return TermYearRangeSearchStrategy(client, model_id)
        else:
            raise ValueError("Invalid query format")
