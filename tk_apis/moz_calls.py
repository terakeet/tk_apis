import requests
import os
import json
import base64
from typing import Optional, Union
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class MOZAPI:
    def __init__(
        self,
        urls: Optional[list] = None,
        access_id: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):

        """
        urls: Optional[list] -> list of URLs that you want to pull data for.
            This can be left blank and passed in when you call the method.

        access_id: Optional[str] -> MOZ access ID
        secret_key: Optional[str] -> MOZ secrect key

        You can delcare these last 2 variables ahead of time as enviornment,
        or you can pass in the ID & Key and we will use them in the
        scope of the class.
        If the enviornment variables are declared these should not be passed in.
        These are found at https://moz.com/products/mozscape/access
        """
        if access_id is None and secret_key is None:
            self.__id: str = os.environ["MOZ_ACCESS_ID"]
            self.__secret: str = os.environ["MOZ_SECRET_KEY"]
        else:
            self.__id = access_id
            self.__secret = secret_key

        # this url is the base of the API
        # https://moz.com/help/links-api/getting-started/overview
        self.base_url: str = "https://lsapi.seomoz.com/v2/"

        # set the url_list: type list
        self.url_list: list = urls

    def _signature(self) -> str:
        """
        Builds the authentication header signature.
        This is called from inside the self._api_call() method and
        should not be called outside that scope
        """
        encoded_auth = base64.b64encode(f"{self.__id}:{self.__secret}".encode("ascii"))
        return {
            "Authorization": "Basic " + encoded_auth.decode("utf-8"),
            "Content-Type": "text/plain",
        }

    def _api_call(self, api_endpoint: str, payload: dict) -> dict:
        """
        api_endpoint: str -> which API call we want to hit
        payload: dict -> body of the API call including params

        returns a request object json response if valid or the requests response if not
        """

        # we need to convert payload to a string when making the request
        payload = json.dumps(payload)

        # make the API request
        response = requests.request(
            "POST",
            self.base_url + api_endpoint,
            headers=self._signature(),
            data=payload,
        )
        return response.json() if response.ok else response

    def url_metrics(
        self, url_list: Optional[list] = None, params: Optional[dict] = None
    ) -> dict:
        """
        url_list: list -> urls (limit 50) to pull data for
        params: dict -> aditional parameters for this call. The "target" parameter is created by this method
            Do not pass in "target". See https://moz.com/help/links-api/making-calls/url-metrics
            for the full list of params

        return all data found under url_metrics endpoint
        """
        # if the passed in url_list is None (not passed in) we will use the url_list in the class
        if url_list is None:
            # if the class property is also None, raise an error. We need at least 1 URL to pull
            if self.url_list is None:
                raise ValueError(
                    "Please declare a URL in the class, or pass in a URL to this method"
                )
            url_list = self.url_list
        payload = self.format_targets(url_list)

        if params is not None:
            valid_vals = sum(list(map(lambda x: isinstance(x, list), params.values())))

            if valid_vals == len(params):
                payload = {**payload, **params}
            else:
                raise TypeError("Parameter values must be lists.")
        return self._api_call("url_metrics/", payload)

    def linking_domains(
        self,
        target_url: str,
        scope: str = "page",
        limit: int = 50,
        next_data: Optional[str] = None,
    ):
        """
        https://moz.com/help/links-api/making-calls/linking-root-domains

        target_url: str -> url of page we want to identify
        scope: str -> how we want to filter,
            Valid Values: page, subdomain, root_domain
        limit: int -> how many domains we want to pull in

        """
        payload = self.format_targets(target_url)
        if scope in {"page", "subdomain", "root_domain"}:
            payload["target_scope"] = scope

        payload["limit"] = limit

        if next_data != None:
            payload["next_token"] = next_data

        return self._api_call("linking_root_domains/", payload)

    def format_targets(self, url_list: Union[list, str] = None) -> dict:
        """
        takes a list (or string - signular url)
        of urls and appends https if not there

        sends the data back in a dictionary (default),
        can just send the data if you pass in False as 2nd param
        """
        if url_list is None:
            url_list = self.url_list

        elif isinstance(url_list, list):
            url_list = [self.add_prefix(url) for url in url_list]

        elif isinstance(url_list, str):
            url_list = [self.add_prefix(url_list)]

        return {"targets": url_list}

    def add_url(self, url: str) -> None:
        """
        Adds a url to the class list
        """
        self.url_list.append(url)

    @staticmethod
    def format_response(response: dict) -> pd.DataFrame:
        return pd.DataFrame(response["results"])

    @staticmethod
    def add_prefix(url: str) -> str:
        try:
            resp = requests.utils.prepend_scheme_if_needed(url, "https")
        except TypeError:
            print(f"Bad Value. Scheme cannot be applied to {url}")
            resp = url
        return resp
