from datetime import datetime

class BookingService:
    def __init__(self, reservation_repository):
        self.reservation_repo = reservation_repository

    def is_available(self, room, start_time, end_time):
        for reservation in self.reservation_repo.get_all():
            if reservation.room.room_id == room.room_id:
                if not (end_time <= reservation.start_time or start_time >= reservation.end_time):
                    return False
        return True

    def create_reservation(self, reservation):
        if self.is_available(reservation.room, reservation.start_time, reservation.end_time):
            self.reservation_repo.add(reservation)
            return True
        return False

