"""
Hotel Reservation System
"""

import json
import os
import unittest
from io import StringIO
from unittest.mock import patch

DATA_DIR = "A6.2/data"
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
        """Return hotel attributes as Dict"""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "rooms": self.rooms,
            "reserved_rooms": self.reserved_rooms,
        }

    @staticmethod
    def from_dict(data):
        """Get hotel instance from Dict"""
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
        """Return customer attributes as Dict"""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data):
        """Get customer instance from Dict"""
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
        """Return reservation attributes as Dict"""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_number": self.room_number,
        }

    @staticmethod
    def from_dict(data):
        """Get reservation instance from Dict"""
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

    def save_hotel(self):
        """Save hotel instances information to JSON file"""
        save_json(HOTELS_FILE,
                  {k: v.to_dict() for k, v in self.hotels.items()})

    def save_customer(self):
        """Save customer instances information to JSON file"""
        save_json(CUSTOMERS_FILE,
                  {k: v.to_dict() for k, v in self.customers.items()})

    def save_reservation(self):
        """Save reservation instances information to JSON file"""
        save_json(RESERVATIONS_FILE,
                  {k: v.to_dict() for k, v in self.reservations.items()})

    def save_all(self):
        """Save all instances information to JSON files"""
        self.save_hotel()
        self.save_customer()
        self.save_reservation()


class HotelService:
    """Hotel management operations."""

    def __init__(self, storage):
        self.storage = storage

    def create_hotel(self, hotel):
        """Add hotel instance to storage"""
        self.storage.hotels[hotel.hotel_id] = hotel
        self.storage.save_all()

    def delete_hotel(self, hotel_id):
        """Delete a hotel instance from storage"""
        self.storage.hotels.pop(hotel_id, None)
        self.storage.save_all()

    def get_hotel(self, hotel_id):
        """Delete a hotel instance from storage"""
        return self.storage.hotels.get(hotel_id)

    def display_hotel(self, hotel_id):
        """Display hotel information"""
        hotel = self.get_hotel(hotel_id)
        if not hotel:
            print("Hotel not found")
            return

        print(f"Hotel ID: {hotel.hotel_id}")
        print(f"Name: {hotel.name}")
        print(f"Rooms: {hotel.rooms}")
        print(f"Reserved: {hotel.reserved_rooms}")

    def modify_hotel(self, hotel_id, name, rooms):
        """Modify hotel information"""
        hotel = self.get_hotel(hotel_id)
        if hotel:
            hotel.name = name
            hotel.rooms = rooms
            self.storage.save_all()

    def reserve_room(self, hotel_id, room_number):
        """Reserve room from hotel"""
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
        """Cancel room reservation from hotel"""
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
        """Add customer instance to storage"""
        self.storage.customers[customer.customer_id] = customer
        self.storage.save_all()

    def delete_customer(self, customer_id):
        """Delete customer from storage"""
        self.storage.customers.pop(customer_id, None)
        self.storage.save_all()

    def get_customer(self, customer_id):
        """Get customer instance from ID"""
        return self.storage.customers.get(customer_id)

    def display_customer(self, customer_id):
        """Display customer information"""
        customer = self.get_customer(customer_id)
        if not customer:
            print("Customer not found")
            return

        print(f"Customer ID: {customer.customer_id}")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")

    def modify_customer(self, customer_id, name, email):
        """Modify customer information"""
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
        """Add reservation instance to storage"""
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
        """Delete reservation instance from storage"""
        reservation = self.storage.reservations.get(reservation_id)
        if not reservation:
            return False

        self.hotel_service.cancel_room(
            reservation.hotel_id,
            reservation.room_number)

        del self.storage.reservations[reservation_id]
        self.storage.save_all()
        return True


class TestHotelSystem(unittest.TestCase):
    """Test Management"""

    def setUp(self):
        self.storage = Storage()
        self.hotel_service = HotelService(self.storage)
        self.customer_service = CustomerService(self.storage)
        self.reservation_service = ReservationService(
            self.storage,
            self.hotel_service,
        )

        self.hotel = Hotel("H1", "Test Hotel", 10)
        self.customer = Customer("C1", "Juan", "juan@email.com")

        self.hotel_service.create_hotel(self.hotel)
        self.customer_service.create_customer(self.customer)

    def test_invalid_json_file(self):
        """Testing an invalid JSON file"""
        with open("A6.2/data/hotels.json", "w", encoding="utf-8") as f:
            f.write("{ invalid json")

        storage = Storage()
        self.assertEqual(storage.hotels, {})

    def test_create_and_get_hotel(self):
        """Test the creation and get of a hotel"""
        hotel = self.hotel_service.get_hotel("H1")
        self.assertEqual(hotel.name, "Test Hotel")

    def test_modify_hotel(self):
        """Test the modification of hotel """
        self.hotel_service.modify_hotel("H1", "Updated", 20)
        self.assertEqual(
            self.hotel_service.get_hotel("H1").rooms, 20)

    def test_reserve_room(self):
        """Test room reservation"""
        result = self.hotel_service.reserve_room("H1", 2)
        self.assertTrue(result)

    def test_cancel_room(self):
        """Test room cancelation"""
        self.hotel_service.reserve_room("H1", 3)
        result = self.hotel_service.cancel_room("H1", 3)
        self.assertTrue(result)

    def test_create_reservation(self):
        """Test reservation creation"""
        reservation = Reservation("R1", "C1", "H1", 2)
        result = self.reservation_service.create_reservation(
            reservation)
        self.assertTrue(result)

    def test_cancel_reservation(self):
        """Test reservation cancelation"""
        reservation = Reservation("R2", "C1", "H1", 3)
        self.reservation_service.create_reservation(reservation)
        result = self.reservation_service.cancel_reservation("R2")
        self.assertTrue(result)

    def test_invalid_reservation(self):
        """Test invalid reservation"""
        reservation = Reservation("R3", "INVALID", "H1", 1)
        self.assertFalse(
            self.reservation_service.create_reservation(reservation)
        )

    def test_display_hotel(self):
        """Test correct hotel information display"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.hotel_service.display_hotel("H1")
            output = fake_out.getvalue()
        self.assertIn("Hotel ID: H1", output)
        self.assertIn("Name: Test Hotel", output)
        self.assertIn("Rooms: 10", output)
        self.assertIn("Reserved: []", output)

    def test_display_hotel_not_found(self):
        """Test incorrect hotel information display"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.hotel_service.display_hotel("INVALID")
            self.assertIn("Hotel not found", fake_out.getvalue())

    def test_display_customer(self):
        """Test correct customer information display"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.customer_service.display_customer("C1")
            output = fake_out.getvalue()
        self.assertIn("Customer ID: C1", output)
        self.assertIn("Name: Juan", output)
        self.assertIn("Email: juan@email.com", output)

    def test_display_customer_not_found(self):
        """Test incorrect customer information display"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.customer_service.display_customer("INVALID")
            self.assertIn("Customer not found", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
