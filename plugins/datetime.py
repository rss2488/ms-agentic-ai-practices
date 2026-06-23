import datetime
import logging
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)


class DateTimePlugin:
    @kernel_function(
        description="Get the current time in the local time zone", name="Time"
    )
    def time(self) -> str:
        now = datetime.datetime.now()
        logger.info("DateTimePlugin: 'time' function called")
        return now.strftime("%I:%M:%S %p")

    @kernel_function(
        description="Get the current time zone offset", name="timeZoneOffset"
    )
    def time_zone_offset(self) -> str:
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        logger.info("DateTimePlugin: 'time_zone_offset' function called")
        return now.strftime("%z")
