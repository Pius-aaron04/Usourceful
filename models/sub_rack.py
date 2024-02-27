#!/usr/bin/python3
"""
Defines sub-racks.
"""
from models.rack import Rack, String, Column
from sqlachemy.orm import relationship


class subrack(Rack):
    """
    Sub racks for branched racks.
    """

    if getenv('USOURCEFUL_STORAGE') == 'db':
        rack_id = Column(String(60), nullable=False)
    else:
        rack_id = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes class

        param 1: non keyword args
        param 2: for keyword args
        """

        super().__init__(*args, **kwargs)
