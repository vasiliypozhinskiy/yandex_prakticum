import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import films, genres, persons
from core import config
from db import db, elastic
from db import redis
from db.elastic.elastic_service import ElasticService

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        address=f'{config.REDIS_HOST}:{config.REDIS_PORT}',
        password=config.REDIS_PASSWORD,
        minsize=10, maxsize=20)

    elastic_settings = {
        'hosts': [f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}']
    }
    if config.ELASTIC_PASSWORD:
        elastic_settings.update({
            'http_auth': ('elastic', config.ELASTIC_PASSWORD)
        })

    db.db = ElasticService(AsyncElasticsearch(**elastic_settings))


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await db.db.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['film'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genre'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['person'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
