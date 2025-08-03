from datetime import datetime
from src.models.user import User
from src.models.room import Room
from src.models.reservation import Reservation
from src.repositories.reservation_repository import ReservationRepository
from src.services.booking_service import BookingService

def test_reserva():
    repo = ReservationRepository()
    service = BookingService(repo)
    user = User(1, "Ana")
    room = Room(1, "Sala B", 5)
    res1 = Reservation(1, user, room, datetime(2025, 8, 3, 9), datetime(2025, 8, 3, 10))
    res2 = Reservation(2, user, room, datetime(2025, 8, 3, 9, 30), datetime(2025, 8, 3, 10, 30))

    assert service.create_reservation(res1) == True
    assert service.create_reservation(res2) == False


