"""PetAPIClient is a client for interacting with the pet API. It provides methods for creating,
retrieving, updating, and deleting pet
"""

import requests
import logging

from ..api_pet_test_data import ApiTestData


class PetAPIClient:
    """Initializes the test client for the Pet API.

    :param test_data: data provider for API constants and templates
    :param session: the requests session object for handling HTTP connections
    :param base_url: the base URL for pet-related API endpoints
    :param payload: the dictionary containing new pet data
    :param headers: the HTTP headers used for API requests
    :param logging: the logger instance for tracking test execution
    :param response: the last received HTTP response object
    :param response_json: the JSON-decoded body of the last response
    :param pet_id: the ID of the current pet being processed
    :param list_of_pet_ids: a list to store IDs of all created pets during the session

    """
    def __init__(self):
        self.test_data = ApiTestData()
        self.session = requests.Session()
        self.base_url: str = self.test_data.BASE_PET_URL
        self.payload: dict = self.test_data.NEW_PET.copy()
        self.headers: dict = self.test_data.HEADERS.copy()
        self.logging = logging.getLogger(__name__)
        self.response: requests.Response = None
        self.response_json: dict = None
        self.pet_id: str = None
        self.list_of_pet_ids: list = []

    def create_pet(self, headers: dict | None = None, payload: dict | None = None) -> None:
        """Creates a new pet

        :param pyload: optional dictionary to override the default payload for pet creation
        :param headers: optional dictionary headers with api key and format data, by defaut are
        used object headers

        """
        try:
            self.logging.info("Creating a new pet")
            self.response = self.session.post(
                url=f"{self.base_url}/pet",
                headers=headers or self.headers,
                json=payload or self.payload
            )
            self.response_json = self.response.json()
            self.pet_id = self.response_json.get("id")
            self.list_of_pet_ids.append(self.pet_id)
            if self.pet_id:
                self.logging.info(f"Pet created with ID: {self.pet_id}")
            self.logging.info(f"Response is: {self.response_json}")
        except requests.RequestException as e:
            self.logging.error(f"Error creating a pet: {e}")

    def upload_pet_image_by_id(self, pet_id: str, image_path: str, additional_metadata: str) -> requests.Response:
        """Creates a new pet by uploading an image

        :param pet_id: the ID of the pet to upload the image for
        :param image_path: the path to the image file to upload
        :param additional_metadata: additional metadata to include with the image upload

        :returns: the response object containing the details of the created pet

        """
        try:
            self.logging.info(f"Uploading an immage by id: {image_path}")
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                return self.session.post(f"{self.base_url}/pet/{pet_id}/uploadImage",
                    files=files,
                    headers=self.headers,
                    json={'additionalMetadata': additional_metadata}
                )
        except requests.RequestException as e:
            self.logging.error(f"Error updating a pet: {e}")

    def get_pet_by_id(self, pet_id: str) -> requests.Response:
        """Retrieves a pet by its ID

        :param pet_id: the ID of the pet to retreive

        :returns: the response object containing the pet details

        """
        try:
            self.logging.info(f"Retrieving pet by ID: {pet_id}")
            return self.session.get(f"{self.base_url}/pet/{pet_id}")
        except requests.RequestException as e:
            self.logging.error(f"Error getting a pet: {e}")

    def delete_pet_by_id(self, pet_id: str, headers: dict | None = None ) -> requests.Response:
        """Deletes a pet by its ID

        :param pet_id: the ID of the pet to delete
        :param headers: optional headers with api key, by defaul are used object headers

        :returns: the response object containing the status of the delete operation

        """
        try:
            self.logging.info(f"Deleting pet by ID: {pet_id}")
            return self.session.delete(f"{self.base_url}/pet/{pet_id}", headers=headers or self.headers)
        except requests.RequestException as e:
            self.logging.error(f"Error deleting a pet: {e}")

    def update_existing_pet(self, payload: dict) -> requests.Response:
        """Updates the a pet only by payload, id must be included into it

        :param payload: the json payload with id inside and other pet data

        :returns: the response object containing the updated pet datails

        """
        try:
            self.logging.info(f"Updating an existing pet by payload with id: {payload.get('id')}")
            return self.session.put(f"{self.base_url}/pet", headers=self.headers, json=payload)
        except requests.RequestException as e:
            self.logging.error(f"Error updating a pet by payloads: {e}")

    def update_pet_with_the_form_data_by_id(self, pet_id: str, name: str, status: str) -> requests.Response:
        """Updates the name and status of a pet using form data

        :param pet_id: the ID of the pet to update
        :param name: the new name for the pet
        :param status: the new status for the pet

        :returns: the response object containing the updated pet details

        """
        try:
            self.logging.info(f"Updating pet with form data by ID: {pet_id}")
            form_data = {}
            if name:
                form_data['name'] = name
            if status:
                form_data['status'] = status
            return self.session.post(f"{self.base_url}/pet/{pet_id}", headers=self.headers, json=form_data)
        except requests.RequestException as e:
            self.logging.error(f"Error updating a pet with form data by ID: {e}")

    def get_pet_by_status(self, status: str) -> requests.Response:
        """Retrieves pet filltered by status

        :param status: the status to filter pets by

        :returns: the response object containing the list of pets with the specified status

        """
        try:
            self.logging.info(f"Finding pets by status: {status}")
            return self.session.get(f"{self.base_url}/pet", params={"status": status})
        except requests.RequestException as e:
            self.logging.error(f"Error getting a pet by status: {e}")
