from enum import StrEnum


class UrlFilterLevels(StrEnum):

    OFF = 'off'
    """Disabled"""

    BLACKLIST = 'blacklist'
    """Deleting only links from blacklist"""

    WHITELIST = 'whitelist'
    """Deleting only links from whitelist"""

    ALL = 'all'
    """Deleting all links"""
