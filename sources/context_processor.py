from sourcelist.settings import DONATE_URL


def add_global_vars(request):
    """
    This adds global variables we can use in the templates.

    :param request:
    :return: context variable
    :rtype: dict
    """

    return {
        'donate_url': DONATE_URL,
    }
