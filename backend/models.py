# models.py
from sqlmodel import SQLModel, Field, Relationship, Column, Table, ForeignKey, JSON
# from sqlalchemy import JSON
from datetime import datetime


# Association table for many-to-many relationship between Page and Tile
# page_tile_link = Table(
#     "page_tile_link",
#     SQLModel.metadata,
#     Column("page_id", ForeignKey("page.id"), primary_key=True),
#     Column("tile_id", ForeignKey("tile.id"), primary_key=True)
#
class PageTileLink(SQLModel, table=True):
    page_id: int = Field(
        default=None, foreign_key="tile.id", primary_key=True
    )
    tile_id: int = Field(
        default=None, foreign_key="page.id", primary_key=True
    )

# Base class for common properties of tiles
class Tile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Primary key column, optional for creating new records
    name: str
    color: str
    click_action: str
    long_click_action: str
    pages: list['Page'] = Relationship(back_populates="tiles", link_model=PageTileLink)  # Many-to-many relationship to Page

# SQLModel for Page, which contains a list of Tile
class Page(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Primary key column, optional for creating new records
    name: str
    tiles: list['Tile'] = Relationship(back_populates="pages", link_model=PageTileLink)  # Many-to-many relationship to Tile

# Base class for common properties of tiles
class TileBase(SQLModel):
    id: int = Field(default=None, primary_key=True)  # Primary key column, optional for creating new records
    name: str = Field(..., nullable=False)  # String column, not nullable
    color: str = Field(..., nullable=True)  #
    click_action: str = Field(..., nullable=False)  # Click action
    long_click_action: str = Field(..., nullable=False)  # Long click action
    tile_type: int
    tile_specifics: dict = Field(default_factory=dict, sa_column=Column(JSON))
    pages: list['Page'] = Relationship(back_populates="tiles", link_model=PageTileLink)  # Many-to-many relationship to Page

class TileSpecifics(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Primary key column, optional for creating new records
    name: str
    specifics: dict = Field(default_factory=dict, sa_column=Column(JSON))

TileSpecificsTemplate = {
    "TimerTile": {
        "running": False,
        "duration": 0
    },
    "LoggerTile": {
        "log_options": [],
        "log_item_template": {"time": "2000-01-01 00:00:00.000000", "log": ""},
        "log_items": []
    },
    "ChecklistTile": {
        "checklist_item_template" : {"done": False, "item": ""},
        "checklist_items": []
    }
}

# # SQLModel for Page, which contains a list of Tile
# class Page(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)  # Primary key column, optional for creating new records
#     name: str = Field(..., nullable=False)  # String column, not nullable
#     tiles: List['TileBase'] = Relationship(back_populates="pages", link_model=page_tile_link)  # Many-to-many relationship to Tile

# # TimerTile prototype
# class TimerTile(TileBase, table=True):
#     running: bool = Field(default=False)  # Indicates if the timer is running
#     duration: int = Field(..., nullable=False)  # Duration of the timer)

# # LoggerTile prototype
# class LoggerTile(TileBase, table=True):
#     log_items: List['LogItem'] = []  # List of log items, default empty list

# # ChecklistTile prototype
# class ChecklistTile(TileBase, table=True):
#     checklist_items: List['ChecklistItem'] = []  # List of checklist items, default empty list

# Usage Example:
# - You can use Tile, Page, TimerTile, LoggerTile, and ChecklistTile both as data validation models (like Pydantic)
# - And as ORM models to create, query, and update the database (like SQLAlchemy)
