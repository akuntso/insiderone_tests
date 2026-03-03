import sys
import os
import logging

import pytest

from endpoints.pet_api_client import PetAPIClient


logging = logging.getLogger(__name__)
sys.path.append(os.path.abspath("."))


@pytest.fixture(scope="session", autouse=True)
def claims_api_client():
    """Fixture to provide a ClaimsAPIClient instance for tests"""
    logging.info("Initializing the Pet client object")
    client = PetAPIClient()
    client.create_pet()
    yield client
    # cleanup
    if client.list_of_pet_ids:
        for id in client.list_of_pet_ids:
            client.delete_pet_by_id(id)
