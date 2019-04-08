

from pygeoip import GeoIP
import re
from xml.dom import minidom
import urllib.request
from urllib.parse import urlparse

notFound = -1
urlOpener = urllib.request.build_opener()
REACH = 'REACH'
RANK = 'RANK'
COUNTRY = 'COUNTRY'
sec = 'secure'
confirm = 'confirm'
login = 'login'
signin = 'signin'
account = 'account'
banking = 'banking'


# Tokenize the URL
def url_tokenizer(website):
    if website == '':
        return [0, 0, 0]
    word_token = re.split('\W+', website)

    no_of_element = sum_of_length = largest_value = 0
    for element in word_token:
        length = len(element)
        sum_of_length += length
        if length > 0:
            no_of_element += 1
        if largest_value < length:
            largest_value = length
    try:
        return [float(sum_of_length) / no_of_element, no_of_element, largest_value]
    except:
        return [0, no_of_element, largest_value]


def find_element_attributes(documentObject, element, feature):
    for subele in documentObject.getElementsByTagName(element):
        if subele.hasAttribute(feature):
            return subele.attributes[feature].value
    return notFound


# Method is use to check the popularity of the website
def website_popularity(hostName):
    xml_path = 'http://data.alexa.com/data?cli=12&dat=snbamz&url=' + hostName

    try:
        xml_object = urllib.request.urlopen(xml_path)
        documentObject = minidom.parse(xml_object)
        hostRank = find_element_attributes(documentObject, REACH, RANK)

        countryRank = find_element_attributes(documentObject, COUNTRY, RANK)
        return [hostRank, countryRank]

    except:
        return [notFound, notFound]


# This method is used whether URL contains EXE.
def find_exe(website):
    if website.find('.exe') != -1:
        return 1
    return 0


# This method is used whether URL contains the IP Address instead of HostName
def IPExist(words):
    count = 0;
    for element in words:
        if str(element).isnumeric():
            count += 1
        else:
            if count >= 4:
                return 1
            else:
                count = 0;
    if count >= 4:
        return 1
    return 0


def getAutonomous_system_number(hostName):
    try:
        geo_ip = GeoIP('GeoIPASNum.dat')
        autonomous_number = int(geo_ip.org_by_name(hostName).split()[0][2:])
        return autonomous_number
    except:
        return notFound


# This method is used to fetch the features from Source code.
def source_code_features(website):
    sourceFeatures = {}
    total_count = 0
    try:
        #  sourceCode = str(urlOpener.open(website))
        sourceCode = urllib.request.urlopen(website).read().decode('utf-8')

        sourceFeatures['source_underescape_count'] = sourceCode.count('underescape(', 0, len(sourceCode))
        sourceFeatures['source_html_count'] = sourceCode.count('<html', 0, len(sourceCode))
        sourceFeatures['source_search_count'] = sourceCode.count('search(', 0, len(sourceCode))
        sourceFeatures['source_iframe_count'] = sourceCode.count('<iframe', 0, len(sourceCode))
        sourceFeatures['source_hlink_count'] = sourceCode.count('<a href=', 0, len(sourceCode))
        sourceFeatures['source_escape_count'] = sourceCode.count('escape(', 0, len(sourceCode))
        sourceFeatures['source_eval_count'] = sourceCode.count('eval(', 0, len(sourceCode))

        sourceFeatures['source_exec_count'] = sourceCode.count('exec(', 0, len(sourceCode))
        sourceFeatures['source_link_count'] = sourceCode.count('link(', 0, len(sourceCode))

        for keyFeature in list(sourceFeatures):
            if (
                    keyFeature != 'source_html_count' and keyFeature != 'source_hlink_count' and keyFeature != 'source_iframe_count'):
                total_count += sourceFeatures[keyFeature]
                sourceFeatures['source_total_javascriptfun_count'] = total_count

    except Exception as e:
        print("Error in downloading page " + website)
        defaultVale = notFound

        sourceFeatures['source_iframe_count'] = defaultVale
        sourceFeatures['source_eval_count'] = defaultVale
        sourceFeatures['source_html_count'] = defaultVale
        sourceFeatures['source_underescape_count'] = defaultVale
        sourceFeatures['source_hlink_count'] = defaultVale

        sourceFeatures['source_exec_count'] = defaultVale
        sourceFeatures['source_search_count'] = defaultVale
        sourceFeatures['source_total_javascriptfun_count'] = defaultVale

        sourceFeatures['source_escape_count'] = defaultVale
        sourceFeatures['source_link_count'] = defaultVale

    return sourceFeatures


# This method is use whether the URL contains any sensitive words associated.
def sensitive_words(words):
    sensitiveWords = [sec, confirm, login, signin, account, banking]
    count = 0
    for element in sensitiveWords:
        if (element in words):
            count += 1;

    return count


# This method is used to check the Safe Browsing.
def safe_browsing(website):
    api = "BNBNJOKKVGYNKJDNKJSNKMDSJNDMKSNDJSDNDM"
    version = "1.0"
    urlCheck = "URL_check"

    request = {}
    request["client"] = urlCheck
    request["pver"] = "3.0"
    request["apikey"] = api
    request["url"] = website
    request["appver"] = version

    try:
        parameters = urllib.urlencode(request)
        requestUrl = "https://sb-ssl.google.com/safebrowsing/api/lookup?" + parameters
        response = urllib.request.urlopen(requestUrl)

        if response.code == 204:

            return 0
        elif response.code == 200:

            return 1
        elif response.code == 204:
            print(
                "URL is safe")
        elif response.code == 400:
            print(
                "Bad URL")
        elif response.code == 401:
            print(
                "API key is not authorized")
        else:
            print(
                "Service is not available")
    except:
        return -1


def featureExtraction(url):
    urlFeatures = {}
    words = re.split('\W+', url)

    object = urlparse(url)
    urlPath = object.path
    hostName = object.netloc

    urlFeatures['IPAddressExist'] = IPExist(words)
    urlFeatures['URLLength'] = len(url)

    urlFeatures['SensitiveWordCount'] = sensitive_words(words)
    urlFeatures['hostRank'], urlFeatures['rank_country'] = website_popularity(hostName)
    urlFeatures['AverageTokenLength'], urlFeatures['TokenCount'], urlFeatures['LargestToken'] = url_tokenizer(url)
    urlFeatures['SafeBrowsing'] = safe_browsing(url)

    urlFeatures['urlPath'] = object.path
    urlFeatures['Website'] = url


    urlFeatures['HostLength'] = len(hostName)
    urlFeatures['Numberofdots'] = url.count('.')

    urlFeatures['AveragePathToken'], urlFeatures['PathTokenCount'], urlFeatures['LargestPath'] = url_tokenizer(urlPath)
    urlFeatures['hostName'] = object.netloc


    urlFeatures['AverageDomainTokenLength'], urlFeatures['DomainTokenCount'], urlFeatures[
        'LargestDomain'] = url_tokenizer(hostName)

    # urlFeatures['EXE_IN_URL']=find_exe(url)
    urlFeatures['ASNNumber'] = getAutonomous_system_number(hostName)

    # urlFeatures=source_code_features(url)

    for key in urlFeatures:
        urlFeatures[key] = urlFeatures[key]

    return urlFeatures


if __name__ == '__main__':

    domain = "https://www.theunitedcargo.com"
    # url_tokenizer(domain)

    print(url_tokenizer(domain))

    print('Popularity: ' + str(website_popularity(domain)))

    print('Exe file: ' + str(find_exe(domain)))

    ip = IPExist('101.236.566.2553')

    if ip == 1:
        print("yes")
    else:
        print('No')

    asn = getAutonomous_system_number(domain)
    print(asn)
    feat = source_code_features(domain)
    print(feat)

    # ext = featureExtraction(domain)
    print(featureExtraction(domain))
