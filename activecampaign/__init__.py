import requests

from django.conf import settings


class ActiveCampaign():
    def __init__(
        self,
        api_key=settings.ACTIVECAMPAIGN_API_KEY,
        api_url=settings.ACTIVECAMPAIGN_URL
    ):
        self.api_key = api_key
        self.api_url = api_url


    def api(self, api_action, method='get', params={}, data={}):
        """Build and call the api. Simple wrapper function to make my life a
           tiny bit easier, given that the ActiveCampaign wrapper they advertise
           does not support python3
        """
        url = '{}/admin/api.php'.format(self.api_url)

        payload = {
            'api_action': api_action,
            'api_key': self.api_key,
            'api_output': 'json',
            **params
        }

        f = getattr(requests, method)
        response = f(url, params=payload, data=data)

        return (response.status_code, response.json())
