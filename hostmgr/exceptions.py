"""
Custom exception and warning classes.
"""


class UserNotAuthorized(Exception):
    """ User is not authorized to manage this resource """
    pass


class HostnameInactive(Exception):
    """ This hostname is currently inactive and can not be assigned or reserved """
    pass


class InvalidStateTransition(Exception):
    """ This hostname is can not not transition to requested status """
    pass


class InvalidAssetIdType(Exception):
    """ Asset ID type is not valid """
    pass


class AssetIdRequired(Exception):
    """ Asset ID is required for hostname assignment """
    pass


class HostnamePersistent(Exception):
    """ This hostname is persistent and can not be modified """
    pass


class InsufficientHostnames(Exception):
    """ There are not enough available hostnames to complete this request """
    pass
