"""
Hotel Reservation System
"""

import json
import os
import unittest


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


