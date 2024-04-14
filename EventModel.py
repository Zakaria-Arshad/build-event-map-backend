from pydantic import BaseModel, Field, root_validator

# this model will parse and validate individual events from the SeatGeek API
# info needed : Event Title, Event Date, Lowest Price, Popularity, URL, Coordinates
class Event(BaseModel):
    datetime_utc: str
    title: str
    url: str
    popularity: float
    venue_name: str = Field(..., alias="venue.name")
    venue_location: dict = Field(..., alias="venue.location")
    lowest_price: float = Field(..., alias="stats.lowest_price")

    # this will get venue name and location from venue
    # this will get lowest price as well
    # root validation performed on entire data
    @root_validator(pre=True)
    def flatten_all(cls, values):
        venue_data = values.get("venue", {})
        if "name" in venue_data:
            values["venue.name"] = venue_data["name"]
        elif "name_v2" in venue_data: # backup plan in case name is not in it
            values["venue.name"] = venue_data["name_v2"]
        if "location" in venue_data:
            values["venue.location"] = venue_data["location"]
        
        stat_data = values.get("stats", {})
        if "lowest_price" in stat_data:
            values["stats.lowest_price"] = stat_data["lowest_price"]
        return values

