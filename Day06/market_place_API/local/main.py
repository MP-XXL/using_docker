"""Task: Build a Jos Market Produce API
Project Overview
Create a simple API for managing a produce market in Jos, Nigeria. Vendors can list their farm produce, and buyers can browse and place orders.
Data Models (Pydantic)
1. Vendor

id: int
name: str (e.g., "Malam Audu", "Mama Grace")
market_location: str (Terminus, Katako, Bukuru, Farin Gada, Building Materials)
phone: str
created_at: datetime

2. Produce

id: int
vendor_id: int
name: str (e.g., "Irish Potato", "Tomatoes", "Carrots", "Cabbage")
quantity_kg: float (in kilograms)
price_per_kg: float (in Naira)
category: str (Vegetables, Fruits, Grains, Tubers)
is_available: bool

3. Order

id: int
produce_id: int
buyer_name: str
buyer_phone: str
produce_name: str
quantity_kg: float
total_price: float
delivery_area: str (Rayfield, Bukuru, Terminus, Jos South, etc.)
status: str (pending, confirmed, delivered)
order_date: datetime


Required Endpoints
Vendors

POST /vendors - Register new vendor
GET /vendors - Get all vendors
GET /vendors/{id} - Get vendor with their produce
PUT /vendors/{id} - Update vendor info
DELETE /vendors/{id} - Remove vendor

Produce

POST /produce - Add new produce item
GET /produce - Get all produce with filtering and sorting
GET /produce/{id} - Get specific produce details
PUT /produce/{id} - Update produce item
PATCH /produce/{id}/stock - Update quantity available
DELETE /produce/{id} - Remove produce

Orders

POST /orders - Place new order
GET /orders - Get all orders with filtering
GET /orders/{id} - Get order details
PATCH /orders/{id}/status - Update order status
DELETE /orders/{id} - Cancel order


Filtering & Sorting Requirements
GET /produce should support:
Filtering:

category: Filter by category (Vegetables, Fruits, Grains, Tubers)
vendor_id: Filter by vendor
market_location: Filter by market location
max_price: Show produce with price_per_kg <= value
available_only: Show only available items (true/false)
search: Search in produce name

Sorting:

sort_by: name, price_per_kg, quantity_kg
order: asc or desc (default: asc)"""

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
from enum import Enum

app = FastAPI(title="Market Place API")

class VENDOR_ID_NOT_FOUND(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found"):
        super().__init__(status_code, detail)
        pass

class MarketLocation(str, Enum):
    TERMINUS = "terminus"
    KATAKO = "katako"
    BUKURU = "bukuru"
    FARIN_GADA = "garin gada"
    BUILDING_MATERIALS = "building materials"

class ProduceCategory(str, Enum):
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    GRAINS = "grains"
    TUBERS = "tubers"

class Vendor(BaseModel):
    name: str
    market_location: MarketLocation
    phone: str

class UpdateVendor(BaseModel):
    name: str | None = None
    market_location: MarketLocation | None = None
    phone: str | None = None


class VendorCreate(Vendor):
    vendor_id: int
    created_at: datetime

class Produce(BaseModel):
    name: str 
    quantity_kg: float 
    price_per_kg: float 
    category: ProduceCategory
    #is_available: bool


class ProduceCreate(Produce):
    produce_id: int
    is_available: bool


class Database:
    def __init__(self):
        self._vendors: Dict[int, VendorCreate] = {}
        self._produce: Dict[int, List[ProduceCreate]] = {}
        self.vendor_id = 1
        self.produce_id = 1

    def increment_vendor_id(self):
        self.vendor_id += 1

    def increment_produce_id(self):
        self.produce_id += 1

    def add_vendor(self, vendor: VendorCreate):
        if vendor.vendor_id in self._vendors:
            raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "User already exists"
                    )
        self._vendors.update({vendor.vendor_id: vendor})
        self._produce.update({vendor.vendor_id: []})

    def get_all_vendors(self):
        return {
                "success": True,
                "data": self._vendors,
                "message": "Displaying all vendors"
                }

    def get_vendor_by_id(self, vendor_id: int):
        for vendor, produce in self._produce.items():
            if vendor == vendor_id:
                data = {vendor_id: produce}
                return {
                    "success": True,
                    "data": data,
                    "message": "Displaying vendor with ID and produce"
                    }

    def create_produce(self, vendor_id: int, produce: ProduceCreate):
        self._produce.setdefault(vendor_id, []).append(produce)

    def vendor_update(self, vendor_id: int, vendor: UpdateVendor):
        if vendor.name != None:
            db_instance._vendors[vendor_id].name = vendor.name
        if vendor.market_location != None:
            db_instance._vendors[vendor_id].market_location = vendor.market_location
        if vendor.phone != None:
            db_instance._vendors[vendor_id].phone = vendor.phone

        data = self._vendors[vendor_id]
        return {
                "success": True,
                "data": data,
                "message": "Vendor details updated successfully"
                }

    def vendor_delete(self, vendor_id: int):
        del self._vendors[vendor_id]
        raise HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail = "Vendor deleted successfully"
                )


db_instance = Database()


@app.get("/home")
def homepage():
    return {
            "success": True,
            "message": "Welcome to Market Place homepage"
            }

@app.post("/vendors")
def regsiter_vendor(vendor: Vendor):
    if not vendor.name or not vendor.market_location or not vendor.phone:
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "All fields are required"
                )
    new_vendor = VendorCreate(
            **vendor.model_dump(),
            vendor_id = db_instance.vendor_id,
            created_at = datetime.now()
            )
    db_instance.add_vendor(new_vendor)
    db_instance.increment_vendor_id()

    return {
            "success": "True",
            "data": new_vendor,
            "message": "Vendor rgistered successfully!"
            }

@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: int):
    if vendor_id not in db_instance._vendors:
        raise VENDOR_ID_NOT_FOUND

    return db_instance.get_vendor_by_id(vendor_id)

@app.get("/vendors")
def all_vendors():
    return db_instance.get_all_vendors()

@app.post("/produce")
def add_produce(vendor_id: int, produce: Produce):
    if vendor_id not in db_instance._vendors:
        raise VENDOR_ID_NOT_FOUND

    new_produce = ProduceCreate(
            **produce.model_dump(),
            produce_id = db_instance.produce_id,
            is_available = True
            )

    db_instance.create_produce(vendor_id, new_produce)
    db_instance.increment_produce_id()

    return {
            "success": True,
            "data": new_produce,
            "message": "Produce added successfully"
            }

@app.put("/vendors")
def update_vendor(vendor_id: int, vendor: UpdateVendor):
    if vendor_id not in db_instance._vendors:
        raise VENDOR_ID_NOT_FOUND

    return db_instance.vendor_update(vendor_id, vendor)

@app.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int):
    if vendor_id not in db_instance._vendors:
        raise VENDOR_ID_NOT_FOUND
    return db_instance.vendor_delete(vendor_id)
