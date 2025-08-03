class Reservation:
    def __init__(self, reservation_id, user, room, start_time, end_time):
        self.reservation_id = reservation_id
        self.user = user
        self.room = room
        self.start_time = start_time
        self.end_time = end_time
