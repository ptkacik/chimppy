import requests
from . exceptions import (
    NoDeserializerFound,
    OutputFormatIsNotSupported
)
from . deserializers import (
    JSONChimppyDeserializer,
    XMLChimpyDeserializer,
    PHPChimpyDeserializer
)

class Chimppy(object):
    """Wrapper for v2.0 API MailChimp.

    ``apikey``
    Your API key for MailChimp account

    ``datacenter``
    All MailChimp API endpoints are datacenter specific. 

    ``format``
    MailChimp API support three output formats
         - json (default)
         - xml
         - php
    """

    SUPPORTED_FORMATS = ("json", "xml", "php")

    json_deserializer = JSONChimppyDeserializer()
    xml_deserializer = XMLChimpyDeserializer()
    php_deserializer = PHPChimpyDeserializer()

    def __init__(self, apikey, datacenter=None, timeout=None, format=None):
        #https://<dc>.api.mailchimp.com/2.0/, <dc> datacenter
        self.base_url = "https://%s.api.mailchimp.com/2.0/"
        self.apikey = apikey
        self.endpoint = self._create_endpoint(datacenter)
        self.format = format
        self.timeout = timeout

    def api(self, url, timeout=None, **params):
        params["apikey"] = self.apikey
        _url = self._build_url(url)
        headers = {'content-type': 'application/json'}
        response = requests.post(
            _url,
            params=params,
            timeout=timeout or self.timeout,
            headers=headers
        )
        deserialized_resopnse = self._deserialize_response(response.text, url)
        return deserialized_resopnse

    def _deserialize_response(self, response_text, url):
        """Deserialize response
        """
        format = self.format or "json"

        if "." in url:
            format = url.split(".")[-1]
        if format not in self.SUPPORTED_FORMATS:
            raise OutputFormatIsNotSupported("Format '%s' is not supported" % format)

        deserializer = getattr(self, "%s_deserializer" % format, None)
        if deserializer is None:
            raise NoDeserializerFound("No deserializer found for format: %s" % format)

        return deserializer.deserialize(response_text)

    def _create_endpoint(self, datacenter):
        """Create API endpoint
        """
        dc = datacenter or self.apikey.split("-")[-1]
        return self.base_url % dc

    def _build_url(self, url):
        return self.endpoint + url
