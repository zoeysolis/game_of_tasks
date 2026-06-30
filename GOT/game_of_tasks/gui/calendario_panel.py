import wx
import wx.adv


class CalendarioPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.calendario = wx.adv.CalendarCtrl(
            self,
            style=(
                wx.adv.CAL_SHOW_HOLIDAYS
                | wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION
            )
        )

        self.calendario.Bind(
            wx.adv.EVT_CALENDAR_SEL_CHANGED,
            self.on_fecha_cambiada
        )

        sizer.Add(
            self.calendario,
            1,
            wx.EXPAND | wx.ALL,
            5
        )

        self.SetSizer(sizer)

    def on_fecha_cambiada(self, event):
        fecha = self.calendario.GetDate()

        print(
            fecha.Format("%d/%m/%Y")
        )