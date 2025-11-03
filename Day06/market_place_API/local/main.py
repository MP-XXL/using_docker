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

sort_by: name, pri{{baseUrl}}/:market_location/producece_per_kg, quantity_kg
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

class UpdateProduce(BaseModel):
    name: str | None = None
    quantity_kg: float | None = None
    price_per_kg: float | None = None
    category: ProduceCategory | None = None

class ProduceCreate(Produce):
    produce_id: int
    is_available: bool

"""class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"""

class Order(BaseModel):
    produce_name: str
    buyer_name: str
    buyer_phone: str
    quantity: float
    delivery_area: str


class OrderInDb(Order):
    order_id: int
    produce_id: int
    total_price: float
    order_date: datetime
    status: str

class Database:
    def __init__(self):
        self._vendors: Dict[int, VendorCreate] = {}
        self._produce: Dict[int, List[ProduceCreate]] = {}
        self._orders: List[OrderInDb] = []
        self.vendor_id = 1
        self.produce_id = 1
        self.order_id = 1

    def increment_vendor_id(self):
        self.vendor_id += 1

    def increment_produce_id(self):
        self.produce_id += 1

    def increment_order_id(self):
        self.order_id += 1

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
            self._vendors[vendor_id].name = vendor.name
        if vendor.market_location != None:
            self._vendors[vendor_id].market_location = vendor.market_location
        if vendor.phone != None:
            self._vendors[vendor_id].phone = vendor.phone

        data = self._vendors[vendor_id]
        return {
                "success": True,
                "data": data,
                "message": "Vendor details updated successfully"
                }

    def vendor_delete(self, vendor_id: int):
        del self._vendors[vendor_id]
        del self._produce[vendor_id]
        raise HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail = "Vendor deleted successfully"
                )

    def get_produce_by_category(self, category: str):
        categorized_produce = []
        for produce, produce_details in self._produce.items():
            for detail in produce_details:
                if detail.category == category:
                    categorized_produce.append({produce:detail})
        return {
            "success": True,
            "data": categorized_produce,
            "message": "Displaying produce by perfered category"
            }

    def get_produce_by_vendor_id(self, vendor_id: int):
        produce_by_vendor = []
        for produce, produce_details in self._produce.items():
                if produce == vendor_id:
                    produce_by_vendor.append({vendor_id: produce_details})
                else:
                    raise VENDOR_ID_NOT_FOUND()
        return {
            "success": True,
            "data": produce_by_vendor,
            "message": "Displaying produce by perfered vendor"
            }


    def get_produce_by_location(self, market_location: str):
        vendors_by_location = []
        produce_by_location = []
        for vendor, vendor_details in self._vendors.items():
            if vendor_details.market_location == market_location:
                vendors_by_location.append(vendor)

        for vendor in vendors_by_location:
            for produce, produce_details in self._produce.items():
                if vendor == produce:
                    produce_by_location.append({produce: produce_details})
        return {
            "success": True,
            "data": produce_by_location,
            "message": "Displaying produce by perfered location"
            }


    def max_price_produce(self, max_price: int):
        price_cap = []
        for produce, produce_details in self._produce.items():
            for detail in produce_details:
                if detail.price_per_kg <= max_price:
                    price_cap.append({produce: detail})

        return {
                "succes": True,
                "data": price_cap,
                "message": "Displaying produce below specfied price"
                }

    def available_produce(self):
        available = []
        for produce, produce_details in self._produce.items():
            for detail in produce_details:
                if detail.is_available == True:
                    available.append({produce:detail})
        return {
            "success": True,
            "data": available,
            "message": "Displaying available produce"
            }

    def search_produce(self, produce_name: str):
        produce_list = []
        for produce, produce_details in self._produce.items():
            for item in produce_details:
                if item.name == produce_name:
                    produce_list.append({produce:item})
        if len(produce_list) == 0:
            raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Market produce not found"
                        )

        return {
            "success": True,
            "data": produce_list,
            "message": "Displaying search result for produce name"
            }

    def produce_detail(self, produce_id: int):
        produce_found = []
        for produce, produce_details in self._produce.items():
            for detail in produce_details:
                if detail.produce_id == produce_id:
                    produce_found.append({produce: detail})
                
        if len(produce_found) == 0:
            raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Produce ID not found"
                    )
        return {
                "success": True,
                "data": produce_found,
                "message": "Displaying produce details"
                }

    def produce_update(self, produce_id: int, item: int, position: int, produce: UpdateProduce):
        if produce.name != None:
            self._produce[item][position].name = produce.name
        if produce.quantity_kg != None:
            self._produce[item][position].quantity_kg = produce.quantity_kg
        if produce.price_per_kg != None:
            self._produce[item][position].price_per_kg = produce.price_per_kg
        if produce.category != None:
            self._produce[item][position].category = produce.category

        return {
                "success": True,
                "data": self._produce[item][position],
                "message": "Produce updated successfully"
                }

    def produce_delete(self, produce_id: int, item, position: int):
        del self._produce[item][position]
        raise HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail = "Delete successfull"
                )






    def store_order(self, order: OrderInDb):
        self._orders.append(order)


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

@app.get("/produce/{category}")
def produce_by_category(category: str):
    return db_instance.get_produce_by_category(category)

@app.get("/vendor/{vendor_id}/produce")
def produce_by_vendor_id(vendor_id: int):
    return db_instance.get_produce_by_vendor_id(vendor_id)

@app.get("/markets/produce/{market_location}")
def produce_by_market_location(market_location: str):
    return db_instance.get_produce_by_location(market_location)

@app.get("/prices/produce/{max_price}")
def set_max_price(max_price: int):
    return db_instance.max_price_produce(max_price)

@app.get("/available/produce")
def produce_availability():
    return db_instance.available_produce()

@app.get("/searchs/produce/{produce_name}")
def produce_search(produce_name: str):
    return db_instance.search_produce(produce_name)

@app.get("/details/produce/{produce_id}")
def get_produce_details(produce_id: int):
    return db_instance.produce_detail(produce_id)

@app.put("/produce/{produce_id}")
def update_produce(produce_id: int, produce: UpdateProduce):
    for item, produce_details in db_instance._produce.items():
        for detail in produce_details:
            if detail.produce_id == produce_id:
                position = produce_details.index(detail)
                return db_instance.produce_update(produce_id, item, position, produce)
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Produce ID not found"
                )

@app.patch("/produce/{produce_id}")
def update_produce_quantity(produce_id: int):
    pass

@app.delete("/produce/{produce_id}")
def delete_produce(produce_id: int):
    for item, produce_details in db_instance._produce.items():
        for detail in produce_details:
            if detail.produce_id == produce_id:
                position = produce_details.index(detail)
                return db_instance.produce_delete(produce_id, item, position)
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Produce ID not found"
                )



@app.post("/orders")
def order_placement(order: Order):
    produce_list = []

    for produce, produce_details in db_instance._produce.items():
        for item in produce_details:
            if item.name == order.produce_name:
                produce_list.append({produce:item})

    if len(produce_list) == 0:
        raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Market produce not found"
                        )

    """for _, produce in produce_list.items():
        if produce.quantity_kg < order.quantity:
                raise HTTPException(
                        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail = "Quantity ordered is above stock level"
                        )"""
    for produce in produce_list:
        for key, value in produce.items():
            if value.name == order.produce_name:
                new_order = OrderInDb(
                **order.model_dump(),
                order_id = db_instance.order_id,
                produce_id = value.produce_id,
                total_price = value.quantity_kg * order.quantity,
                order_date = datetime.now(),
                status = "pending"
                )

    db_instance.increment_order_id()
    db_instance.store_order(new_order)

    return {
            "success": True,
            "data": new_order,
            "message": "Order placed successfully"
            }
