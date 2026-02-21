"""
Hotel Reservation System
"""

import json
import os
import unittest

DATA_DIR = "data"
HOTELS_FILE = os.path.join(DATA_DIR, "hotels.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")


def ensure_data_dir():
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(path):
    """Load JSON safely, handling invalid data."""
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"[ERROR] Could not read {path}: {error}")
        return {}


def save_json(path, data):
    """Save JSON safely."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        print(f"[ERROR] Could not write {path}: {error}")


class Hotel:
    """Hotel entity."""

    def __init__(self, hotel_id, name, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.rooms = rooms
        self.reserved_rooms = []

    def to_dict(self):
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "rooms": self.rooms,
            "reserved_rooms": self.reserved_rooms,
        }

    @staticmethod
    def from_dict(data):
        hotel = Hotel(data["hotel_id"], data["name"], data["rooms"])
        hotel.reserved_rooms = data.get("reserved_rooms", [])
        return hotel


class Customer:
    """Customer entity."""

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data):
        return Customer(data["customer_id"], data["name"], data["email"])


class Reservation:
    """Reservation entity."""

    def __init__(self, reservation_id,
                 customer_id,
                 hotel_id,
                 room_number):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.room_number = room_number

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_number": self.room_number,
        }

    @staticmethod
    def from_dict(data):
        return Reservation(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
            data["room_number"],
        )


class Storage:
    """Persistence layer."""

    def __init__(self):
        ensure_data_dir()
        self.hotels = self._load_hotels()
        self.customers = self._load_customers()
        self.reservations = self._load_reservations()

    def _load_hotels(self):
        raw = load_json(HOTELS_FILE)
        return {k: Hotel.from_dict(v) for k, v in raw.items()}

    def _load_customers(self):
        raw = load_json(CUSTOMERS_FILE)
        return {k: Customer.from_dict(v) for k, v in raw.items()}

    def _load_reservations(self):
        raw = load_json(RESERVATIONS_FILE)
        return {k: Reservation.from_dict(v) for k, v in raw.items()}

    def save_all(self):
        save_json(HOTELS_FILE,
                  {k: v.to_dict() for k, v in self.hotels.items()})
        save_json(CUSTOMERS_FILE,
                  {k: v.to_dict() for k, v in self.customers.items()})
        save_json(RESERVATIONS_FILE,
                  {k: v.to_dict() for k, v in self.reservations.items()})
        

class HotelService:
    """Hotel management operations."""

    def __init__(self, storage):
        self.storage = storage

    def create_hotel(self, hotel):
        self.storage.hotels[hotel.hotel_id] = hotel
        self.storage.save_all()

    def delete_hotel(self, hotel_id):
        self.storage.hotels.pop(hotel_id, None)
        self.storage.save_all()

    def get_hotel(self, hotel_id):
        return self.storage.hotels.get(hotel_id)
    
    def display_hotel(self, hotel_id):
        hotel = self.get_hotel(hotel_id)
        if not hotel:
            print("Hotel not found")
            return

        print(f"Hotel ID: {hotel.hotel_id}")
        print(f"Name: {hotel.name}")
        print(f"Rooms: {hotel.rooms}")
        print(f"Reserved: {hotel.reserved_rooms}")

    def modify_hotel(self, hotel_id, name, rooms):
        hotel = self.get_hotel(hotel_id)
        if hotel:
            hotel.name = name
            hotel.rooms = rooms
            self.storage.save_all()

    def reserve_room(self, hotel_id, room_number):
        hotel = self.get_hotel(hotel_id)
        if not hotel:
            return False
        if room_number in hotel.reserved_rooms:
            return False
        if room_number > hotel.rooms:
            return False

        hotel.reserved_rooms.append(room_number)
        self.storage.save_all()
        return True

    def cancel_room(self, hotel_id, room_number):
        hotel = self.get_hotel(hotel_id)
        if not hotel:
            return False

        if room_number in hotel.reserved_rooms:
            hotel.reserved_rooms.remove(room_number)
            self.storage.save_all()
            return True
        return False
    

class CustomerService:
    """Customer management."""

    def __init__(self, storage):
        self.storage = storage

    def create_customer(self, customer):
        self.storage.customers[customer.customer_id] = customer
        self.storage.save_all()

    def delete_customer(self, customer_id):
        self.storage.customers.pop(customer_id, None)
        self.storage.save_all()

    def get_customer(self, customer_id):
        return self.storage.customers.get(customer_id)

    def display_customer(self, customer_id):
        customer = self.get_customer(customer_id)
        if not customer:
            print("Customer not found")
            return

        print(f"Customer ID: {customer.customer_id}")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")

    def modify_customer(self, customer_id, name, email):
        customer = self.get_customer(customer_id)
        if customer:
            customer.name = name
            customer.email = email
            self.storage.save_all()

class ReservationService:
    """Reservation management."""

    def __init__(self, storage, hotel_service):
        self.storage = storage
        self.hotel_service = hotel_service

    def create_reservation(self, reservation):
        if reservation.customer_id not in self.storage.customers:
            return False

        if not self.hotel_service.reserve_room(
                reservation.hotel_id,
                reservation.room_number):
            return False

        self.storage.reservations[
            reservation.reservation_id] = reservation
        self.storage.save_all()
        return True

    def cancel_reservation(self, reservation_id):
        reservation = self.storage.reservations.get(reservation_id)
        if not reservation:
            return False

        self.hotel_service.cancel_room(
            reservation.hotel_id,
            reservation.room_number)

        del self.storage.reservations[reservation_id]
        self.storage.save_all()
        return True

