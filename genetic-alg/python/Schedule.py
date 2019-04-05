"""Schedule class implementation."""

class Schedule:
    def __init__(self):
        self.schedule = None

    def Schedule(self, nRooms, nTimeSlots):
        """Creates a schedule nTimeSlots x nRooms.
        :param nRooms: Number of rooms.
        :param nTimeSlots: Number of time slots.
        """
        self.schedule = [[0 for x in range(nTimeSlots)] for y in range(nRooms)]
