import hashlib
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

# Приклад реальної бази (MD5 хеші тестових файлів)
SIGNATURES = {
    "44d88612fea8a8f36de82e1278abb02f": "EICAR-Test-File",
    "e3b0c44298fc1c149afbf4c8996fb924": "Empty-Malware-Example"
}


class MobileScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10)

        self.status = Label(text="Натисніть 'Сканувати Downloads'", size_hint_y=None, height=100)
        self.add_widget(self.status)

        self.scan_btn = Button(text="СКАНУВАТИ", size_hint_y=None, height=100, background_color=(0, 0.8, 0.4, 1))
        self.scan_btn.bind(on_release=self.start_scan)
        self.add_widget(self.scan_btn)

        self.results = Label(text="", halign="left", valign="top", text_size=(None, None))
        scroll = ScrollView()
        scroll.add_widget(self.results)
        self.add_widget(scroll)

    def start_scan(self, instance):
        # Визначаємо шлях до завантажень залежно від платформи
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            path = "/storage/emulated/0/Download"
        else:
            path = os.path.expanduser("~/Downloads")

        self.status.text = "Сканування..."
        found_threats = []

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    f_hash = self.get_hash(file_path)
                    if f_hash in SIGNATURES:
                        found_threats.append(f"{file}: {SIGNATURES[f_hash]}")
                except:
                    continue

        if found_threats:
            self.status.text = f"ЗНАЙДЕНО ЗАГРОЗ: {len(found_threats)}"
            self.status.color = (1, 0, 0, 1)
            self.results.text = "\n".join(found_threats)
        else:
            self.status.text = "Все чисто!"
            self.status.color = (0, 1, 0, 1)

    def get_hash(self, path):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()


class AntivirusApp(App):
    def build(self):
        return MobileScanner()


if __name__ == "__main__":
    AntivirusApp().run()
