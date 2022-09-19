from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, DECIMAL
from hethongquanlyChuyenBay import db
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from datetime import datetime
from enum import Enum as Enums
class UserRole(Enums):
    CUSTOMER = 1
    EMPLOYEE = 2
    ADMIN = 3

class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole, default=UserRole.ADMIN))

    def __str__(self):
        return self.username

    def get_id(self):
        return self.account_id

class User(db.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(10), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(DateTime, default=datetime.strptime("1/1/2001", "%d/%m/%Y"))
    identity_card = Column(String(15), nullable=False, unique=True)
    avatar = Column(String(150))
    phone = Column(String(15), nullable=False)
    accounts = relationship('Account', backref='user', lazy=True, cascade="all, delete", passive_deletes=True)

class Customer(db.Model):
    __tablename__ = 'customer'
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False, primary_key=True)
    mileage_acquired = Column(Integer, default=0)
    tickets = relationship('Ticket', backref='customer', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False, primary_key=True)
    starting_date = Column(DateTime, default=datetime.now())
    salary = Column(DECIMAL(13, 3), default=0)
    # bills = relationship('Bill', backref='employee', lazy=True)


# class Bill(db.Model):
#     __tablename__ = 'bill'
#     bill_id = Column(String(6), primary_key=True, nullable=False)
#     date_of_payment = Column(DateTime, default=datetime.now())
#     amount = Column(DECIMAL(13, 3), nullable=False)
#     status = Column(Boolean, default=False)
#     tickets = relationship('Ticket', backref='bill', lazy=False, cascade="all, delete", passive_deletes=True)

class Airport(db.Model):
    __tablename__ = 'airport'
    airport_id = Column(String(3), nullable=False, primary_key=True)
    airport_name = Column(String(50), nullable=False, unique=True)
    location = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)
    transit_airports = relationship('TransitAirport', backref='airport', lazy=True)

class TransitAirport(db.Model):
    __tablename__ = 'transit_airport'
    transit_airport_id = Column(String(3), ForeignKey('airport.airport_id'), nullable=False, primary_key=True)
    flight_id = Column(String(10), ForeignKey('flight.flight_id'), nullable=False, primary_key=True)
    timing_point = Column(Integer, default=0)
    arrival_day = Column(DateTime)

class Airline(db.Model):
    __tablename__ = 'airline'
    airline_id = Column(String(2), primary_key=True)
    airline_name = Column(String(50), nullable=False, unique=True)
    airplanes = relationship('Airplane', backref='airline', lazy=True)


class Flight(db.Model):
    __tablename__ = 'flight'
    flight_id = Column(String(10), primary_key=True, nullable=False)
    airplane_id = Column(String(7), ForeignKey('airplane.airplane_id'), nullable=False)
    flight_time = Column(Integer, default=0)
    departure_day = Column(DateTime, nullable=False)
    arrival_day = Column(DateTime, nullable=False)
    seat_classes = relationship('SeatClass', backref='flight', lazy=True, cascade="all, delete", passive_deletes=True)
    ticket_prices = relationship('TicketPrice', backref='flight', lazy=True, cascade="all, delete", passive_deletes=True)
    tickets = relationship('Ticket', backref='flight', lazy=True)
    transit_airports = relationship('TransitAirport', backref='flight', lazy=True)

class Airplane(db.Model):
    __tablename__ = 'airplane'
    airplane_id = Column(String(7), primary_key=True, nullable=False)
    airplane_type = Column(String(4), ForeignKey('airplane_type.id'), nullable=False)
    airline_id = Column(String(2), ForeignKey('airline.airline_id'), nullable=False)
    active = Column(Boolean, default=True)
    seats = relationship('Seat', backref='airplane', lazy=True, cascade="all, delete", passive_deletes=True)
    flights = relationship('Flight', backref='airplane', lazy=True)

class AirplaneType(db.Model):
    __tablename__ = 'airplane_type'
    id = Column(String(4), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    seat_number = Column(Integer, default=0)
    airplanes = relationship('Airplane', backref='airplane type', lazy=True)

class SeatType(db.Model):
    __tablename__ = 'seat_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    seats = relationship('Seat', backref='seat type', lazy=True)
    seat_classes = relationship('SeatClass', backref='seat type', lazy=True)


class Seat(db.Model):
    __tablename__ = 'seat'
    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    seat_name = Column(String(3), nullable=False)
    seat_type = Column(Integer, ForeignKey('seat_type.id'))
    active = Column(Boolean, default=True)

    airplane_id = Column(String(10), ForeignKey('airplane.airplane_id', ondelete="CASCADE"), nullable=False)
    tickets = relationship('Ticket', backref='seat', lazy=True)

class SeatClass(db.Model):
    __tablename__ = 'seat_class'
    flight_id = Column(String(10), ForeignKey('flight.flight_id', ondelete="CASCADE"), primary_key=True, nullable=False)
    seat_type = Column(Integer, ForeignKey('seat_type.id'), primary_key=True, nullable=False)
    seat_number = Column(Integer, default=0)

class TicketType(db.Model):
    __tablename__ = 'ticket_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    tickets = relationship('Ticket', backref='ticket type', lazy=True)
    ticket_prices = relationship('TicketPrice', backref='ticket type', lazy=True)

class TicketPrice(db.Model):
    __tablename__ = 'ticket_price'
    flight_id = Column(String(10), ForeignKey('flight.flight_id', ondelete="CASCADE"), primary_key=True, nullable=False)
    ticket_type = Column(Integer, ForeignKey('ticket_type.id'), primary_key=True)
    price = Column(DECIMAL(13, 3), default=0)
    quantity = Column(Integer, default=0)
class Ticket(db.Model):

    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(String(10), ForeignKey('flight.flight_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.user_id'), nullable=False)
    ticket_type = Column(Integer, ForeignKey('ticket_type.id'))
    seat_id = Column(Integer, ForeignKey('seat.seat_id'), nullable=False)

if __name__ == '__main__':
    db.create_all()


