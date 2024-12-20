from opensearchpy import OpenSearch
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

class OpenSearchManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenSearchManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = None
            cls._instance.model_id = os.getenv("model_id", "Pt5esY0BQ48z97Fdmasb")
        return cls._instance

    def __init__(self):
        if not self.client:
            self.client = self.connect_to_opensearch()

    @staticmethod
    def connect_to_opensearch():
        try:
            client = OpenSearch(
                hosts=[{"host": os.getenv("DB_HOSTNAME"), "port": int(os.getenv("DB_PORT"))}],
                http_auth=(os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD")),
                use_ssl=False,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            logger.info("OpenSearch connection successful")
            return client
        except Exception as e:
            logger.error(f"OpenSearch connection failed: {e}")
            return None

    def create_or_update_pipeline(self, weight: float = 0.3):
        pipeline_body = {
            "description": "Post processor for hybrid search",
            "phase_results_processors": [
                {
                    "normalization-processor": {
                        "normalization": {"technique": "min_max"},
                        "combination": {
                            "technique": "arithmetic_mean",
                            "parameters": {"weights": [weight, 1 - weight]}
                        }
                    }
                }
            ]
        }
        try:
            self.client.transport.perform_request(
                'PUT',
                '/_search/pipeline/nlp-search-pipeline',
                body=pipeline_body
            )
            logger.info("Search pipeline created/updated successfully")
        except Exception as e:
            logger.warning(f"Failed to create/update search pipeline: {e}")
