import strawberry
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI
import uvicorn

from Graphqls.query import Query
from Graphqls.mutation import Mutation

from config import db


def init_app():
    apps = FastAPI(
        debug=True,
        title="David Code Fast API QL",
        description="FastAPI with Strawberry GraphQL demo",
        version="1.0.0",
    )

    @apps.on_event("startup")
    async def startup():
        await db.create_all()

    @apps.on_event("shutdown")
    async def shutdown():
        await db.close()

    @apps.get("/")
    def home():
        return "Welcome to the app!"

    # add graphQL endpoint
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    apps.include_router(graphql_app, prefix="/graphql")

    return apps


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
