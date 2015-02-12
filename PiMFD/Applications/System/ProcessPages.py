# coding=utf-8

try:
    import psutil
except ImportError:
    psutil = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import MenuItem


__author__ = 'Matt Eland'


class ProcessPage(MFDPage):

    processes = None

    def __init__(self, controller, application, auto_scroll=True):
        super(ProcessPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self,):

        if not psutil:
            return

        self.processes = psutil.get_process_list()

        self.panel.children.append(self.get_header_label('Processes ({})'.format(len(self.processes))))

        is_first_control = True
        
        for p in self.processes:

            try:
                name = p.name()

            except psutil.AccessDenied:
                continue
                
            except psutil.NoSuchProcess:
                continue

            lbl = MenuItem(self.controller.display, self, "{}: {}".format(p.pid, name))
            lbl.font = self.display.fonts.list
            lbl.data_context = p

            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False

    def arrange(self):
        return super(ProcessPage, self).arrange()

    def render(self):

        if not psutil:
            self.center_text("psutil offline".upper())

        return super(ProcessPage, self).render()

    def handle_reselected(self):
        self.refresh()
        super(ProcessPage, self).handle_reselected()

    def get_button_text(self):
        return "PROC"




