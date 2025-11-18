import enum

class Gender(enum.Enum):
    M = "M"
    F = "F"

class Category(enum.Enum):
    farmer = "farmer"
    buyer = "buyer"

class ProductCategory(enum.Enum):
    GRAINS = "grains"
    TUBERS = "tubers"
    CEREALS = "cereals"
    FRUITS = "fruits"
    LIVESTOCK = "livestock"
    VEGETABLE = "vegetables"
    OILS = "oils"
    LATEX = "latex"