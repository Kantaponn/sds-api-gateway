from fastapi import FastAPI, HTTPException, Query, Path
from typing import Annotated
import requests
import os


app = FastAPI()

chef_url = os.environ.get("chef_url")  # "http://localhost:50001"
recipe_url = os.environ.get("recipe_url")  # "http://localhost:50002"
review_url = os.environ.get("review_url")  # "http://localhost:50003"


@app.get(
    "/recipes",
    responses={
        400: {"description": "Bad Request"},
        503: {"description": "Service Unavailable"},
    },
)
def get_recipes(
    page_size: Annotated[int, Query(description="Number of maximum recipes per page")],
    current_page: Annotated[
        int, Query(description="Get the specific page of total pages")
    ],
    text: Annotated[str, Query(description="Exact text search in recipe")] = None,
):
    params = {"pageSize": page_size, "currentPage": current_page, "text": text}
    return request_get(f"{recipe_url}/recipes", params=params)


@app.get("/recipe/{recipe_id}")
def read_recipe_by_id(recipe_id: Annotated[int, Path(description="The recipe id")]):
    recipe = request_get(f"{recipe_url}/recipes/{recipe_id}", params={})["recipe"]

    reviews = request_get(f"{review_url}/reviews", params={"recipeId": recipe_id})[
        "reviews"
    ]
    recipe["reviews"] = [
        {k: v for k, v in d.items() if k != "recipeId"} for d in reviews
    ]

    chef_id = recipe["chefId"]
    recipe["chef"] = request_get(f"{chef_url}/chefs/{chef_id}", params={})["chef"]

    recipe.pop("chefId")
    return {"recipe": recipe}


@app.get("/chef/{chef_id}")
def read_chef(
    chef_id: Annotated[int, Path(description="The chef id")],
):
    return request_get(f"{chef_url}/chefs/{chef_id}", params={})


def request_get(url, params):
    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail=response.json())
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail=response.json())
        else:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Failed to fetch data from the external API",
                    "fetch_status_code": response.status_code,
                },
            )
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail={"error": str(e)})
