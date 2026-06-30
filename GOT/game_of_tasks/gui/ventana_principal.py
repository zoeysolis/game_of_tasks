import os
import wx
from gui.dialogo_mision import DialogoNuevaMision
from gui.calendario_panel import CalendarioPanel


class VentanaPrincipal(wx.Frame):
    def __init__(self, parent, title, db):
        super().__init__(parent, title=title, size=(1000, 600))
        self.db = db

        # =========================
        #  MENÚ
        # =========================
        menu_bar = wx.MenuBar()

        menu_ayuda = wx.Menu()
        menu_config = wx.Menu()

        item_creditos = menu_ayuda.Append(wx.ID_ABOUT, "Acerca de / Créditos")
        self.Bind(wx.EVT_MENU, self.mostrar_creditos, item_creditos)

        item_perfil = menu_config.Append(wx.ID_ANY, "Perfil")
        item_avatar = menu_config.Append(wx.ID_ANY, "Cambiar avatar")
        menu_config.AppendSeparator()
        item_salir = menu_config.Append(wx.ID_EXIT, "Salir")

        self.Bind(wx.EVT_MENU, self.abrir_perfil, item_perfil)
        self.Bind(wx.EVT_MENU, self.cambiar_avatar, item_avatar)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), item_salir)

        menu_bar.Append(menu_ayuda, "Ayuda")
        menu_bar.Append(menu_config, "Configuración")
        self.SetMenuBar(menu_bar)

        # =========================
        #  LAYOUT
        # =========================
        panel_principal = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # =========================
        #  PERFIL
        # =========================
        panel_perfil = wx.Panel(panel_principal, size=(200, -1), style=wx.BORDER_SUNKEN)
        sizer_perfil = wx.BoxSizer(wx.VERTICAL)

        sizer_perfil.Add(wx.StaticText(panel_perfil, label="PERFIL"), 0, wx.ALL | wx.ALIGN_CENTER, 10)

        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_avatar = os.path.join(carpeta_actual, "img", "avatar.png")

        if os.path.exists(ruta_avatar):
            imagen = wx.Image(ruta_avatar)
            imagen = imagen.Scale(150, 150)
            self.avatar = wx.StaticBitmap(panel_perfil, bitmap=wx.Bitmap(imagen))
        else:
            self.avatar = wx.StaticText(panel_perfil, label="Sin avatar")

        sizer_perfil.Add(self.avatar, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        self.barra_xp = wx.Gauge(panel_perfil, range=100, size=(160, 15))
        self.barra_xp.SetValue(35)
        sizer_perfil.Add(self.barra_xp, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        panel_perfil.SetSizer(sizer_perfil)

        # =========================
        # CENTRO
        # =========================
        panel_centro = wx.Panel(panel_principal)
        sizer_centro = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(panel_centro)

        self.panel_activas = wx.Panel(self.notebook)
        self.panel_completadas = wx.Panel(self.notebook)
        self.panel_futuras = wx.Panel(self.notebook)

        self.notebook.AddPage(self.panel_activas, "Activas")
        self.notebook.AddPage(self.panel_completadas, "Completadas")
        self.notebook.AddPage(self.panel_futuras, "Futuras")

        self.lista_activas = self.crear_lista(self.panel_activas)
        self.lista_completadas = self.crear_lista(self.panel_completadas)
        self.lista_futuras = self.crear_lista(self.panel_futuras)

        sizer_centro.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        btn_agregar = wx.Button(panel_centro, label="Nueva misión")
        btn_agregar.Bind(wx.EVT_BUTTON, self.abrir_dialogo)

        btn_completar = wx.Button(panel_centro, label="Completar misión")
        btn_completar.Bind(wx.EVT_BUTTON, self.completar_mision)

        sizer_centro.Add(btn_agregar, 0, wx.EXPAND | wx.ALL, 5)
        sizer_centro.Add(btn_completar, 0, wx.EXPAND | wx.ALL, 5)

        panel_centro.SetSizer(sizer_centro)

        # =========================
        # DERECHA
        # =========================
        collapsible = wx.CollapsiblePane(panel_principal, label="Opciones")
        pane = collapsible.GetPane()
        sizer_pane = wx.BoxSizer(wx.VERTICAL)

        btn_backup = wx.Button(pane, label="Guardar backup")
        btn_backup.Bind(wx.EVT_BUTTON, self.guardar_backup)

        sizer_pane.Add(btn_backup, 0, wx.ALL, 5)

        self.calendario_panel = CalendarioPanel(pane)
        sizer_pane.Add(self.calendario_panel, 1, wx.EXPAND)

        pane.SetSizer(sizer_pane)

        # =========================
        # FINAL
        # =========================
        body_sizer.Add(panel_perfil, 0, wx.EXPAND | wx.ALL, 5)
        body_sizer.Add(panel_centro, 1, wx.EXPAND | wx.ALL, 5)
        body_sizer.Add(collapsible, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(body_sizer, 1, wx.EXPAND)
        panel_principal.SetSizer(main_sizer)

        self.actualizar_tablas()
        self.Show()

    # =========================
    # FUNCIONES
    # =========================

    def crear_lista(self, parent):
        lista = wx.ListCtrl(parent, style=wx.LC_REPORT)
        lista.InsertColumn(0, "Nombre", width=200)
        lista.InsertColumn(1, "Estado", width=100)
        lista.InsertColumn(2, "XP", width=80)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lista, 1, wx.EXPAND)
        parent.SetSizer(sizer)

        return lista

    def actualizar_tablas(self):
        misiones = self.db.obtener_todas()

        for lista in [self.lista_activas, self.lista_completadas, self.lista_futuras]:
            lista.DeleteAllItems()

        for m in misiones:
            nombre = str(m[1])
            xp = str(m[3])
            estado = str(m[4])

            if estado == "completada":
                lista = self.lista_completadas
            elif estado == "futura":
                lista = self.lista_futuras
            else:
                lista = self.lista_activas

            index = lista.InsertItem(lista.GetItemCount(), nombre)
            lista.SetItem(index, 1, estado)
            lista.SetItem(index, 2, xp)

    def abrir_dialogo(self, event):
        dlg = DialogoNuevaMision(self)
        if dlg.ShowModal() == wx.ID_OK:
            datos = dlg.obtener_datos()
            self.db.agregar_mision(*datos)
            self.actualizar_tablas()
        dlg.Destroy()

    def completar_mision(self, event):
        index = self.lista_activas.GetFirstSelected()

        if index == -1:
            wx.MessageBox("Seleccioná una misión", "Error")
            return

        nombre = self.lista_activas.GetItemText(index)

        self.db.marcar_completada(nombre)
        self.actualizar_tablas()

    def guardar_backup(self, event):
        with wx.FileDialog(self, "Guardar",
                           wildcard="TXT (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:

            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            path = dlg.GetPath()

            if not path.endswith(".txt"):
                path += ".txt"

            misiones = self.db.obtener_todas()

            with open(path, "w", encoding="utf-8") as f:
                for m in misiones:
                    f.write(f"{m}\n")

            wx.MessageBox("Guardado", "OK")

    def abrir_perfil(self, event):
        frame = wx.Frame(self, title="Perfil", size=(300, 250))
        panel = wx.Panel(frame)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(panel, label="Perfil del jugador"), 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(wx.StaticText(panel, label="Nivel: 1"), 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(panel, label="XP: 35"), 0, wx.ALL, 5)
 
        panel.SetSizer(sizer)
        frame.Show()


    def cambiar_avatar(self, event):
        with wx.FileDialog(self, "Seleccionar avatar",
                           wildcard="Imagen (*.png;*.jpg)|*.png;*.jpg",
                           style=wx.FD_OPEN) as dlg:

            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            ruta = dlg.GetPath()

            try:
                imagen = wx.Image(ruta, wx.BITMAP_TYPE_ANY)
                imagen = imagen.Scale(150, 150)
                self.avatar.SetBitmap(wx.Bitmap(imagen))

                wx.MessageBox("Avatar actualizado", "OK")

            except Exception as e:
                wx.MessageBox(str(e), "Error")


    def mostrar_creditos(self, event):
        """Muestra los créditos del equipo y una guía rápida de usuario :))"""
        guia_usuario = (
            "=========================================\n"
            "   MANUAL DE AVENTURERO - GAME OF TASKS  \n"
            "=========================================\n\n"
            "1. CÓMO AGREGAR UNA MISIÓN:\n"
            "   • Hacé clic en el botón 'NUEVA MISIÓN' abajo al centro.\n"
            "   • Completá el nombre, elegí la fecha/hora límite y la dificultad.\n"
            "   • Presioná 'Aceptar' y aparecerá en la pestaña 'Activas'.\n\n"
            "2. CÓMO COMPLETAR UNA MISIÓN:\n"
            "   • Seleccioná la misión haciendo clic sobre ella en la tabla.\n"
            "   • Presioná el botón 'COMPLETAR MISIÓN'.\n"
            "   • ¡Listo! Pasará automáticamente a la pestaña 'Completadas'.\n\n"
            "3. GUARDAR PROCESO LOCAL:\n"
            "   • En el panel derecho 'Logística', usá el botón para exportar\n"
            "     un archivo de texto (.txt) con todo tu historial de juego.\n\n"
            "=========================================\n"
            "   CRÉDITOS DEL PROYECTO\n"
            "=========================================\n"
            "• Desarrolladores: Zoe K. Solis & Lautaro G. Torres\n"
            "• Materia: Programación Orientada a Objetos\n"
            "• Profesor: Javier Castrillo\n"
            "• Institución: UNPi - 2026"
        )
        
        wx.MessageBox(guia_usuario, "Ayuda, Tutorial y Créditos", wx.OK | wx.ICON_INFORMATION)