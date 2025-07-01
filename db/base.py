# Import all the models, so that Base has them before being
# imported by Alembic
from db.session import Base  # noqa
from modules.users.models.user import User, UserType, SavedList # noqa
from modules.trips.models.trip import ( # noqa
    Location, Trip, Activity, ActivityVideos, TripDocument, TripSchedule, Schedule
)
from modules.tips.models.tip import Tip # noqa
