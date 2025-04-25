product_list_retrieve = {
    "id": 0,
    "brands": {"id": 0, "name": "string"},
    "category": {"id": 0, "name": "string"},
    "shop": {"id": 0, "name": "string"},
    "color": [{"id": 0, "name": "string", "hex_color": "string"}],
    "sizes": {
        "male": [
            {
                "id": 0,
                "name": "string",
            }
        ],
        "female": [
            {
                "id": 0,
                "name": "string",
            }
        ],
    },
    "images": [
        {
            "id": 0,
            "color": {"id": 0, "name": "string", "hex_color": "string"},
            "path": "string",
        }
    ],
    "created_at": "2025-04-08T17:14:30.295Z",
    "name": "string",
    "price": 2147483647,
    "description": "string",
    "quantity": 2147483647,
}

crud_address = {
    "application/json": {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "coordinate": {
                "type": "object",
                "properties": {
                    "sting_key1": {},
                    "sting_key2": {},
                },
                "required": ["sting_key1", "sting_key2"],
            },
        },
        "required": ["address"],
    }
}
