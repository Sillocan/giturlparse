import itertools
import re


class BasePlatform:
    FORMATS = {
        "ssh": r"ssh://%(_user)s@%(domain)s:%(repo)s%(dot_git)s",
        "http": r"http://%(domain)s/%(repo)s%(dot_git)s",
        "https": r"https://%(domain)s/%(repo)s%(dot_git)s",
        "git": r"git://%(domain)s/%(repo)s%(dot_git)s",
    }

    PATTERNS = {
        "ssh": r"(?P<_user>.+)@(?P<domain>[^/]+?):(?P<repo>.+).git",
        "http": r"http://(?P<domain>[^/]+?)/(?P<repo>.+).git",
        "https": r"https://(?P<domain>[^/]+?)/(?P<repo>.+).git",
        "git": r"git://(?P<domain>[^/]+?)/(?P<repo>.+).git",
    }

    # None means it matches all domains
    DOMAINS = None
    SKIP_DOMAINS = None
    DEFAULTS = {}

    def __init__(self):
        # Precompile PATTERNS
        self.COMPILED_PATTERNS = {proto: re.compile(regex, re.IGNORECASE) for proto, regex in self.PATTERNS.items()}

        # Supported protocols
        self.PROTOCOLS = self.PATTERNS.keys()

        if self.__class__ == BasePlatform:
            sub = [subclass.SKIP_DOMAINS for subclass in self.__class__.__subclasses__() if subclass.SKIP_DOMAINS]
            if sub:
                self.SKIP_DOMAINS = list(itertools.chain.from_iterable(sub))

    @staticmethod
    def clean_data(data):
        print(data)
        data["path"] = ""
        data["branch"] = ""
        data["protocols"] = list(filter(lambda x: x, data.get("protocols", "").split("+")))
        data["pathname"] = data.get("pathname", "").strip(":").rstrip("/")
        return data
