from commands import Network, imdict, Print, Time
from typing import Union
from ._version import __version__


class BitrixRESTAPI:
    def __init__(self, link):
        self.link = link.rstrip("/")
        self.verify = True
        print("bitrix_hook", __version__)
        
    def disable_ssl_sert_checking(self, bool_: bool):
        self.verify = not bool_
    
    def url_escaping(self, not_escaped_url: str) -> str:
        output_url = not_escaped_url
        output_url = output_url.replace("#", "%23")
        return output_url

    def get(self, method: str, params: dict = imdict(), verbose=False) -> dict:
        if isinstance(params, dict):
            params_str = self.dict2str_of_url_params(params)
        else:
            raise TypeError("params must be dict")

        url = self.url_escaping(f"{self.link}/{method}?{params_str}")
        response = Network.get(url, verify=self.verify)
        if verbose:
            Print.colored(response.url, "green")
        
        response_json = response.json()
        try:
            if response_json["error"] == 'QUERY_LIMIT_EXCEEDED':
                Time.sleep(1)
                return self.get(method=method, params=params)
        except KeyError:
            pass

        return response_json

    def smart_get(self, method: str,
                  params: dict = None,
                  verbose=False) -> dict:
        output = None
        if params is None:
            params = {}
        while True:
            params["start"] = 0 if output is None else len(output)
            response = self.get(method=method, params=params, verbose=verbose)

            # check if there is result
            try:
                if verbose:
                    Print.prettify(response['result'])
                output_part = response['result']
            except KeyError:
                Print.prettify(response)
                raise

            # if it's first page
            if output is None:
                output = output_part

            # else if it's second page
            elif isinstance(output, dict):
                output.update(output_part)
            else:
                output += output_part

            # if all is loaded
            try:
                if verbose:
                    Print.colored(f"{len(output)} of {response['total']} is loaded", "magenta")
                if response["total"] <= len(output):
                    break
            except KeyError:  # if there's no paged output
                break

        return output

    @staticmethod
    def zfill(str_like, count_of_zeros):
        return str(str_like).zfill(count_of_zeros)

    def date2str(self, d):
        return f"{d.year}-{self.zfill(d.month, 2)}-{self.zfill(d.day, 2)}T{self.zfill(d.hour, 2)}" \
               f":{self.zfill(d.minute, 2)}:{self.zfill(d.second, 2)}+05:00"

    def dict2list_of_url_params(self, dict_: dict, prefix: str = "", dict_name: Union[str, None] = None) -> list:
        output_list = []
        for key, value in dict_.items():
            if dict_name is None:
                current_prefix = key
            else:
                current_prefix = prefix + f"[{key}]"
            
            if isinstance(value, list) or isinstance(value, tuple):
                value = dict(enumerate(value))

            if isinstance(value, dict):
                output_list = output_list + self.dict2list_of_url_params(dict_=value, prefix=current_prefix, dict_name=key)
            else:
                output_list.append(f"{current_prefix}={value}")
            # debug Print(f"{prefix=}{current_prefix=}{key=}{value=}{output_list=}")
        return output_list

    def dict2str_of_url_params(self, dict_: dict) -> str:
        list_ = self.dict2list_of_url_params(dict_)
        return "&".join(list_)
