
PET_SCHEMA = {
  "type": "object",
  "required": ["name", "status"],
  "properties": {
    "id": {
      "type": "integer",
      "format": "int64",
      "example": 0
    },
    "category": {
      "type": "object",
      "properties": {
        "id": { "type": "integer" },
        "name": { "type": "string" }
      }
    },
    "name": {
      "type": "string",
      "example": "doggie"
    },
    "photoUrls": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "integer" },
          "name": { "type": "string" }
        }
      }
    },
    "status": {
      "type": "string",
      "description": "pet status in the store",
      "enum": ["available", "pending", "sold"]
    }
  }
}