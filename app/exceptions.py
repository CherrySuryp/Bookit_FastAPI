from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User Already Exists"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email or Password"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Your cookie token has expired"
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing JWT token"
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token format"
)

UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

RoomCanNotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="No rooms left"
)

BookingDoesntExistException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Booking doesn't exist"
)

BookingsDoesNotExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User doesn't have bookings"
)

HotelNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found"
)

AvailableHotelsNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="No hotels were found according to the specified parameters",
)

RoomsOrHotelNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="No rooms were found according to the specified parameters",
)

TooMuchDaysException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Too many days"
)

WrongDateEntryException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Date to is less than date from"
)
