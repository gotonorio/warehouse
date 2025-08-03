from .big_category_views import (
    BigCategoryCreateView,
    BigCategoryDeleteView,
    BigCategoryIndexView,
    BigCategoryUpdateView,
    BigCategoryView,
)
from .category_views import (
    CategoryBigView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryIndexView,
    CategoryUpdateView,
)
from .file_views import (
    FileCategoryView,
    FileCreateView,
    FileDeleteView,
    FileIndexView,
    FileUpdateView,
    pdf_view,
)
from .search_views import SearchlistView

__all__ = [
    # File
    "FileIndexView",
    "FileCategoryView",
    "FileCreateView",
    "FileUpdateView",
    "FileDeleteView",
    "pdf_view",
    # Category
    "CategoryIndexView",
    "CategoryBigView",
    "CategoryCreateView",
    "CategoryUpdateView",
    "CategoryDeleteView",
    # BigCategory
    "BigCategoryIndexView",
    "BigCategoryCreateView",
    "BigCategoryUpdateView",
    "BigCategoryDeleteView",
    "BigCategoryView",
    # Search
    "SearchlistView",
]
