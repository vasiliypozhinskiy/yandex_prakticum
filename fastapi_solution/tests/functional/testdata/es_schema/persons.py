class Persons:
    mappings = {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "full_name": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "films_ids": {
                "type": "keyword"
            }
        }
    }
