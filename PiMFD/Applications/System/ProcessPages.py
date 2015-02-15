# coding=utf-8
from datetime import datetime

from PiMFD.Applications.System.ByteFormatting import format_size
from PiMFD.UI.Charts import BarChart
from PiMFD.UI.Panels import StackPanel


try:
    import psutil
except ImportError:
    psutil = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import TextMenuItem


__author__ = 'Matt Eland'


class ProcessDetailsPage(MFDPage):
    """
    :param controller: 
    :param application: 
    :param process: 
    :param auto_scroll:
    :type process: psutil.Process
    """

    def __init__(self, controller, application, process, auto_scroll=True):
        super(ProcessDetailsPage, self).__init__(controller, application, auto_scroll)

        self.process = process
        self.last_refresh = datetime.now()

        try:
            self.name = process.name()
        except:
            self.name = "Unknown Process"

        self.refresh_performance_counters()

    def render(self):
        return super(ProcessDetailsPage, self).render()

    def arrange(self):

        now = datetime.now()

        delta = now - self.last_refresh
        if delta.seconds >= 1:
            self.last_refresh = now
            self.refresh_performance_counters()

        return super(ProcessDetailsPage, self).arrange()

    def get_button_text(self):
        return "INFO"

    def refresh_performance_counters(self):

        self.panel.children = [self.get_header_label("{} (PID: {})".format(self.name, self.process.pid))]

        # Render CPU
        pct = self.process.cpu_percent()
        if not pct:
            pct = 0.0

        lbl_cpu = self.get_list_label("CPU:")
        lbl_cpu_pct = self.get_list_label("{} %".format(pct))
        chrt_cpu = BarChart(self.display, self, pct, width=25, height=lbl_cpu.font.size)
        pnl_cpu = StackPanel(self.display, self, is_horizontal=True)
        pnl_cpu.children = [lbl_cpu, chrt_cpu, lbl_cpu_pct]

        self.panel.children.append(pnl_cpu)

        # Render Memory
        mem = self.process.memory_info()
        if mem:
            pnl_mem = StackPanel(self.display, self)
            pnl_mem.children.append(self.get_label("Memory"))
            pnl_mem.children.append(self.get_list_label("Memory Usage: {}".format(format_size(mem.rss))))
            pnl_mem.children.append(self.get_list_label("Virtual Memory Size: {}".format(format_size(mem.vms))))
            self.panel.children.append(pnl_mem)

        # Render threads
        pnl_threads = StackPanel(self.display, self)
        try:
            threads = self.process.threads()
            pnl_threads.children = [self.get_label("Threads ({})".format(len(threads)))]

            for t in threads:
                lbl = self.get_list_label("{}: User: {}, SYS: {}".format(t.id, t.user_time, t.system_time))
                pnl_threads.children.append(lbl)

        except psutil.AccessDenied:
            pnl_threads.children = [self.get_label("Threads"), self.get_list_label("No Access")]

        self.panel.children.append(pnl_threads)


class ProcessPage(MFDPage):

    processes = None

    def __init__(self, controller, application, auto_scroll=True):
        super(ProcessPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self,):

        if not psutil:
            return

        self.processes = psutil.get_process_list()

        self.panel.children = [self.get_header_label('Processes ({})'.format(len(self.processes)))]

        is_first_control = True
        
        for p in self.processes:

            try:
                name = p.name()

            except psutil.AccessDenied:
                continue
                
            except psutil.NoSuchProcess:
                continue

            lbl = TextMenuItem(self.controller.display, self, "{}: {}".format(p.pid, name))
            lbl.font = self.display.fonts.list
            lbl.data_context = p

            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False

    def handle_control_state_changed(self, widget):

        process = widget.data_context

        if process:
            self.application.select_page(ProcessDetailsPage(self.controller, self.application, process))

        super(ProcessPage, self).handle_control_state_changed(widget)

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




