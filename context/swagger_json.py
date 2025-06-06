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
    "external_id": "string",
    "rating": 0,
    "favorites": [0],
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

work_schedule_retrieve = {
    "application/json": {
        "type": "object",
        "properties": {
            "shop": {"type": "integer"},
            "work_schedule": {
                "type": "object",
                "properties": {
                    "Monday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Tuesday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Wednesday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Thursday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Friday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Saturday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                    "Sunday": {
                        "type": "object",
                        "properties": {
                            "begin": {"type": "string"},
                            "end": {"type": "string"},
                        },
                    },
                },
            },
        },
        "required": ["shop", "work_schedule"],
    }
}

human_images = {
    "id": 0,
    "images": [{"id": 0, "image": "string", "name": "string"}],
    "created_at": "date time",
    "updated_at": "date time",
    "description": "string",
    "name": "string",
    "price": 0,
    "product_human_images": [
        {
            "product": {"id": 0, "name": "string", "brands_id": 0},
            "product_color": 0,
            "product_image": {"path": "string", "id": 0, "name": "string"},
        }
    ],
}
