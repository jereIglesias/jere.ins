from datetime import datetime
from models.user import User
from models.room import Room
from models.reservation import Reservation
from repositories.user_repository import UserRepository
from repositories.room_repository import RoomRepository
from repositories.reservation_repository import ReservationRepository
from services.booking_service import BookingService

# Crear repositorios
user_repo = UserRepository()
room_repo = RoomRepository()
reservation_repo = ReservationRepository()
booking_service = BookingService(reservation_repo)

# ejemplo para Craear datos
user = User(1, "Jere")
room = Room(1, "Sala A", 10)
user_repo.add(user)
room_repo.add(room)

# ejemplo para Crear una reserva
start = datetime(2025, 8, 3, 10, 0)
end = datetime(2025, 8, 3, 11, 0)
reservation = Reservation(1, user, room, start, end)

if booking_service.create_reservation(reservation):
    print("Reserva realizada con éxito")
else:
    print("La sala no está disponible")


