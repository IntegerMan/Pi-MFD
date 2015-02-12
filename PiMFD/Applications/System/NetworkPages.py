# coding=utf-8
import psutil

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import MenuItem


__author__ = 'Matt Eland'


class NetworkPage(MFDPage):
    connections = None

    def __init__(self, controller, application, auto_scroll=True):
        super(NetworkPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self, ):

        try:
            self.connections = psutil.net_connections(kind='all')
        except psutil.AccessDenied:
            self.connections = None
            return

        self.panel.children.append(self.get_header_label('Connections ({})'.format(len(self.connections))))

        is_first_control = True

        for c in self.connections:

            file_descriptor = c.fd
            family = c.family
            conn_type = c.type
            local_address = c.laddr  # May be tuple or path
            remote_address = c.raddr  # May be tuple, path, or None
            status = c.status
            opener_pid = c.pid

            text = "{} ({}) - {} - {} {} PID:{} FD:{}".format(remote_address, local_address, status, conn_type, family,
                                                              opener_pid, file_descriptor)

            lbl = MenuItem(self.controller.display, self, text)
            lbl.data_context = c
            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False


    def arrange(self):
        return super(NetworkPage, self).arrange()

    def render(self):

        if not self.connections:
            self.center_text("ACCESS DENIED")

        return super(NetworkPage, self).render()


    def handle_reselected(self):
        self.refresh()
        super(NetworkPage, self).handle_reselected()

    def get_button_text(self):
        return "NET"




