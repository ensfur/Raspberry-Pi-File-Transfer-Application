#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi File Transfer Application
Raspberry Pi Dosya Transfer Uygulaması

A professional GUI application for secure file transfer between Windows PC and Raspberry Pi.
Windows PC ile Raspberry Pi arasında güvenli dosya transferi için profesyonel GUI uygulaması.

Features / Özellikler:
- SSH/SFTP secure file transfer / SSH/SFTP güvenli dosya transferi
- Two-panel interface (Local/Remote) / İki panel arayüz (Yerel/Uzak)
- File management operations / Dosya yönetim işlemleri
- Transfer progress tracking / Transfer ilerleme takibi
- Connection management / Bağlantı yönetimi
- Search functionality / Arama işlevselliği
- Transfer logging / Transfer günlüğü

Author / Yazar: ensfur
License / Lisans: MIT
"""

import tkinter as tk
from tkinter import messagebox

# Import our custom modules / Özel modüllerimizi içe aktar
from config_manager import ConfigManager
from connection_manager import ConnectionManager
from file_transfer import FileTransfer
from gui_components import FileTransferGUI


class FileTransferApp:
    """Main application class / Ana uygulama sınıfı"""
    
    def __init__(self, root):
        """
        Initialize the application / Uygulamayı başlat
        
        Args:
            root: Tkinter root window / Tkinter ana pencere
        """
        self.root = root
        self.root.title("Raspberry Pi File Transfer / Raspberry Pi Dosya Transfer")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Initialize managers / Yöneticileri başlat
        self.config_manager = ConfigManager()
        self.connection_manager = ConnectionManager()
        self.file_transfer = FileTransfer(self.connection_manager)
        
        # Initialize GUI / GUI'yi başlat
        self.gui = FileTransferGUI(
            self.root, 
            self.config_manager, 
            self.connection_manager, 
            self.file_transfer
        )
        
        # Setup callbacks / Geri çağırma fonksiyonlarını ayarla
        self._setup_callbacks()
        
        # Load last connection / Son bağlantıyı yükle
        self._load_last_connection()
    
    def _setup_callbacks(self):
        """Setup application callbacks / Uygulama geri çağırma fonksiyonlarını ayarla"""
        # Connection callbacks / Bağlantı geri çağırma fonksiyonları
        self.connection_manager.set_connection_callbacks(
            on_connect=self.gui.on_connection_success,
            on_disconnect=self.gui.on_connection_disconnect,
            on_error=self.gui.on_connection_error
        )
        
        # Transfer callbacks / Transfer geri çağırma fonksiyonları
        self.file_transfer.set_progress_callbacks(
            progress_cb=self.gui.update_progress,
            status_cb=self.gui.update_status,
            speed_cb=self.gui.update_speed,
            eta_cb=self.gui.update_eta
        )
    
    def _load_last_connection(self):
        """Load last used connection / Son kullanılan bağlantıyı yükle"""
        last_connection = self.config_manager.get_last_connection()
        if last_connection:
            # Set connection in GUI / Bağlantıyı GUI'de ayarla
            connection_info = self.config_manager.get_connection(last_connection)
            if connection_info:
                self.gui.connection_combo.set(last_connection)
                self.gui.ip_entry.insert(0, connection_info["ip"])
                self.gui.user_entry.insert(0, connection_info["user"])
                self.gui.port_entry.delete(0, tk.END)
                self.gui.port_entry.insert(0, str(connection_info["port"]))
    
    def run(self):
        """Start the application / Uygulamayı başlat"""
        try:
            # Start GUI main loop / GUI ana döngüsünü başlat
            self.gui.run()
        except Exception as e:
            messagebox.showerror("Application Error / Uygulama Hatası", 
                               f"Failed to start application / Uygulama başlatılamadı:\n{str(e)}")
    
    def cleanup(self):
        """Cleanup resources before exit / Çıkış öncesi kaynakları temizle"""
        try:
            # Disconnect from server / Sunucudan bağlantıyı kes
            if self.connection_manager.is_connected_to_server():
                self.connection_manager.disconnect()
            
            # Save configuration / Konfigürasyonu kaydet
            self.config_manager.save_config()
            
        except Exception as e:
            print(f"Cleanup error / Temizleme hatası: {e}")


def main():
    """Main entry point / Ana giriş noktası"""
    try:
        # Create main window / Ana pencereyi oluştur
        root = tk.Tk()
        
        # Create application instance / Uygulama örneğini oluştur
        app = FileTransferApp(root)
        
        # Handle application closing / Uygulama kapanma işlemi
        def on_closing():
            app.cleanup()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start application / Uygulamayı başlat
        app.run()
        
    except Exception as e:
        messagebox.showerror("Application Error / Uygulama Hatası", 
                           f"Failed to start application / Uygulama başlatılamadı:\n{str(e)}")


if __name__ == "__main__":
    main()
