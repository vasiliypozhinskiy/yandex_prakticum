class Genres:
    mappings = {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "name": {
                "type": "keyword"
            },
            "description": {
                "type": "keyword",
            },
            "films_ids": {
                "type": "keyword"
            }
        }
    }
