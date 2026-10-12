from enum import Enum

class AmazonMusicTier(Enum):
    STD = "STD"
    HD = "HD"
    UHD = "UHD"
    ATMOS = "ATMOS"

class AmazonRegion(Enum):
    US = "US"
    EU = "EU"
    FE = "FE"

class AmazonContinent(Enum):
    NA = "NA"
    EU = "EU"
    FE = "FE"
    ROW = "ROW"

class AmazonMusicDevice:
    def __init__(self, *args, **kwargs):
        pass

class AmazonMusicMobileAPICredentials:
    def __init__(self, *args, **kwargs):
        pass
