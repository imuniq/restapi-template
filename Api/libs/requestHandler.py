import cloudscraper
import random
import time, string
import re
from urllib.parse import unquote_plus, quote_plus
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

class termcolor:
    CEND = '\33[0m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'
    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'

    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    GREY = '\33[90m'
    RED2 = '\33[91m'
    GREEN2 = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2 = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2 = '\33[96m'
    WHITE2 = '\33[97m'

    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'
    END = '\033[0m'

class Objector:

        def __init__(self, json_dict) -> None:
                self.__dict__ = json_dict
                for key, value in json_dict.items():
                        if isinstance(value, dict):
                                setattr(self, key, Objector(value))

        def __getattr__(self, attr):
                if attr in self.__dict__:
                        return self.__dict__[attr]
                else:
                        return None
                
class RequestHandler:
    def __init__(self, capsolver_key: str = None, proxies: list = [], proxy_type: str = "http") -> None:
        self.capsolver_key = capsolver_key
        self.proxies = self.set_proxy(proxies, proxy_type).get("proxies", None)
        self.session = cloudscraper.session()
        self.session.proxies = self.proxies
        self.UNIT_MAPPING = {
        'd': 'days',
        'h': 'hours',
        'm': 'minutes'
    }

    def set_proxy(self, proxies: list, proxy_type: str = "http"):
        try:
            if not proxies:
                return {"error": "No proxies provided"}

            host, port, user, pas = random.choice(proxies).split(":")[:4]

            return {
                "proxies": {
                    'http': f'{proxy_type}://{user}:{pas}@{host}:{port}',
                    'https': f'{proxy_type}://{user}:{pas}@{host}:{port}'
                }
            }
        except Exception as e:
            return {"error": str(e)}
        

    def generate_serial_key(self, prefix="APP", keylen=4):
        def rnd_str():
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=keylen))
        serial_key = f"{prefix}-{rnd_str()}-{rnd_str()}-{rnd_str()}"
        return serial_key.lower()
    
    def group_list(self, limit: int, l: list) -> list[list]:
        """
        List of Groups
        --------------
        Use this method to make a list of groups
        """
        t = [l[i:i+limit] for i in range(0, len(l), limit)]
        return t
    
    def get_percent(self, amount: int, total_amount: int):
        """
        Get Perchentage
        ---------------
        Returns a perchentage of a number
        """
        return "{0:.0f}%".format(amount/total_amount * 100)

    def num_formator(self, num: int) -> str:
        """
        Number Formatter
        ----------------
        Convert your integer into perfect format.
        """
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),
                             ['', 'K', 'M', 'B', 'T'][magnitude])
    
    def is_valid_email(self, email: str):
        """
        To check email validation
        """
        rx = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(rx, email)):
                return True

        else:
                return False
    
    def extract_emails(self, text: str) :
        """
        To extract emails from a string.
        """
        try:
            r = re.findall(r"[A-Za-z0-9_%+-.]+"
                           r"@[A-Za-z0-9.-]+"
                           r"\.[A-Za-z]{2,5}", text)
            return r
        except Exception as er:
            raise Exception(f"Failed to exctract: {str(er)}")

    def xform_builder(self, json_data: dict) -> str:
        result = []
        for key, value in json_data.items():
            ekey = quote_plus(key)
            evalue = quote_plus(value)
            result.append(f"{ekey}={evalue}")
        return '&'.join(result)

    def divide_string(self, text: str, parts: int = 4):

        if len(text) % parts == 0:
            part_length = len(text) // parts
            return [text[i:i+part_length] for i in range(0, len(text), part_length)]
        else:
            return None

    def xform_parser(self, data: str) -> dict:
        try:
            result = {}
            for item in data.split('&'):
                key, value = item.split('=', 1)
                result[key] = unquote_plus(value)
            return result
        except Exception:
            return None

    def jsonify(self, headers: str):
        try:

            pattern = re.compile(r'([^\s:]+):\s*([\s\S]+?)(?=\n|$)')
            matches = pattern.findall(headers)
            result = {k.strip(): v.strip() for k, v in matches}
            return result

        except Exception:
            return None

    def _parse_proxy(self, proxy_data: str):
        proxies = re.findall(r'(\S+:\d+:\S+:\S+)', proxy_data)
        return proxies
    
    def _date_diff_in_seconds(self, dt2, dt1):
        time_difference = dt1 - dt2
        return int(time_difference.total_seconds())

    def _dhms_from_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    def get_expire_time(self, expire_timestamp):

        expire_date = datetime.fromtimestamp(expire_timestamp, timezone.utc).replace(microsecond=0)
        current_date = datetime.now(timezone.utc).replace(microsecond=0)

        time_difference = self._date_diff_in_seconds(current_date, expire_date)
        days, hours, minutes, seconds = self._dhms_from_seconds(time_difference)

        if time_difference < 0:
            return "expired"

        day = "{} day{}".format(str(days), "s" if days >= 2 else "")
        day = [day] if days >= 1 else []
        hr = "{} hour{}".format(str(hours), "s" if hours >= 2 else "")
        hr = [hr] if hours >= 1 else []
        minn = "{} minute{}".format(str(minutes), "s" if minutes >= 2 else "")
        minn = [minn] if minutes >= 1 else []

        sec = "{} second{}".format(str(seconds), "s" if seconds >= 2 else "")
        sec = [sec] if seconds >= 1 else []

        return ", ".join(day + hr + minn + sec)

    def get_future_time(self, time):
        """
        Get Future Time
        """
        components = time.split()
        time_dict = {component[-1]: int(component[:-1])
                     for component in components}

        dt = datetime.now(timezone.utc)
        td = timedelta(**{self.UNIT_MAPPING[unit]: value for unit, value in time_dict.items()})
        my_date = dt + td
        return my_date
     
    def starts_with(self, item: str, lis: list) -> bool:
     return any(item.startswith(x) for x in lis)
    
    def ends_with(self, item: str, lis: list) -> bool:
     return any(item.endswith(x) for x in lis)
    
    def extract_url(self, text: str):
        """
        To extract urls from a string
        """
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
        return urls


    def generate_key(self):
        return Fernet.generate_key().decode()

    def encrypt_data(self, value, key):
        cipher_suite = Fernet(key)
        encrypted_value = cipher_suite.encrypt(value.encode())
        return encrypted_value.hex()

    def decrypt_data(self, encrypted_value_hex, key):
        cipher_suite = Fernet(key)
        encrypted_value = bytes.fromhex(encrypted_value_hex)
        decrypted_value = cipher_suite.decrypt(encrypted_value).decode()
        return decrypted_value
    

    def capsolver(self, key: str, payload: dict):
        url = "https://api.capsolver.com/createTask"
        requests = cloudscraper.session()
        response = requests.post(url, json=payload)
        # print(response.text)
        resp = response.json()

        if not resp.get("taskId", None):
            error = resp["errorDescription"]

            return {"error": f"Error - {error}"}

        time.sleep(5)
        url = "https://api.capsolver.com/getTaskResult"
        payload = {
            "clientKey": key,
            "taskId": resp['taskId']
        }
        while True:
            getresult = requests.post(url,  json=payload)
            result = getresult.json()
            status = result["status"]
            if not status in ["processing","idle"]:
                return {"token": result['solution']['gRecaptchaResponse']}
            else:
                continue
       