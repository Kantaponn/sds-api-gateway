from pydantic import BaseModel
from typing import List


class MessageError(BaseModel):
    error: str


class Recipe(BaseModel):
    id: str
    description: str
    name: str
    step: List[str]
    ingredients: str
    imageUrl: str
    chefId: int


class PaginationMetadata(BaseModel):
    totalPage: int
    currentPage: int
    totalRecipes: int


class RecipesData(BaseModel):
    recipes: List[Recipe]
    paginationMetadata: PaginationMetadata


class Review(BaseModel):
    id: str
    description: str
    reviewerName: str
    rating: float


class ChefInfo(BaseModel):
    id: str
    name: str
    description: str
    imageUrl: str
    phoneNumber: str
    email: str
    quote: str
    experience: str


class RecipeDetail(BaseModel):
    id: str
    description: str
    name: str
    step: List[str]
    ingredients: str
    imageUrl: str
    reviews: List[Review]
    chef: ChefInfo


class RecipeDetailData(BaseModel):
    recipe: RecipeDetail


class chefData(BaseModel):
    chef: ChefInfo
