import tkinter as tk
import nfc
import ndef

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NFC Card Reader")
        self.geometry("300x150")
        self.card_type_label = tk.Label(self, text="Card Type:")
        self.card_type_label.pack()
        self.card_type_var = tk.StringVar()
        self.card_type = tk.Label(self, textvariable=self.card_type_var)
        self.card_type.pack()

        self.clf = nfc.ContactlessFrontend()
        self.clf.connect(rdwr={'on-connect': self.on_connect})

    def on_connect(self, tag):
        card_type_string = card_type(tag)
        self.card_type_var.set(card_type_string)

def card_type(tag):
    #Check if the card support ATS 
    if hasattr(tag, 'ats'):
        ats = tag.ats
        if ats[:2] == b'\x75\x77':
            return "Type B (ISO/IEC 14443-3B)"
        elif ats[:2] == b'\x77\x75':
            return "Type A (ISO/IEC 14443-3A)"
    #Check if the card support ATQA
    if hasattr(tag, 'atqa'):
        atqa = tag.atqa
        if atqa == b'\x04\x00':
            return "Type A (ISO/IEC 14443-3A)"
        elif atqa == b'\x02\x00':
            return "Type B (ISO/IEC 14443-3B)"
    #Check if the card support NDEF
    if hasattr(tag, 'ndef'):
        ndef_data = tag.ndef
        records = ndef.message_decoder(ndef_data)
        for record in records:
            if record.type == "urn:nfc:wkt:T":
                return "NDEF formatted card"
    return "unknown"

if __name__ == "__main__":
    app = App()
    app.mainloop()
