from fastapi import APIRouter

from .endpoints import (
    AlbumController,
    ArtistController,
    BookController,
    ItemController,
    SongController,
)

router = APIRouter()

router.include_router(BookController.router, tags=["books"], prefix="/books")

router.include_router(ItemController.router, tags=["items"], prefix="/items")

router.include_router(SongController.router, tags=["songs"], prefix="/songs")
router.include_router(AlbumController.router, tags=["albums"], prefix="/albums")
router.include_router(ArtistController.router, tags=["artists"], prefix="/artists")
