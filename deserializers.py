import json
from . exceptions import MailChimpException


class BaseChimppyDeserializer(object):
    """Base class for deserializion MailChimp response.
    MailChimp support three output formats, json(default), xml, php
    Each Deserializer must contains method for deserializion and method for
    checking if response is success or not
    """

    def _deserializer(self, response_text):
        """Deserialize response text
        """
        return NotImplementedError

    def _raise_for_error(self, deserialized_resopnse):
        """Checkig MailChimp error response.
        If response is error response raise MailChimpException
        """
        return NotImplementedError

    def deserialize(self, response_text):
        deserialized_resopnse = self._deserializer(response_text)
        self._raise_for_error(deserialized_resopnse)
        return deserialized_resopnse



class JSONChimppyDeserializer(BaseChimppyDeserializer):
    
    def _deserializer(self, response_text):
        print response_text
        return json.loads(response_text)

    def _raise_for_error(self, deserialized_resopnse):
        data = deserialized_resopnse
        if "error" in data and data.get("status", None) == "error":
            raise MailChimpException(
                code=data["code"],
                name=data["name"],
                error=data["error"]
            )
        return None


class XMLChimpyDeserializer(BaseChimppyDeserializer):
    pass


class PHPChimpyDeserializer(BaseChimppyDeserializer):
    pass
