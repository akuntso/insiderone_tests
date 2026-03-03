"""This module contains test data for API tests."""

import dataclasses

@dataclasses.dataclass
class ApiTestData:

    BASE_PET_URL: str = 'https://petstore.swagger.io/v2/'
    NEW_PET = {
        "id": 555,
        "category": {},
        "name": "Bob",
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }

    UPDATE_PET = {
        "id": 555,
        "name": "Bob Marlin",
        "status": "pending"
    }
    HEADERS = {
        "api_key": "special-key",
        'Content-Type': 'aplication/json',
        'Accept': 'aplication/json'
    }
    HEADERS_WITH_INVALID_API_KEY = {
        "api_key": "invalid-key",
        'Content-Type': 'aplication/json',
        'Accept': 'aplication/json'
    }
    PET_WITHOUT_NAME_VALUE = {
        "id": 555,
        "category": {},
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WITHOUT_STATUS_VALUE = {
        "id": 555,
        "category": {},
        "name": "Bob",
        "photoUrls": [],
        "tags": [],
    }
    PET_WITHOUT_CATEGORY_VALUE = {
        "id": 555,
        "name": "Bob",
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WITH_INVALID_FORMAT_ID= {
        "id": "invalid-format-id", # invalid format str, expected int
        "name": "Tobias",
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WITH_NON_EXISTENT_ID = {
        "id": 666, # such id has not been existed yet
        "name": "Tobias",
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WTIH_ALREADY_EXISTENT_ID = {
        "id": 13508,
        "name": "Tobias",
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WTIH_INVALID_FORMAT_NAME = {
        "id": 13508,
        "name": 555, # invalid format int. expected str
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
    PET_WTIH_INVALID_FORMAT_TAG_NAME = {
        "id": 13508,
        "name": "Jon",
        "photoUrls": [],
        "tags": [
            {
                "id": 0,
                "name": 555 # invalid format int. expected str
            }
        ],
        "status": "available"
    }
    PET_WTIH_INVALID_FORMAT_TAG_NAME = {
        "id": 13508,
        "name": "Jon",
        "photoUrls": [
            555 # invalid format int. expected str
        ],
        "photoUrls": [],
        "tags": [],
        "status": "available"
    }
