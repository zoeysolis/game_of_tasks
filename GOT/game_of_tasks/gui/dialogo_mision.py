import wx
import wx.adv

class DialogoNuevaMision(wx.Dialog):
    def __init__(self, parent):
        # Tamaño copado para que no se corten los elementos ni los botones - z
        super().__init__(parent, title="Nueva Misión", size=(350, 420))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- Nombre de la misión ---
        sizer.Add(wx.StaticText(panel, label="Nombre de la misión:"), 0, wx.ALL, 5)
        self.txt_nombre = wx.TextCtrl(panel)
        sizer.Add(self.txt_nombre, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Fecha límite - lo cambiamos a self.fecha_picker para evitar el AttributeError 
        sizer.Add(wx.StaticText(panel, label="Fecha límite:"), 0, wx.ALL, 5)
        self.fecha_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN)
        sizer.Add(self.fecha_picker, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        #  Hora límite 
        sizer.Add(wx.StaticText(panel, label="Hora límite:"), 0, wx.ALL, 5)
        self.time_picker = wx.adv.TimePickerCtrl(panel)
        sizer.Add(self.time_picker, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        #  Dificultad de la aventura 
        sizer.Add(wx.StaticText(panel, label="Dificultad de la aventura:"), 0, wx.ALL, 5)
        opciones_dificultad = ["Fácil", "Media", "Difícil"]
        self.combo_dificultad = wx.ComboBox(panel, choices=opciones_dificultad, style=wx.CB_READONLY)
        self.combo_dificultad.SetSelection(1)  # "Media" por defecto pero es muy libre todo
        sizer.Add(self.combo_dificultad, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Recompensa (XP) 
        sizer.Add(wx.StaticText(panel, label="Recompensa (XP):"), 0, wx.ALL, 5)
        self.spin_xp = wx.SpinCtrl(panel, value="50", min=10, max=500)
        sizer.Add(self.spin_xp, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Espacio para empujar los botones abajo
        sizer.AddStretchSpacer()
        
        # Botones de la ventana 
        botones_sizer = wx.StdDialogButtonSizer()
        btn_aceptar = wx.Button(panel, wx.ID_OK)
        btn_cancelar = wx.Button(panel, wx.ID_CANCEL)
        
        botones_sizer.AddButton(btn_aceptar)
        botones_sizer.AddButton(btn_cancelar)
        botones_sizer.Realize()
        
        sizer.Add(botones_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)
        panel.SetSizer(sizer)

    def obtener_datos(self):
        """Devuelve de forma limpia los 4 valores requeridos por la ventana principal."""
        nombre = self.txt_nombre.GetValue()
        
        # Procesamos la fecha de wxWidgets a formato texto YYYY-MM-DD
        wx_date = self.fecha_picker.GetValue()
        fecha_str = f"{wx_date.GetYear()}-{wx_date.GetMonth()+1:02d}-{wx_date.GetDay():02d}"
        
        # Procesamos la hora de wxWidgets a formato texto HH:MM:SS
        wx_time = self.time_picker.GetValue()
        hora_str = f"{wx_time.GetHour():02d}:{wx_time.GetMinute():02d}:{wx_time.GetSecond():02d}"
        
        # Unimos ambas en la cadena completa
        fecha_completa = f"{fecha_str} {hora_str}"
        
        xp = self.spin_xp.GetValue()
        dificultad = self.combo_dificultad.GetStringSelection()
        
        return nombre, fecha_completa, xp, dificultad
    
    def on_guardar_proceso_local(self, event):
        """Abre un diálogo nativo para guardar el historial en un archivo .txt"""
        dialogo_guardar = wx.FileDialog(
            self, 
            message="Guardar historial de misiones como...",
            defaultDir="", 
            defaultFile="historial_misiones.txt",
            wildcard="Archivos de texto (*.txt)|*.txt",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dialogo_guardar.ShowModal() == wx.ID_OK:
            ruta_seleccionada = dialogo_guardar.GetPath()
            
            # objeto de base de datos
            exito = self.db.exportar_misiones_a_texto(ruta_seleccionada)
            
            if exito:
                wx.MessageBox("¡Tu progreso e historial de misiones se guardaron con éxito!", 
                              "Progreso Guardado", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Hubo un error al intentar escribir el archivo.", 
                              "Error", wx.OK | wx.ICON_ERROR)
                
        dialogo_guardar.Destroy()