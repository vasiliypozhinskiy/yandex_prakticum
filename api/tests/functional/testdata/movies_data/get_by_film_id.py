from typing import List

films_data: List[dict] = [
    {
        "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
        "imdb_rating": float(2.5),
        "genre": ["Action", "Adventure", "Fantasy", "Sci-Fi"],
        "title": "Star Wars: Episode IV - A New Hope",
        "description": "The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the Galaxy.",
        "director": {
            "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
            "name": "George Lucas",
        },
        "actors_names": [
            "Peter Cushing",
            "Carrie Fisher",
            "Harrison Ford",
            "Mark Hamill",
        ],
        "writers_names": ["George Lucas"],
        "actors": [
            {"id": "e039eedf-4daf-452a-bf92-a0085c68e156", "name": "Peter Cushing"},
            {"id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358", "name": "Carrie Fisher"},
            {"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Harrison Ford"},
            {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Mark Hamill"},
        ],
        "writers": [
            {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"}
        ],
    },
    {
        "id": "516f91da-bd70-4351-ba6d-25e16b7713b7",
        "imdb_rating": float(7.5),
        "genre": ["Action", "Adventure", "Fantasy", "Sci-Fi"],
        "title": "Star Wars: Episode III - Revenge of the Sith",
        "description": "Near the end of the Clone Wars, Darth Sidious has revealed himself and is ready to execute the last part of his plan to rule the galaxy. Sidious is ready for his new apprentice, Darth Vader, to step into action and kill the remaining Jedi. Vader, however, struggles to choose the dark side and save his wife or remain loyal to the Jedi order.",
        "director": {
            "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
            "name": "George Lucas",
        },
        "actors_names": [
            "Natalie Portman",
            "Ewan McGregor",
            "Ian McDiarmid",
            "Hayden Christensen",
        ],
        "writers_names": ["George Lucas"],
        "actors": [
            {"id": "c777f646-dae0-466f-867a-bc535a0b021b", "name": "Natalie Portman"},
            {"id": "69b02c62-a329-414d-83c6-ca54be34de24", "name": "Ewan McGregor"},
            {"id": "7214e401-bb43-4da2-9e7a-cd6ca31ee8ca", "name": "Ian McDiarmid"},
            {
                "id": "62df10e8-244d-4c31-b396-564dfbc2f9c5",
                "name": "Hayden Christensen",
            },
        ],
        "writers": [
            {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"}
        ],
    },
    {
        "id": "57beb3fd-b1c9-4f8a-9c06-2da13f95251c",
        "imdb_rating": float(6.9),
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "title": "Solo: A Star Wars Story",
        "description": "During an adventure into the criminal underworld, Han Solo meets his future co-pilot Chewbacca and encounters Lando Calrissian years before joining the Rebellion.",
        "director": {
            "id": "33eb3b88-69f2-4f38-a26d-ff32f1feb1a1",
            "name": "Ron Howard",
        },
        "actors_names": [
            "Emilia Clarke",
            "Woody Harrelson",
            "Joonas Suotamo",
            "Alden Ehrenreich",
        ],
        "writers_names": ["George Lucas", "Jonathan Kasdan", "Lawrence Kasdan"],
        "actors": [
            {"id": "7a852205-2bf6-4b75-b3b2-8a46ed6e91ef", "name": "Emilia Clarke"},
            {"id": "01377f6d-9767-48ce-9e37-3c81f8a3c739", "name": "Woody Harrelson"},
            {"id": "c69da9bd-eb87-4a06-be70-95d4ee2da1cc", "name": "Joonas Suotamo"},
            {"id": "ce06e6d7-600b-4829-badf-5d02c61f1a92", "name": "Alden Ehrenreich"},
        ],
        "writers": [
            {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"},
            {"id": "a2c091a2-281e-4732-9357-79b213d8d92f", "name": "Jonathan Kasdan"},
            {"id": "3217bc91-bcfc-44eb-a609-82d228115c50", "name": "Lawrence Kasdan"},
        ],
    },
]

expected_film_data = {
    "id": "516f91da-bd70-4351-ba6d-25e16b7713b7",
    "imdb_rating": float(7.5),
    "genre": ["Action", "Adventure", "Fantasy", "Sci-Fi"],
    "title": "Star Wars: Episode III - Revenge of the Sith",
    "description": "Near the end of the Clone Wars, Darth Sidious has revealed himself and is ready to execute the last part of his plan to rule the galaxy. Sidious is ready for his new apprentice, Darth Vader, to step into action and kill the remaining Jedi. Vader, however, struggles to choose the dark side and save his wife or remain loyal to the Jedi order.",
    "director": {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"},
    "actors_names": [
        "Natalie Portman",
        "Ewan McGregor",
        "Ian McDiarmid",
        "Hayden Christensen",
    ],
    "writers_names": ["George Lucas"],
    "actors": [
        {"id": "c777f646-dae0-466f-867a-bc535a0b021b", "name": "Natalie Portman"},
        {"id": "69b02c62-a329-414d-83c6-ca54be34de24", "name": "Ewan McGregor"},
        {"id": "7214e401-bb43-4da2-9e7a-cd6ca31ee8ca", "name": "Ian McDiarmid"},
        {"id": "62df10e8-244d-4c31-b396-564dfbc2f9c5", "name": "Hayden Christensen"},
    ],
    "writers": [{"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas"}],
}

expect_not_found_film_data: dict = {
    "id": "ea434935-cb62-4012-9138-be74435890cd",
    "imdb_rating": float(8.0),
    "genre": [
        "Action",
        "Adventure",
        "Fantasy",
        "Sci-Fi",
        "Drama",
        "Thriller",
        "Comedy",
        "Animation",
        "Family",
    ],
    "title": "Star vs. the Forces of Evil",
    "description": "An interdimensional princess, from the kingdom of Mewni, named Star Butterfly is sent to a new dimension, the Earth dimension, to learn how to use her newest possession, the royal family wand, and she finds help along the way meeting an Earth boy named Marco Diaz, and she lives with Marco and his parents causing all kinds of interdimensional mischief.",
    "director": None,
    "actors_names": ["Daron Nefcy", "Adam McArthur", "Grey Griffin", "Eden Sher"],
    "writers_names": ["Jordana Arkin", "David Wasson", "Daron Nefcy"],
    "actors": [
        {"id": "91315ca2-e928-4bc3-aa20-4a9024fed936", "name": "Daron Nefcy"},
        {"id": "6eada848-9bb2-4309-8250-90e20b82f0df", "name": "Adam McArthur"},
        {"id": "b4e1b2bd-7f36-4322-8a96-0baecf121424", "name": "Grey Griffin"},
        {"id": "fee27fee-19ea-4100-af1f-a2fd1ed85f0b", "name": "Eden Sher"},
    ],
    "writers": [
        {"id": "57d6e028-3d65-4879-bb4e-d2c086c74898", "name": "Jordana Arkin"},
        {"id": "13f1f970-08d3-442a-9b2c-dc3e54f47dde", "name": "David Wasson"},
        {"id": "91315ca2-e928-4bc3-aa20-4a9024fed936", "name": "Daron Nefcy"},
    ],
}
