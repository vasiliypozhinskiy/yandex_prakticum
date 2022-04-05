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
                "type": "text",
                "analyzer": "ru_en"
            },
            "films_ids": {
                "type": "keyword"
            }
        }
    }
