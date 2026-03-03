import pytest
import requests

from assertpy import assert_that
from jsonschema import validate, ValidationError

from endpoints.pet_api_client import PetAPIClient
from api_tests.tests.pet_json_schema import PET_SCHEMA

# -------------------------
# Positive tests
# -------------------------
@pytest.mark.api
def test_create_pet_success(pet_api_client: PetAPIClient):
    """Test case verifies that a pet can be successfully created with valid data"""
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.created)
    assert_that(pet_api_client.response_json).contains_key(
        "id", "name", "status", "category", "photoUrls", "tags"
    )

@pytest.mark.api
def test_upload_pet_image_by_id(pet_api_client: PetAPIClient):
    """Test case verifies that an image can be uploaded for a pet by its ID"""
    resp = pet_api_client.upload_pet_image_by_id(
        pet_id=pet_api_client.pet_id,
        image_path='tests/resources/pet_image.jpg',
        additional_metadata='Test image upload'
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.ok)
    assert_that(resp.json()).contains_key("message")
    assert_that(resp.json()).contains_key("code")
    assert_that(resp.json()).contains_key("type")

@pytest.mark.api
def test_get_pet_by_id(pet_api_client: PetAPIClient):
    """Test case verifies that a pet can be retrieved by its ID after creation"""
    resp = pet_api_client.get_pet_by_id(pet_api_client.pet_id)
    assert_that(resp.status_code).is_equal_to(requests.codes.ok)
    assert_that(resp.json()).contains_key("id").is_equal_to(pet_api_client.pet_id)

@pytest.mark.api
def test_get_pet_by_status(pet_api_client: PetAPIClient):
    """Test case verifies that pet can be listed with a status 'available' by filter"""
    resps = pet_api_client.get_pet_by_status('available')
    assert_that(resps.status_code).is_equal_to(requests.codes.ok)
    assert all(assert_that(resp.get('status')).is_equal_to('available') for resp in resps.json())

@pytest.mark.api
def test_update_pet_by_payloads(pet_api_client: PetAPIClient):
    """Test case verifies that the pet name and status of a pet can be updated successfully"""
    resp = pet_api_client.update_existing_pet(pet_api_client.test_data.UPDATE_PET)
    assert_that(resp.status_code).is_equal_to(requests.codes.ok)
    assert_that(resp.json().get("name")).is_equal_to('Bob Marlin')
    assert_that(resp.json().get("status")).is_equal_to('pending')

@pytest.mark.api
def test_update_pet_with_form_data_by_id(pet_api_client: PetAPIClient):
    """Test case verifies that the name and status of a pet can be updated using form data"""
    resp = pet_api_client.update_pet_with_the_form_data_by_id(
        pet_id=pet_api_client.pet_id,
        name='Updated Pet Name',
        status='sold'
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.ok)
    assert_that(resp.json().get("name")).is_equal_to('Updated Pet Name')
    assert_that(resp.json().get("status")).is_equal_to('sold')

@pytest.mark.api
def test_delete_pet_by_id(pet_api_client: PetAPIClient):
    """Test case verifies that a pet can be deleted by its ID successfully"""
    resp = pet_api_client.delete_pet_by_id(pet_api_client.pet_id)
    assert_that(resp.status_code).is_equal_to(requests.codes.ok)
    # Verify that the pet is no longer retrievable
    get_resp = pet_api_client.get_pet_by_id(pet_api_client.pet_id)
    assert_that(get_resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_validate_pet_schema(pet_api_client: PetAPIClient):
    """Test case verifies that the response defines JSON schema correctly"""
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.created)
    try:
        validate(instance=pet_api_client.response_json, schema=PET_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"JSON Schema validation error: {e.message}")

@pytest.mark.api
def test_create_pet_missing_name_value(pet_api_client: PetAPIClient):
    """Test case verifies that creating a pet without the name value creates object
    and returns 200 status code

    """
    pet_api_client.create_pet(payload=pet_api_client.test_data.PET_WITHOUT_NAME_VALUE)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_create_pet_missing_status_value(pet_api_client: PetAPIClient):
    """Test case verifies that missing status value object is created and returns 200 status code"""
    pet_api_client.create_pet(payload=pet_api_client.test_data.PET_WITHOUT_STATUS_VALUE)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_create_pet_missing_category_value(pet_api_client: PetAPIClient):
    """Test case verifies that missing category value object is created and returns 200 status code"""
    pet_api_client.create_pet(payload=pet_api_client.test_data.PET_WITHOUT_CATEGORY_VALUE)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_update_pet_missing_status_value(pet_api_client: PetAPIClient):
    """Test case verifies that update missing status value, returns 200 status code"""
    pet_api_client.update_existing_pet(payload=pet_api_client.test_data.PET_WITHOUT_STATUS_VALUE)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_update_pet_missing_name_value(pet_api_client: PetAPIClient):
    """Test case verifies that update missing name value, returns 200 status code"""
    pet_api_client.update_existing_pet(payload=pet_api_client.test_data.PET_WITHOUT_NAME_VALUE)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_create_pet_with_empty_body(pet_api_client: PetAPIClient):
    """Test case verifies that with empty body object will be created,
    id is automaticaly created and rturns 200 status code

    """
    payload = {}
    pet_api_client.create_pet(payload=payload)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.ok)

# # -------------------------
# # Negative tests
# # -------------------------

@pytest.mark.api
def test_create_pet_with_invalid_method(pet_api_client: PetAPIClient):
    """Test case verifies that creating a pet with invalid HTTP method fails and returns 405 status code"""
    pet_api_client.logging.info("Creating a new pet with invalid HTTP method (PATCH instead of POST)")
    resp = pet_api_client.session.patch(f"{pet_api_client.base_url}/pet")
    assert_that(resp.status_code).is_equal_to(requests.codes.method_not_allowed)

@pytest.mark.api
def test_create_pet_by_invalid_format_name(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format id returns 405 status code"""
    pet_api_client.create_pet(payload=pet_api_client.test_data.PET_WTIH_INVALID_FORMAT_NAME)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.not_allowed)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_create_pet_by_invalid_tag_format_name(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format tag returns 405 status code"""
    pet_api_client.create_pet(payload=pet_api_client.test_data.PET_WTIH_INVALID_FORMAT_TAG_NAME)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.not_allowed)
    pet_api_client.delete_pet_by_id(pet_api_client.pet_id)

@pytest.mark.api
def test_update_pet_by_invalid_format_id(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format id (e.g str format) returns 400 status code"""
    resp = pet_api_client.update_existing_pet(pet_api_client.test_data.PET_WITH_INVALID_FORMAT_ID)
    assert_that(resp.status_code).is_equal_to(requests.codes.bad_request)

@pytest.mark.api
def test_update_pet_by_non_existent_id(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with non existent id returns 404 status code"""
    resp = pet_api_client.update_existing_pet(pet_api_client.test_data.PET_WITH_NON_EXISTENT_ID)
    assert_that(resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_update_pet_by_invalid_format_name(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with non existent id returns 405 status code"""
    resp = pet_api_client.update_existing_pet(pet_api_client.test_data.PET_WTIH_INVALID_FORMAT_NAME)
    assert_that(resp.status_code).is_equal_to(requests.codes.not_allowed)

@pytest.mark.api
def test_update_pet_by_invalid_tag_name(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format tag returns 405 status code"""
    resp = pet_api_client.update_existing_pet(pet_api_client.test_data.PET_WTIH_INVALID_FORMAT_TAG_NAME)
    assert_that(resp.status_code).is_equal_to(requests.codes.not_allowed)

@pytest.mark.api
def test_update_pet_with_empty_body(pet_api_client: PetAPIClient):
    """Test case verifies that update with empty body fails and rturns 405 status code"""
    payload = {}
    pet_api_client.update_existing_pet(payload=payload)
    assert_that(pet_api_client.response.status_code).is_equal_to(requests.codes.not_allowed)

@pytest.mark.api
def test_get_pet_with_invalid_format_status_value(pet_api_client: PetAPIClient):
    """Test case verifies that filtered pet with invvalid format status returns 400 status code"""
    resp = pet_api_client.get_pet_by_status("invalid-format-status")
    assert_that(resp.status_code).is_equal_to(requests.codes.bad_request)

@pytest.mark.api
def test_get_pet_with_non_existent_id(pet_api_client: PetAPIClient):
    """Test case verifies that filtered pet with non existent id returns 404"""
    resp = pet_api_client.get_pet_by_id(0) # assuming 0 id does not exist
    assert_that(resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_get_pet_with_invalid_format_id(pet_api_client: PetAPIClient):
    """Test case verifies that filtered pet with invalid format id returns 400"""
    resp = pet_api_client.get_pet_by_id("invalid-format-id") # used str, expected int
    assert_that(resp.status_code).is_equal_to(requests.codes.bad_request)

@pytest.mark.api
def test_delete_pet_with_non_existent_id(pet_api_client: PetAPIClient):
    """Test case verifies that deleting a pet with non existent id returns 404 status code"""
    resp = pet_api_client.delete_pet_by_id(0) # assuming 0 id does not exist
    assert_that(resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_delete_pet_with_invalid_format_id(pet_api_client: PetAPIClient):
    """Test case verifies that deleting a pet with invalid format returns 400 status code"""
    resp = pet_api_client.delete_pet_by_id("invalid-format-id") # used str, expected int
    assert_that(resp.status_code).is_equal_to(requests.codes.bad_request)

@pytest.mark.api
def test_delete_pet_with_invalid_api_key(pet_api_client: PetAPIClient):
    """Test case verifies that deleting a pet with invalid api key returns 404 status code"""
    resp = pet_api_client.delete_pet_by_id(
        pet_id=pet_api_client.pet_id,
        headers=pet_api_client.test_data.HEADERS_WITH_INVALID_API_KEY)
    assert_that(resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_update_pet_with_form_data_by_id_with_non_existent_id(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with non-existent id returns 404 status code"""
    resp = pet_api_client.update_pet_with_the_form_data_by_id(
        pet_id=0, # assuming 0 id does not exist
        name="Updated Pet Name",
        status="sold"
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.not_found)

@pytest.mark.api
def test_update_pet_with_form_data_by_id_with_invalid_format_id(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format id returns 405 status code"""
    resp = pet_api_client.update_pet_with_the_form_data_by_id(
        pet_id="invalid-format-id", # invalid format str. expected int
        name="Updated Pet Name",
        status="sold"
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.not_allowed)

@pytest.mark.api
def test_update_pet_with_form_data_by_id_with_invalid_name_value(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format name value returns 405 status code"""
    resp = pet_api_client.update_pet_with_the_form_data_by_id(
        pet_id=pet_api_client.pet_id,
        name=555, # invalid format int. expected str
        status="sold"
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.not_allowed)

@pytest.mark.api
def test_update_pet_with_form_data_by_id_with_invalid_status_value(pet_api_client: PetAPIClient):
    """Test case verifies that updating a pet with invalid format status value returns 405 status code"""
    resp = pet_api_client.update_pet_with_the_form_data_by_id(
        pet_id=pet_api_client.pet_id,
        name="Noni",
        status=555 # invalid format int. expected str
    )
    assert_that(resp.status_code).is_equal_to(requests.codes.not_allowed)
