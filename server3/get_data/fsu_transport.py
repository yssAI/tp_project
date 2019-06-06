# -*- coding: UTF-8 -*-
from os import path
from zeep.transports import Transport


class FSUTransport(Transport):
    """Customer transport for FSU server"""
    def __init__(self, operation_timeout=600, session=None, path=None):
        Transport.__init__(self, cache=None, timeout=300, session=session,
                           operation_timeout=operation_timeout)
        if not path:
            # 默认路径为当前引用路径 /services
            self.path = '.'
        else:
            self.path = path

    def load(self, url):
        # print url, self.path
        # Custom URL overriding to local file storage
        if url and url == "http://schemas.xmlsoap.org/soap/encoding/":
            url = path.join(self.path, "schemas.xmlsoap.org.soap.encoding.xml")

        if url and url == "http://schemas.xmlsoap.org/wsdl/":
            url = path.join(self.path, "schemas.xmlsoap.org.wsdl.xml")

        if url and url == "http://schemas.xmlsoap.org/wsdl/soap/":
            url = path.join(self.path, "schemas.xmlsoap.org.wsdl.soap.xml")

        if url and url == "http://www.w3.org/2001/XMLSchema":
            url = path.join(self.path, "XMLSchema.dtd")

        # Call zeep.transports.Transport's load()
        return super(FSUTransport, self).load(url)
