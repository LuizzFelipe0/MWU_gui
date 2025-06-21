from tkinter import ttk


class IdDropdownComponent(ttk.Combobox):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, state="readonly", *args, **kwargs)
        self._name_to_id_map = {}
        self._id_to_name_map = {}
        self.bind("<<ComboboxSelected>>", self._on_select)

    def set_options(self, options_map: dict):

        self._name_to_id_map = options_map
        self._id_to_name_map = {v: k for k, v in options_map.items()}

        display_names = list(options_map.keys())
        self["values"] = display_names

        if display_names:
            self.set_selected_name(display_names[0])
        else:
            self.set_selected_name("")
    def get_selected_id(self):

        selected_name = self.get()
        return self._name_to_id_map.get(selected_name)

    def set_selected_id(self, item_id: str):

        item_name = self._id_to_name_map.get(item_id)
        if item_name:
            self.set_selected_name(item_name)
        else:
            self.set_selected_name("")

    def set_selected_name(self, name: str):

        self.set(name)

    def _on_select(self, event=None):

        pass