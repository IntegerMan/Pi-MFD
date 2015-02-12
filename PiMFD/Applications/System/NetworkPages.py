# coding=utf-8
from _socket import SOCK_STREAM, SOCK_DGRAM, SOCK_RAW, SOCK_RDM, SOCK_SEQPACKET, AF_INET, AF_INET6, AF_APPLETALK, \
    AF_DECnet, AF_IPX, AF_IRDA, AF_SNA, AF_UNSPEC

try:
    import psutil
except ImportError:
    psutil = None

try:
    from psutil._common import AF_UNIX
except ImportError:
    AF_UNIX = 1

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import MenuItem


"""
Contains code related to network monitoring. Note that code here can be OS sensitive.
"""

__author__ = 'Matt Eland'


class NetworkPage(MFDPage):
    """
    A page containing network connection information
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type auto_scroll: bool
    """
    connections = None

    def __init__(self, controller, application, auto_scroll=True):
        super(NetworkPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self, ):

        if not psutil:
            return

        try:
            self.connections = psutil.net_connections(kind='all')
        except psutil.AccessDenied:
            self.connections = None
            return

        self.panel.children.append(self.get_header_label('Connections ({})'.format(len(self.connections))))

        is_first_control = True

        for c in self.connections:

            family = self.get_connection_family_text(c.family)
            conn_type = self.get_connection_type_text(c.type)
            local_address = self.get_address_text(c.laddr)  # May be tuple or path
            remote_address = self.get_address_text(c.raddr)  # May be tuple, path, or None
            status = c.status
            pid = self.get_process_text(c.pid)

            if local_address == remote_address:                
                address_text = remote_address
            else:
                address_text = "{}({})".format(remote_address, local_address)
                
            text = "{} {} {}/{} {}".format(status, address_text, conn_type, family, pid)

            lbl = MenuItem(self.controller.display, self, text)
            lbl.font = self.controller.display.fonts.list
            lbl.data_context = c
            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False

    @staticmethod
    def get_address_text(address):
        """
        Gets an address string from an address object
        :param address: The address object
        :return: Address string
        """
        if address is None:
            return ""
        
        if isinstance(address, tuple):
            if len(address) <= 0:
                return ""
            
            if len(address) >= 2:
                return "{}:{}".format(address[0], address[1])
        
        return str(address)

    @staticmethod
    def get_process_text(pid):
        """
        Gets process text from the specified PID string
        :param pid: The process identifier
        :return: Process text
        """
        if pid is None or pid <= 0:
            return ""

        return "- PID: {}".format(pid)

    @staticmethod
    def get_connection_family_text(family):
        """
        Gets a readible string from a connection family code
        :param family: The family code
        :return: Readible string
        """
        if family is None:
            return "UNK"
        
        if family == AF_INET:
            return "INET"
        elif family == AF_INET6:
            return "INET6"
        elif family == AF_UNIX:
            return "UNIX"
        elif family == AF_APPLETALK:
            return "Appletalk"
        elif family == AF_DECnet:
            return "DECnet"
        elif family == AF_IPX:
            return "IPX"
        elif family == AF_IRDA:
            return "IRDA"
        elif family == AF_SNA:
            return "SNA"
        elif family == AF_UNSPEC:
            return "UNSPEC"
        
        return "UNK:" + str(family)
    
    @staticmethod
    def get_connection_type_text(conn_type):
        """
        Gets a connection type string a connection code
        :param conn_type: The connection type
        :return: The connection type
        """
        
        if conn_type is None:
            return "None"

        if conn_type == SOCK_STREAM:
            return "Stream"
        elif conn_type == SOCK_DGRAM:
            return "Datagram"
        elif conn_type == SOCK_RAW:
            return "Raw"
        elif conn_type == SOCK_RDM:
            return "RDM"
        elif conn_type == SOCK_SEQPACKET:
            return "SEQ Packet"

        return "UNK: " + str(conn_type)

    def render(self):

        if not self.connections:
            self.center_text("ACCESS DENIED")

        return super(NetworkPage, self).render()

    def handle_reselected(self):
        self.refresh()
        super(NetworkPage, self).handle_reselected()

    def get_button_text(self):
        return "NTWK"




