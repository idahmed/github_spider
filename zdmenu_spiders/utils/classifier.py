import re

from requests import Response

from zdmenu_spiders import settings

# api_key = settings.SCRAPY_WEB_API_KEY


class BaseClassifier(object):
    matched = []

    def __init__(self, url=None, response=None, bio=None):
        if not url and not response and not bio:
            raise ValueError("At least one should be set")
        self.url = url or ""
        self.response = response or Response()
        self.bio = bio or ""
        self.matched = []

    def find_matches_for(self, name):
        attr = getattr(self, name)
        if attr == "clicks":
            if (
                re.findall(rf"{attr}", self.url)
                or re.findall(rf"{attr}", self.bio, re.IGNORECASE)
                or re.findall(rf"{attr}", self.response.text, re.IGNORECASE)
            ):
                self.matched.append(name)
        if re.findall(rf"{attr}", self.url) or re.findall(
            rf"{attr}", self.bio, re.IGNORECASE
        ):
            self.matched.append(name)


class FoodAggregatorClassifier(BaseClassifier):
    """ This class is used to detect detects direct competitors like talabat, El menu, etc
    """

    """
    The below unicode chars representing the Arabic translations for
    دليڤرو , ديليڤرو, طلبات, كاريدج , ديليفرو,دليفرو,ديلفيروو
    """

    elmenus = "\\b\@?[eE]lmenus(\.com)?\\b|[eE]lmenus"
    zomato = "\\b\@?[zZ]omato(\.com)?\\b|[zZ]omato"
    payzah = "\\b\@?[pP]ayzah(\.com)?\\b|[pP]ayzah"
    bilbayt = "\\b\@?[bB]ilbayt(\.com|\.ksa|\.kw|\.kwt)?\\b|[bB]ilbayt"
    cravez = "\\b[Cc]ravez+\\b|\\bCRAVEZ\\b|\\b[cC]raves\\b|\\b\@?[Cc]ravez(kwt|KWT)\\b|\u0643\u0631\u064A\u0641\u0632|\u0643\u0631\u064A\u06A4\u0632"
    talabat = "talabat|\\bTALABAT\\b|\\b\@?[tT]alabat(kwt|KWT|qa|QA)?(\.com)?\\b|(?u)\\b\u0637\u0644\u0628\u0627\u062A\\b"
    carriage = "[Cc]arriage|\\b\@?[cC]arriage(kwt|KWT)?(\.com)?\\b|\\b[tT]ry[cC]arriage(kwt|KWT)?(\.com)?\\b|(?u)\\b\u0643\u0627\u0631\u064A\u062F\u062C\\b"
    deliveroo = "[dD]elivero|\\b\@?deliveroo(\.|_)kw\\b|\\b\@?[dD]eliver[o]{1,3}(\.com)?\\b|(?u)\\b\u062F\u064A\u0644\u0641\u064A\u0631\u0648\u0648\\b|(?u)\\b\u062F\u0644\u064A\u0641\u0631\u0648\\b|(?u)\\b\u062F\u064A\u0644\u064A\u0641\u0631\u0648\\b|(?u)\\b\u062F\u064A\u0644\u064A\u06A4\u0631\u0648\\b|(?u)\\b\u062F\u0644\u064A\u06A4\u0631\u0648\\b|(?u)\\b\u062f\u064a\u0644\u06a4\u064a\u0631\u0648\u0648\\b"
    clicks = "\\b(use)?clicks(\.com|\.kw|_kw)?\\b|\\bClicks\\b"
    hungerstation = (
        "hungerstation|(?u)\\b\u0647\u0646\u0642\u0631\u0633\u062a\u064a\u0634\u0646\\b"
    )
    careem = "\\b[cC]areem[a-z]{1,4}\\b"

    def get_match(self):
        self.find_matches_for("talabat")
        self.find_matches_for("elmenus")
        self.find_matches_for("carriage")
        self.find_matches_for("deliveroo")
        self.find_matches_for("zomato")
        self.find_matches_for("payzah")
        self.find_matches_for("bilbayt")
        self.find_matches_for("cravez")
        self.find_matches_for("clicks")
        self.find_matches_for("hungerstation")
        self.find_matches_for("careem")
        return self.matched


class IndirectCompetitorsClassifier(BaseClassifier):
    """ This class is used to detect detects direct competitors like whatsapp, V-Thru,
    """

    vthru = "(?u)\\b\u0641\u064a \u062b\u0631\u0648\\b|(?u)\\b\u06a4\u064a \u062b\u0631\u0648\\b|\\b[vV](-|_|\s)?thru(\.com)?\\b"
    whatsapp = "\\b\@?[Ww]hats(\s)?[aA]pp(\.com)?\\b|(?u)\u0648\u0627\u062A\u0633"

    def get_match(self):
        self.find_matches_for("vthru")
        self.find_matches_for("whatsapp")
        if re.findall(r"whatsapp\.com", self.response.text.lower()):
            self.matched.append("whatsapp")
        if re.findall(
            r"kitopi|kitopiconnect\.com", self.response.text, re.IGNORECASE
        ) or re.findall(r"kitopi|kitopiconnect\.com", self.bio, re.IGNORECASE):
            self.matched.append("kitopi")
        if re.findall(
            r"finedinemenu|fndn\.mn", self.response.text, re.IGNORECASE
        ) or re.findall(r"finedinemenu|fndn\.mn", self.bio, re.IGNORECASE):
            self.matched.append("finedine")
        return self.matched


class DirectCompetitorsClassifier(BaseClassifier):
    """ This class is used to detects direct competitors like Mnasati, Itsordable, etc
    """

    def get_match(self):
        # if Zyda Closed
        if "Sorry" and "receive your order at the moment" in self.response.text:
            self.matched.append("zyda_closed")
        # If Zyda
        if (
            "https://zyda-photos-prod.s3.amazonaws.com" in self.response.text
            or "zyda.com" in self.response.text
        ):
            self.matched.append("zyda")
        # If Mnasati
        if (
            "Powered By MNASATI" in self.response.text
            or "mnasaticdn.com" in self.response.text
        ):
            self.matched.append("mnasati")
        # If Itsordable
        if "tapcom-live.ams3.cdn.digitaloceanspaces.com" in self.response.text:
            self.matched.append("itsordable")
        # If plugn
        if "es.cloudinary.com/plugn" in self.response.text:
            self.matched.append("plugn")
        # If Simple Broker
        if re.findall(
            r"\bsimple\sbroker\b|simplebroker\.com", self.response.text, re.IGNORECASE
        ):
            self.matched.append("simple broker")
        # If Chat Food
        if "chatfood.imgix.net" in self.response.text:
            self.matched.append("chatfood")
        # If Taker
        if (
            "https://web-production-b.my.taker.io/static/js/2.chunk.js"
            in self.response.text
        ):
            self.matched.append("taker")
        # If BlinkCo
        if "https://www.blinkco.io" in self.response.text:
            self.matched.append("blinkco")
        # If UPayaments
        if "https://upayments.com/en/ustore/" in self.response.text:
            self.matched.append("upayments")
        # If Zvendo
        if "zvendo.com" in self.response.text:
            self.matched.append("zvendo")
        # If Zammit
        if "https://zammit.s3-eu-west-1.amazonaws.com" in self.response.text:
            self.matched.append("zammit")
        # If BentoBox
        if "getbento.com" in self.response.text:
            self.matched.append("bentobox")
        # If Chownow
        if "chownow" in self.response.text:
            self.matched.append("chownow")
        # If GloriaFood
        if "https://www.fbgcdn.com/embedder/js/ewm2.js" in self.response.text:
            self.matched.append("gloriafood")
        # if tryorder.online
        if (
            "tryorder.online" in self.url
            or "tryorder.online" in self.response.text
            or "tryorder.online" in self.bio
        ):
            self.matched.append("tryorder")
        return self.matched
