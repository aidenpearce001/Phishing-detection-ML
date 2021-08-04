# importing required packages for this section
from urllib.parse import urlparse,urlencode
import ipaddress
import re
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
import dns.resolver
import socket
import time
import gc

truseted_ca = ['cPanel,',
 'Microsoft',
 'HydrantID',
 'AlphaSSL',
 'GTS',
 'RapidSSL',
 'DFN-Verein',
 'Cloudflare',
 'GeoTrust',
 'QuoVadis',
 'Certum',
 'Amazon',
 'Gandi',
 'COMODO',
 'Go',
 'Cybertrust',
 'GlobalSign',
 'Yandex',
 'R3',
 'Network',
 'DigiCert',
 'GoGetSSL',
 'Thawte',
 'Apple',
 'Starfield',
 'RU-CENTER',
 'Trustwave',
 'Entrust',
 'InCommon',
 'Sectigo',
 'Secure']

headers = {

    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

class Extractor():
    def __init__(self):
        self.feature_names = ['Speical_Char','Have_IP', 'Have_At','URL_length' ,'URL_Depth','redirection', 'time_get_redirect',
                        'port_in_url','use_http', 'http_in_domain','TinyURL', 'Prefix/Suffix', 'DNS_Record','trusted_ca',
                        'domain_lifespan', 'domain_timeleft', 'same_asn','iFrame', 'Mouse_Over','Right_Click','eval','unescape',
                        'escape', 'ActiveXObject','fromCharCode','atob','Punny_Code',
                        'TLDs','Title','country_name']
    
    # 1.Speical Chartacter in URL
    @staticmethod
    def special_char(url):
        url = url.replace("/","")
        url = url.replace("-","")
        special = re.sub('[\w]+' ,'', url)

        return len(special)
    # 2.Checks for IP address in URL (Have_IP)
    @staticmethod
    def havingIP(url):
        try:
            if ipaddress.ip_address(url) and Extractor.getLength(url) == 1 :
                ip = 1
        except:
            ip = 0
        return ip

    # 3.Checks the presence of @ in URL (Have_At)
    @staticmethod
    def haveAtSign(url):
        if "@" in url and Extractor.getLength(url) == 1:
            at = 1    
        else:
            at = 0    
        return at

    # 4.Finding the length of URL and categorizing (URL_Length)
    @staticmethod
    def getLength(url):
        if "?fbclid" in url: #Fukin link in facebook contain fbclid
            url = url.split("?fbclid")[0]
        if len(url) < 54:
            length = 0            
        else:
            length = 1            
        return length

    # 5.Gives number of '/' in URL (URL_Depth)
    @staticmethod
    def getDepth(url):
        s = urlparse(url).path.split('/')
        depth = 0
        for j in range(len(s)):
            if len(s[j]) != 0:
                depth = depth+1
        return depth 

    # 6.Checking for redirection '//' in the url (Redirection)
    @staticmethod
    def redirection(url):
        pos = url.rfind('//')
        return pos

    # 7.Redirect time 
    @staticmethod
    def forwarding(response):
        try:

            n_redirect = len([response for response in responses.history])

            return n_redirect
        except:
            return 0

    # 8.
    @staticmethod
    def port_in_url(url):
        p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

        m = re.search(p,url)
        if m.group('port') :
            return 1
        else :
            return 0

    # 9.
    @staticmethod
    def notsafe_protocol(url):
        if urlparse(url).scheme == 'http':
            return 1
        else:
            return 0

    # 10.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
    @staticmethod
    def httpDomain(url):
        # domain = urlparse(url).netloc
        # if 'http' in domain and Extractor.getLength(url) == 1:
        if 'http' in url.split("//")[1]:
            return 1
        else:
            return 0

    # 11. Checking for Shortening Services in URL (Tiny_URL)
    @staticmethod
    def tinyURL(url):
            #listing shortening services
        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                        r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                        r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                        r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                        r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                        r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                        r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                        r"tr\.im|link\.zip\.net"
        match=re.search(shortening_services,url)
        if match:
            return 1
        else:
            return 0
    # 12.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
    @staticmethod
    def prefixSuffix(url):
        if '-' in urlparse(url).netloc:
            return 1            # phishing
        else:
            return 0            # legitimate

    # Reject
    @staticmethod
    def web_traffic(url):
        try:
            #Filling the whitespaces in the URL if any
            url = urllib.parse.quote(url)
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
            rank = int(rank)
        except TypeError:
                print("Cant get web traffic")
                return 1
        if rank <100000:
            return 0
        else:
            return 1

    # 13
    @staticmethod
    def trusted_ca(domain):
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain['domain_name']) as s:
                s.settimeout(5)
                s.connect((domain['domain_name'], 443))
                cert = s.getpeercert()

            subject = dict(x[0] for x in cert['subject'])
            issued_to = subject['commonName']
            issuer = dict(x[0] for x in cert['issuer'])
            issued_by = issuer['commonName']

            if issued_by.split(" ")[0] in truseted_ca:
                return 0
            else:
                return 1
        except:
            return 1
            # print(f"DOMAIN {domain['domain_name']} ERROR")

    # 14.Survival time of domain: The difference between termination time and creation time (Domain_Age)  
    @staticmethod
    def domain_lifespan(domain_name):
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date

        if isinstance(creation_date, list):
            creation_date= creation_date[-1]
        if isinstance(expiration_date, list):
            expiration_date= expiration_date[-1]

        if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
            try:
                creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
            except:
                return 1
        if ((expiration_date is None) or (creation_date is None)):
            return 1
        elif ((type(expiration_date) is list) or (type(creation_date) is list)):
            return 1
        else:
            ageofdomain = abs((expiration_date - creation_date).days)
            # print("Domain Age: ", ageofdomain)
            if ((ageofdomain/30) < 6):
                age = 1
            else:
                age = 0
        return age

    # 15.End time of domain: The difference between termination time and current time (Domain_End) 
    @staticmethod
    def domainEnd(domain_name):
        expiration_date = domain_name.expiration_date

        if isinstance(expiration_date, list):
            expiration_date= expiration_date[-1]

        if isinstance(expiration_date,str):
            try:
                expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
            except:
                return 1
        if (expiration_date is None):
            return 1
        elif (type(expiration_date) is list):
            return 1
        else:
            today = datetime.now()
            end = abs((expiration_date - today).days)
            if ((end/30) < 6):
                end = 1
            else:
                end = 0
            return end  

    # 16.
    @staticmethod
    def same_asn(domain_name):
        try:
            _asn = []
            for record in dns.resolver.resolve(domain_name["domain_name"], 'MX'):
                mx = record.to_text().split(" ")[1]
                _asn.append(socket.gethostbyname(mx))
            
            if len(_asn) == 1 and ocket.gethostbyname(_asn[0]) == socket.gethostbyname(domain_name):
                return 1 
            else :
                return 0
        except:
            return 1

    # reject (too slow)
    @staticmethod
    def top_n_google(domain, stop=30):
        google_search = [j for j in search(domain, tld="co.in", num=10, stop=stop, pause=2)]
        if domain not in google_search:
            return 1
        else:
            return 0

    # 17. IFrame Redirection (iFrame)
    @staticmethod
    def iframe(response):
        if response == "":
            return 1
        else:
            if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                return 0
            else:
                return 1

    # 18.Checks the effect of mouse over on status bar (Mouse_Over)
    @staticmethod
    def mouseOver(response): 
        if response == "" :
            return 1
        else:
            if re.findall("<script>.+onmouseover.+</script>", response.text):
                return 1
            else:
                return 0
    
    # 19.Checks the status of the right click attribute (Right_Click)
    @staticmethod
    def rightClick(response):
        if response == "":
            return 1
        else:
            if re.findall(r"event.button ?== ?2", response.text):
                return 0
            else:
                return 1

    # 21       
    @staticmethod
    def js_eval(response):      
        try:      
            if response == "":
                return 1
            else:
                return response.count("eval")
        except:
            return 0

    # 22
    @staticmethod
    def js_unescape(response):
        try:
            if response == "":
                return 1
            else:
                return response.count("unescape")
        except:
            return 0

    # 23
    @staticmethod
    def js_escape(response):
        try:
            if response == "":
                return 1
            else:
                return response.count("escape")
        except:
            return 0

    # 24
    @staticmethod
    def js_Active(response):
        try:
            if response == "":
                return 1
            else:
                return response.count("ActiveXObject")
        except:
            return 0

    # 25
    @staticmethod
    def js_charcode(response):
        try:
            if response == "":
                return 1
            else:
                return response.count("fromCharCode")
        except:
            return 0

    # 26
    @staticmethod
    def js_atob(response):
        try:
            if response == "":
                return 1
            else:
                return response.count("atob")
        except:
            return 0

    # 27.Punny code 
    @staticmethod
    def punnycode(url):

        vaild_regex = "/^(http|https|ftp):\/\/([A-Z0-9][A-Z0-9_-]*(?:\.[A-Z0-9][A-Z0-9_-]*)+):?(\d+)?\/?/i"
        if re.match(vaild_regex,url):
            punny = 1 
        else:
            punny = 0

        return punny

    @staticmethod
    def extract_title(response):
        try:
            if response == "":
                return "No Title"
            else:
                match_title = re.search("<title.*?>(.*?)</title>", response.text)
                if match_title is not None:
                    title = match_title.group(1)
                    return title
                else:
                    return "No Title"
        except:
            return "No Title"
    #Function to extract features
    def __call__(self, url, max_retries=2):
        if isinstance(url, str):
            features = []
            try:
                response = requests.get(url, headers=headers, timeout=3)
                if response.status_code not in range(400,600):
                    url = url.rstrip()

                    features.append(self.special_char(url))
                    features.append(self.havingIP(url))
                    features.append(self.haveAtSign(url))
                    features.append(self.getLength(url))
                    features.append(self.getDepth(url))
                    features.append(self.redirection(url))
                    features.append(self.forwarding(response))
                    features.append(self.port_in_url(url))
                    features.append(self.notsafe_protocol(url))
                    features.append(self.httpDomain(url))
                    features.append(self.tinyURL(url))
                    features.append(self.prefixSuffix(url))
                    
                    #Domain based features (4)
                    dns = 0
                    try:
                        domain_name = whois.whois(urlparse(url).netloc)
                    except:
                        dns = 1

                    features.append(dns)
                    features.append(1 if dns == 1 else self.trusted_ca(domain_name))
                    features.append(1 if dns == 1 else self.domain_lifespan(domain_name))
                    features.append(1 if dns == 1 else self.domainEnd(domain_name))
                    features.append(1 if dns == 1 else self.same_asn(domain_name))
                    # features.append(1 if dns == 1 else self.top_n_google(domain_name))
                    
                    #HTML & Javascript based features

                    features.append(self.iframe(response))
                    features.append(self.mouseOver(response))
                    features.append(self.rightClick(response))
                    features.append(self.js_eval(response))
                    features.append(self.js_unescape(response))
                    features.append(self.js_escape(response))
                    features.append(self.js_Active(response))
                    features.append(self.js_charcode(response))
                    features.append(self.js_atob(response))

                    features.append(self.punnycode(url))

                    # Data for Dashboard plotting
                    features.append(urlparse(url).netloc.split(".")[-1])
                    features.append(self.extract_title(response))
                    features.append("None" if dns == 1 else domain_name.country)

                    return features
                else:
                    return []
            except Exception as e: 
                return []
        else:
            return []


if __name__ == "__main__":
    ext = Extractor()
    vector = ext("https://stackoverflow.com/questions/42179046/what-flavor-of-regex-does-visual-studio-code-use")
    print(vector)
    # Vector = ext("http://msmcomun662.000webhostapp.com/login3.php")
    # print(len(Vector))
