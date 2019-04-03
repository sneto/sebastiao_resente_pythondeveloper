import ipinfo
from src import settings


handler = ipinfo.getHandler(access_token=settings.IP_INFO_TOKEN)


def get_ip_location(ip=None):
    """
    Get the location coordinates of an IP.
    :param ip: IP to get coordinates. If None, current internet connection IP will be used.
    :return: None if error or the an IP coordinates (latitude, longitude)
    """
    try:
        details = handler.getDetails(ip)
    except:
        details = None

    if not details:
        return None
    else:
        return details.latitude, details.longitude
