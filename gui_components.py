#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Components / GUI Bileşenleri

Reusable GUI components and dialogs for the file transfer application.
Dosya transfer uygulaması için yeniden kullanılabilir GUI bileşenleri ve diyaloglar.

Author / Yazar: GitHub User
License / Lisans: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime


class FileTransferGUI:
    """Main GUI class for file transfer application / Dosya transfer uygulaması için ana GUI sınıfı"""
    
    def __init__(self, root, config_manager, connection_manager, file_transfer):
        """
        Initialize GUI / GUI'yi başlat
        
        Args:
            root: Tkinter root window / Tkinter ana pencere
            config_manager: ConfigManager instance / ConfigManager örneği
            connection_manager: ConnectionManager instance / ConnectionManager örneği
            file_transfer: FileTransfer instance / FileTransfer örneği
        """
        self.root = root
        self.config_manager = config_manager
        self.connection_manager = connection_manager
        self.file_transfer = file_transfer
        
        # File paths - Start from appropriate root for cross-platform usage
        if os.name == 'nt':  # Windows
            self.local_current_path = "C:\\"
        else:  # Linux/Unix
            self.local_current_path = "/"
        self.remote_current_path = "/"
        
        # GUI variables / GUI değişkenleri
        self.progress_var = tk.DoubleVar()
        
        # Setup UI / Arayüzü ayarla
        self.setup_ui()
        
        # Load initial data / Başlangıç verilerini yükle
        self.refresh_local_files()
        self.update_connection_combo()
    
    def setup_ui(self):
        """Setup user interface / Kullanıcı arayüzünü ayarla"""
        # Main frame / Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weights / Grid ağırlıkları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Create UI sections / UI bölümlerini oluştur
        self._create_connection_frame(main_frame)
        self._create_transfer_frame(main_frame)
        self._create_file_panels(main_frame)
        self._create_progress_frame(main_frame)
        self._create_control_frame(main_frame)
        
        # Keyboard shortcuts / Klavye kısayolları
        self._setup_keyboard_shortcuts()
    
    def _create_connection_frame(self, parent):
        """Create connection management frame / Bağlantı yönetim çerçevesini oluştur"""
        # Connection frame
        connection_frame = ttk.LabelFrame(parent, text="Connection Settings", padding="5")
        connection_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Connection fields
        ttk.Label(connection_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ip_entry = ttk.Entry(connection_frame, width=15)
        self.ip_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(connection_frame, text="Username:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.user_entry = ttk.Entry(connection_frame, width=10)
        self.user_entry.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(connection_frame, text="Password:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.password_entry = ttk.Entry(connection_frame, width=10, show="*")
        self.password_entry.grid(row=0, column=5, padx=(0, 10))
        
        ttk.Label(connection_frame, text="Port:").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(connection_frame, width=6)
        self.port_entry.insert(0, "22")
        self.port_entry.grid(row=0, column=7, padx=(0, 10))
        
        # Connection buttons
        self.connect_btn = ttk.Button(connection_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=0, column=8, padx=(5, 5))
        
        self.disconnect_btn = ttk.Button(connection_frame, text="Disconnect", 
                                       command=self.disconnect, state="disabled")
        self.disconnect_btn.grid(row=0, column=9, padx=(5, 5))
        
        self.save_btn = ttk.Button(connection_frame, text="Save", command=self.save_connection)
        self.save_btn.grid(row=0, column=10, padx=(5, 5))
        
        # Connection management
        ttk.Label(connection_frame, text="Saved Connections:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.connection_combo = ttk.Combobox(connection_frame, width=20, state="readonly")
        self.connection_combo.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10), pady=(5, 0))
        self.connection_combo.bind("<<ComboboxSelected>>", self.load_connection)
        
        self.load_btn = ttk.Button(connection_frame, text="Load", command=self.load_connection)
        self.load_btn.grid(row=1, column=3, padx=(5, 5), pady=(5, 0))
        
        self.delete_btn = ttk.Button(connection_frame, text="Delete", command=self.delete_connection)
        self.delete_btn.grid(row=1, column=4, padx=(5, 5), pady=(5, 0))
        
        # Connection status
        self.status_label = ttk.Label(connection_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=1, column=5, columnspan=3, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Quick connect buttons
        ttk.Button(connection_frame, text="Quick Connect (pi@192.168.1.100)", 
                  command=lambda: self.quick_connect("192.168.1.100", "pi", "22")).grid(row=1, column=8, padx=(5, 5), pady=(5, 0))
        ttk.Button(connection_frame, text="Quick Connect (pi@raspberrypi.local)", 
                  command=lambda: self.quick_connect("raspberrypi.local", "pi", "22")).grid(row=1, column=9, padx=(5, 5), pady=(5, 0))
    
    def _create_transfer_frame(self, parent):
        """Create transfer control frame / Transfer kontrol çerçevesini oluştur"""
        transfer_frame = ttk.Frame(parent)
        transfer_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        transfer_frame.columnconfigure(0, weight=1)
        transfer_frame.columnconfigure(1, weight=1)
        transfer_frame.columnconfigure(2, weight=1)
        transfer_frame.columnconfigure(3, weight=1)
        transfer_frame.columnconfigure(4, weight=1)
        
        # Transfer buttons
        self.transfer_to_remote_btn = ttk.Button(transfer_frame, text="→ Send to Raspberry Pi", 
                                               command=self.transfer_to_remote, state="disabled")
        self.transfer_to_remote_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        ttk.Button(transfer_frame, text="📁 Select All (Local)", 
                  command=self.select_all_local).grid(row=0, column=1, padx=(5, 5), sticky=(tk.W, tk.E))
        
        self.transfer_to_local_btn = ttk.Button(transfer_frame, text="← Download to PC", 
                                              command=self.transfer_to_local, state="disabled")
        self.transfer_to_local_btn.grid(row=0, column=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(transfer_frame, text="📁 Select All (Remote)", 
                  command=self.select_all_remote).grid(row=0, column=3, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Cancel transfer button
        self.cancel_transfer_btn = ttk.Button(transfer_frame, text="❌ Cancel Transfer", 
                                            command=self.cancel_transfer, state="disabled")
        self.cancel_transfer_btn.grid(row=0, column=4, padx=(10, 0), sticky=(tk.W, tk.E))
    
    def _create_file_panels(self, parent):
        """Create file browser panels / Dosya tarayıcı panellerini oluştur"""
        file_frame = ttk.Frame(parent)
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(2, weight=1)
        file_frame.rowconfigure(1, weight=1)
        
        # Local panel
        self._create_local_panel(file_frame)
        
        # Remote panel
        self._create_remote_panel(file_frame)
    
    def _create_local_panel(self, parent):
        """Create local file panel / Yerel dosya panelini oluştur"""
        local_frame = ttk.LabelFrame(parent, text="PC Files", padding="5")
        local_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        local_frame.columnconfigure(0, weight=1)
        local_frame.rowconfigure(1, weight=1)
        
        # Local navigation
        local_nav_frame = ttk.Frame(local_frame)
        local_nav_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        local_nav_frame.columnconfigure(1, weight=1)
        
        self.local_back_btn = ttk.Button(local_nav_frame, text="← Back", command=self.local_back)
        self.local_back_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.local_path_label = ttk.Label(local_nav_frame, text=self.local_current_path)
        self.local_path_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        
        self.local_up_btn = ttk.Button(local_nav_frame, text="↑ Up", command=self.local_up)
        self.local_up_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Local file list
        local_list_frame = ttk.Frame(local_frame)
        local_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        local_list_frame.columnconfigure(0, weight=1)
        local_list_frame.rowconfigure(0, weight=1)
        
        self.local_tree = ttk.Treeview(local_list_frame, columns=("size", "modified"), show="tree headings")
        self.local_tree.heading("#0", text="Name")
        self.local_tree.heading("size", text="Size")
        self.local_tree.heading("modified", text="Modified")
        self.local_tree.column("#0", width=300)
        self.local_tree.column("size", width=100)
        self.local_tree.column("modified", width=150)
        self.local_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        local_scrollbar = ttk.Scrollbar(local_list_frame, orient="vertical", command=self.local_tree.yview)
        local_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.local_tree.configure(yscrollcommand=local_scrollbar.set)
        
        self.local_tree.bind("<Double-1>", self.local_double_click)
        self.local_tree.bind("<Button-3>", self.local_right_click)
    
    def _create_remote_panel(self, parent):
        """Create remote file panel / Uzak dosya panelini oluştur"""
        remote_frame = ttk.LabelFrame(parent, text="Raspberry Pi Files", padding="5")
        remote_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        remote_frame.columnconfigure(0, weight=1)
        remote_frame.rowconfigure(1, weight=1)
        
        # Remote navigation
        remote_nav_frame = ttk.Frame(remote_frame)
        remote_nav_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        remote_nav_frame.columnconfigure(1, weight=1)
        
        self.remote_back_btn = ttk.Button(remote_nav_frame, text="← Back", command=self.remote_back, state="disabled")
        self.remote_back_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.remote_path_label = ttk.Label(remote_nav_frame, text=self.remote_current_path)
        self.remote_path_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        
        self.remote_up_btn = ttk.Button(remote_nav_frame, text="↑ Up", command=self.remote_up, state="disabled")
        self.remote_up_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Remote file list
        remote_list_frame = ttk.Frame(remote_frame)
        remote_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        remote_list_frame.columnconfigure(0, weight=1)
        remote_list_frame.rowconfigure(0, weight=1)
        
        self.remote_tree = ttk.Treeview(remote_list_frame, columns=("size", "modified"), show="tree headings")
        self.remote_tree.heading("#0", text="Name")
        self.remote_tree.heading("size", text="Size")
        self.remote_tree.heading("modified", text="Modified")
        self.remote_tree.column("#0", width=300)
        self.remote_tree.column("size", width=100)
        self.remote_tree.column("modified", width=150)
        self.remote_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        remote_scrollbar = ttk.Scrollbar(remote_list_frame, orient="vertical", command=self.remote_tree.yview)
        remote_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.remote_tree.configure(yscrollcommand=remote_scrollbar.set)
        
        self.remote_tree.bind("<Double-1>", self.remote_double_click)
        self.remote_tree.bind("<Button-3>", self.remote_right_click)
    
    def _create_progress_frame(self, parent):
        """Create progress tracking frame / İlerleme takip çerçevesini oluştur"""
        self.progress_frame = ttk.Frame(parent)
        self.progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        self.progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.grid(row=0, column=1)
        
        self.speed_label = ttk.Label(self.progress_frame, text="", foreground="blue")
        self.speed_label.grid(row=0, column=2, padx=(10, 0))
        
        self.time_label = ttk.Label(self.progress_frame, text="", foreground="green")
        self.time_label.grid(row=0, column=3, padx=(10, 0))
    
    def _create_control_frame(self, parent):
        """Create control buttons frame / Kontrol butonları çerçevesini oluştur"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Refresh buttons
        ttk.Button(control_frame, text="Refresh Local", command=self.refresh_local_files).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(control_frame, text="Refresh Remote", command=self.refresh_remote_files).grid(row=0, column=1, padx=(5, 0))
        
        # Folder creation buttons
        ttk.Button(control_frame, text="📁 Create Local Folder", command=self.create_local_folder).grid(row=0, column=2, padx=(10, 5))
        ttk.Button(control_frame, text="📁 Create Remote Folder", command=self.create_remote_folder).grid(row=0, column=3, padx=(5, 0))
        
        # Log button frame
        log_frame = ttk.Frame(parent)
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log button
        ttk.Button(log_frame, text="📋 Transfer Log", command=self.show_transfer_log).grid(row=0, column=0, padx=(0, 0))
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts / Klavye kısayollarını ayarla"""
        self.root.bind("<F5>", lambda e: self.refresh_local_files())
        self.root.bind("<Control-r>", lambda e: self.refresh_remote_files())
        self.root.bind("<Control-F5>", lambda e: self.refresh_remote_files())
    
    # Connection management methods / Bağlantı yönetim metodları
    def connect(self):
        """Establish connection / Bağlantı kur"""
        ip = self.ip_entry.get().strip()
        user = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not all([ip, user, password, port]):
            messagebox.showerror("Error", "Fill all fields!")
            return
        
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number!")
            return
        
        # Connect in separate thread / Ayrı thread'de bağlan
        def connect_thread():
            try:
                self.connect_btn.config(state="disabled")
                self.status_label.config(text="Connecting...", foreground="orange")
                self.root.update()
                
                success, error_msg = self.connection_manager.connect(ip, user, password, port)
                
                if success:
                    # Save last connection / Son bağlantıyı kaydet
                    connection_name = f"{user}@{ip}:{port}"
                    self.config_manager.set_last_connection(connection_name)
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, lambda: self.on_connection_error(error_msg))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_connection_error(str(e)))
        
        import threading
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect(self):
        """Close connection / Bağlantıyı kapat"""
        self.connection_manager.disconnect()
    
    def on_connection_success(self):
        """Handle successful connection / Başarılı bağlantıyı işle"""
        self.status_label.config(text="Connected", foreground="green")
        self.connect_btn.config(state="disabled")
        self.disconnect_btn.config(state="normal")
        self.remote_back_btn.config(state="normal")
        self.remote_up_btn.config(state="normal")
        self.transfer_to_remote_btn.config(state="normal")
        self.transfer_to_local_btn.config(state="normal")
        self.refresh_remote_files()
    
    def on_connection_disconnect(self):
        """Handle connection disconnect / Bağlantı kesintisini işle"""
        self.status_label.config(text="Disconnected", foreground="red")
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.remote_back_btn.config(state="disabled")
        self.remote_up_btn.config(state="disabled")
        self.transfer_to_remote_btn.config(state="disabled")
        self.transfer_to_local_btn.config(state="disabled")
        
        # Clear remote file list / Remote dosya listesini temizle
        for item in self.remote_tree.get_children():
            self.remote_tree.delete(item)
    
    def on_connection_error(self, error_msg):
        """Handle connection error / Bağlantı hatasını işle"""
        self.status_label.config(text="Connection Error", foreground="red")
        self.connect_btn.config(state="normal")
        messagebox.showerror("Connection Error", f"Connection failed:\n{error_msg}")
    
    # Progress callback methods / İlerleme geri çağırma metodları
    def update_progress(self, progress: float):
        """Update progress bar / İlerleme çubuğunu güncelle"""
        self.progress_var.set(progress)
    
    def update_status(self, status: str):
        """Update status label / Durum etiketini güncelle"""
        self.progress_label.config(text=status)
    
    def update_speed(self, speed: str):
        """Update speed label / Hız etiketini güncelle"""
        self.speed_label.config(text=speed)
    
    def update_eta(self, eta: str):
        """Update ETA label / ETA etiketini güncelle"""
        self.time_label.config(text=eta)
    
    # Placeholder methods for functionality / İşlevsellik için yer tutucu metodlar
    def save_connection(self):
        """Save connection profile"""
        ip = self.ip_entry.get().strip()
        user = self.user_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not all([ip, user, port]):
            messagebox.showerror("Error", "Fill IP, username and port fields!")
            return
        
        try:
            port = int(port)
            name = f"{user}@{ip}:{port}"
            self.config_manager.add_connection(name, ip, user, port)
            self.update_connection_combo()
            messagebox.showinfo("Success", "Connection saved!")
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number!")
    
    def load_connection(self, event=None):
        """Load connection profile"""
        selected = self.connection_combo.get()
        if not selected:
            return
        
        connection = self.config_manager.get_connection(selected)
        if connection:
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, connection["ip"])
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, connection["user"])
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, str(connection["port"]))
            self.password_entry.delete(0, tk.END)
    
    def delete_connection(self):
        """Delete connection profile"""
        selected = self.connection_combo.get()
        if not selected:
            messagebox.showwarning("Warning", "Select connection to delete!")
            return
        
        if messagebox.askyesno("Confirm", f"Delete connection '{selected}'?"):
            self.config_manager.remove_connection(selected)
            self.update_connection_combo()
            messagebox.showinfo("Success", "Connection deleted!")
    
    def quick_connect(self, ip, user, port):
        """Quick connect with predefined settings"""
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, ip)
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, user)
        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(0, port)
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()
    
    def update_connection_combo(self):
        """Update connection combo box"""
        connections = self.config_manager.get_connection_names()
        self.connection_combo["values"] = connections
        
        # Select last connection
        last_connection = self.config_manager.get_last_connection()
        if last_connection and last_connection in connections:
            self.connection_combo.set(last_connection)
    
    def refresh_local_files(self):
        """Refresh local file list"""
        # Clear current items
        for item in self.local_tree.get_children():
            self.local_tree.delete(item)
        
        try:
            # Add folders and files
            items = []
            for item in os.listdir(self.local_current_path):
                item_path = os.path.join(self.local_current_path, item)
                if os.path.isdir(item_path):
                    items.append((item, "Folder", "", True))
                else:
                    size = os.path.getsize(item_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(item_path))
                    items.append((item, self.format_size(size), modified.strftime("%Y-%m-%d %H:%M"), False))
            
            # Sort (folders first, then files)
            items.sort(key=lambda x: (not x[3], x[0].lower()))
            
            for name, size, modified, is_dir in items:
                icon = "📁" if is_dir else "📄"
                item_id = self.local_tree.insert("", "end", text=f"{icon} {name}", values=(size, modified))
                if is_dir:
                    self.local_tree.set(item_id, "size", "Folder")
            
        except PermissionError:
            messagebox.showerror("Error", f"No permission to access '{self.local_current_path}'!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading local files: {e}")
        
        self.local_path_label.config(text=self.local_current_path)
    
    def format_size(self, size: float) -> str:
        """Format size in human readable format"""
        if size == 0:
            return "0 B"
        elif size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size/1024:.1f} KB"
        elif size < 1024**3:
            return f"{size/(1024**2):.1f} MB"
        else:
            return f"{size/(1024**3):.1f} GB"
    
    def refresh_remote_files(self):
        """Refresh remote file list"""
        if not self.connection_manager.is_connected_to_server():
            return
        
        sftp_client = self.connection_manager.get_sftp_client()
        if not sftp_client:
            return
        
        # Clear current items
        for item in self.remote_tree.get_children():
            self.remote_tree.delete(item)
        
        try:
            # Add remote files and folders
            items = []
            for item in sftp_client.listdir_attr(self.remote_current_path):
                if item.st_mode is not None:
                    if self.is_directory(item.st_mode):
                        items.append((item.filename, "Folder", "", True))
                    else:
                        size = item.st_size if item.st_size is not None else 0
                        modified = datetime.fromtimestamp(item.st_mtime) if item.st_mtime else datetime.now()
                        items.append((item.filename, self.format_size(size), modified.strftime("%Y-%m-%d %H:%M"), False))
            
            # Sort (folders first, then files)
            items.sort(key=lambda x: (not x[3], x[0].lower()))
            
            for name, size, modified, is_dir in items:
                icon = "📁" if is_dir else "📄"
                item_id = self.remote_tree.insert("", "end", text=f"{icon} {name}", values=(size, modified))
                if is_dir:
                    self.remote_tree.set(item_id, "size", "Folder")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading remote files: {e}")
        
        self.remote_path_label.config(text=self.remote_current_path)
    
    def is_directory(self, mode: int) -> bool:
        """Check if mode represents a directory"""
        return (mode & 0o040000) != 0
    
    def local_double_click(self, event):
        """Handle local file double click"""
        selection = self.local_tree.selection()
        if selection:
            item = self.local_tree.item(selection[0])
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            
            path = os.path.join(self.local_current_path, name)
            if os.path.isdir(path):
                self.local_current_path = path
                self.refresh_local_files()
    
    def remote_double_click(self, event):
        """Handle remote file double click"""
        if not self.connection_manager.is_connected_to_server():
            return
        
        selection = self.remote_tree.selection()
        if selection:
            item = self.remote_tree.item(selection[0])
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            
            remote_path = os.path.join(self.remote_current_path, name).replace("\\", "/")
            
            try:
                # Check if it's a directory
                sftp_client = self.connection_manager.get_sftp_client()
                stat = sftp_client.stat(remote_path)
                if self.is_directory(stat.st_mode):
                    self.remote_current_path = remote_path
                    self.refresh_remote_files()
            except:
                pass
    
    def local_right_click(self, event):
        """Handle local file right click"""
        selection = self.local_tree.selection()
        if selection:
            item = self.local_tree.item(selection[0])
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            
            local_path = os.path.join(self.local_current_path, name)
            
            # Context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Transfer to Remote", command=self.transfer_to_remote)
            context_menu.add_separator()
            context_menu.add_command(label="Rename", command=lambda: self.rename_local_file(local_path))
            context_menu.add_command(label="Delete", command=lambda: self.delete_local_file(local_path))
            context_menu.add_separator()
            context_menu.add_command(label="File Info", command=lambda: messagebox.showinfo("File Info", f"File: {name}\nPath: {local_path}"))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def remote_right_click(self, event):
        """Handle remote file right click"""
        if not self.connection_manager.is_connected_to_server():
            return
        
        selection = self.remote_tree.selection()
        if selection:
            item = self.remote_tree.item(selection[0])
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            
            remote_path = os.path.join(self.remote_current_path, name).replace("\\", "/")
            
            # Context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Download to PC", command=self.transfer_to_local)
            context_menu.add_separator()
            context_menu.add_command(label="Rename", command=lambda: self.rename_remote_file(remote_path))
            context_menu.add_command(label="Delete", command=lambda: self.delete_remote_file(remote_path))
            context_menu.add_separator()
            context_menu.add_command(label="File Info", command=lambda: messagebox.showinfo("File Info", f"File: {name}\nPath: {remote_path}"))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def local_back(self):
        """Navigate back in local directory"""
        if self.local_current_path != os.path.dirname(self.local_current_path):
            self.local_current_path = os.path.dirname(self.local_current_path)
            self.refresh_local_files()
    
    def local_up(self):
        """Navigate up in local directory"""
        parent = os.path.dirname(self.local_current_path)
        if parent != self.local_current_path:
            self.local_current_path = parent
            self.refresh_local_files()
    
    def remote_back(self):
        """Navigate back in remote directory"""
        if self.remote_current_path != "/" and self.remote_current_path != "":
            self.remote_current_path = os.path.dirname(self.remote_current_path) or "/"
            self.refresh_remote_files()
    
    def remote_up(self):
        """Navigate up in remote directory"""
        if self.remote_current_path != "/":
            self.remote_current_path = os.path.dirname(self.remote_current_path) or "/"
            self.refresh_remote_files()
    
    def select_all_local(self):
        """Select all local files"""
        for item_id in self.local_tree.get_children():
            self.local_tree.selection_add(item_id)
    
    def select_all_remote(self):
        """Select all remote files"""
        for item_id in self.remote_tree.get_children():
            self.remote_tree.selection_add(item_id)
    
    def transfer_to_remote(self):
        """Transfer files to remote"""
        if not self.connection_manager.is_connected_to_server():
            messagebox.showerror("Error", "No connection!")
            return
        
        selection = self.local_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select files to transfer!")
            return
        
        # Get selected files
        selected_files = []
        for item_id in selection:
            item = self.local_tree.item(item_id)
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            local_path = os.path.join(self.local_current_path, name)
            selected_files.append((local_path, os.path.join(self.remote_current_path, name).replace("\\", "/")))
        
        if selected_files:
            self.file_transfer.transfer_files(selected_files, "upload")
    
    def transfer_to_local(self):
        """Transfer files to local"""
        if not self.connection_manager.is_connected_to_server():
            messagebox.showerror("Error", "No connection!")
            return
        
        selection = self.remote_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select files to transfer!")
            return
        
        # Get selected files
        selected_files = []
        for item_id in selection:
            item = self.remote_tree.item(item_id)
            name = item["text"].replace("📁 ", "").replace("📄 ", "")
            if name.startswith("📁"):
                name = name[2:]
            remote_path = os.path.join(self.remote_current_path, name).replace("\\", "/")
            selected_files.append((remote_path, os.path.join(self.local_current_path, name)))
        
        if selected_files:
            self.file_transfer.transfer_files(selected_files, "download")
    
    def cancel_transfer(self):
        """Cancel current transfer"""
        self.file_transfer.cancel_transfer()
    
    def create_local_folder(self):
        """Create local folder"""
        folder_name = simpledialog.askstring("Create Folder", "Folder name:")
        if folder_name:
            try:
                folder_path = os.path.join(self.local_current_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                self.refresh_local_files()
                messagebox.showinfo("Success", f"Folder '{folder_name}' created.")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating folder: {e}")
    
    def create_remote_folder(self):
        """Create remote folder"""
        if not self.connection_manager.is_connected_to_server():
            messagebox.showerror("Error", "No connection!")
            return
        
        folder_name = simpledialog.askstring("Create Folder", "Folder name:")
        if folder_name:
            try:
                sftp_client = self.connection_manager.get_sftp_client()
                folder_path = os.path.join(self.remote_current_path, folder_name).replace("\\", "/")
                sftp_client.mkdir(folder_path)
                self.refresh_remote_files()
                messagebox.showinfo("Success", f"Folder '{folder_name}' created.")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating folder: {e}")
    
    
    def show_transfer_log(self):
        """Show transfer log"""
        log = self.file_transfer.get_transfer_log()
        if not log:
            messagebox.showinfo("Transfer Log", "No transfers recorded.")
            return
        
        # Simple log display
        log_text = "Transfer Log:\n\n"
        for entry in log[-10:]:  # Show last 10 entries
            log_text += f"{entry['timestamp']} - {entry['action']}: {entry['filename']}\n"
        
        messagebox.showinfo("Transfer Log", log_text)
    
    def rename_local_file(self, file_path):
        """Rename local file/folder"""
        old_name = os.path.basename(file_path)
        
        # Preserve file extension
        if os.path.isfile(file_path):
            name_part, ext_part = os.path.splitext(old_name)
            initial_value = name_part
        else:
            initial_value = old_name
        
        new_name = simpledialog.askstring("Rename", f"New name:", initialvalue=initial_value)
        
        if new_name and new_name != initial_value:
            try:
                # Add extension if it's a file
                if os.path.isfile(file_path):
                    name_part, ext_part = os.path.splitext(old_name)
                    if not new_name.endswith(ext_part):
                        new_name = new_name + ext_part
                
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                self.refresh_local_files()
                messagebox.showinfo("Success", f"'{old_name}' renamed to '{new_name}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Rename error: {e}")
    
    def rename_remote_file(self, file_path):
        """Rename remote file/folder"""
        if not self.connection_manager.is_connected_to_server():
            messagebox.showerror("Error", "No connection!")
            return
        
        old_name = os.path.basename(file_path)
        
        # Preserve file extension
        try:
            sftp_client = self.connection_manager.get_sftp_client()
            stat = sftp_client.stat(file_path)
            if not self.is_directory(stat.st_mode):  # If it's a file
                name_part, ext_part = os.path.splitext(old_name)
                initial_value = name_part
            else:  # If it's a folder
                initial_value = old_name
        except:
            initial_value = old_name
        
        new_name = simpledialog.askstring("Rename", f"New name:", initialvalue=initial_value)
        
        if new_name and new_name != initial_value:
            try:
                # Add extension if it's a file
                try:
                    sftp_client = self.connection_manager.get_sftp_client()
                    stat = sftp_client.stat(file_path)
                    if not self.is_directory(stat.st_mode):  # If it's a file
                        name_part, ext_part = os.path.splitext(old_name)
                        if not new_name.endswith(ext_part):
                            new_name = new_name + ext_part
                except:
                    pass
                
                new_path = os.path.join(os.path.dirname(file_path), new_name).replace("\\", "/")
                sftp_client.rename(file_path, new_path)
                self.refresh_remote_files()
                messagebox.showinfo("Success", f"'{old_name}' renamed to '{new_name}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Rename error: {e}")
    
    def delete_local_file(self, file_path):
        """Delete local file/folder"""
        name = os.path.basename(file_path)
        confirm_msg = f"Delete '{name}'?\nThis action cannot be undone!"
        
        if messagebox.askyesno("Confirm Delete", confirm_msg):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                self.refresh_local_files()
                messagebox.showinfo("Success", f"'{name}' deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Delete error: {e}")
    
    def delete_remote_file(self, file_path):
        """Delete remote file/folder"""
        if not self.connection_manager.is_connected_to_server():
            messagebox.showerror("Error", "No connection!")
            return
        
        name = os.path.basename(file_path)
        confirm_msg = f"Delete '{name}'?\nThis action cannot be undone!"
        
        if messagebox.askyesno("Confirm Delete", confirm_msg):
            try:
                sftp_client = self.connection_manager.get_sftp_client()
                stat = sftp_client.stat(file_path)
                if self.is_directory(stat.st_mode):
                    # Delete directory recursively
                    self._delete_remote_directory(sftp_client, file_path)
                else:
                    sftp_client.remove(file_path)
                self.refresh_remote_files()
                messagebox.showinfo("Success", f"'{name}' deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Delete error: {e}")
    
    def _delete_remote_directory(self, sftp_client, dir_path):
        """Recursively delete remote directory"""
        for item in sftp_client.listdir(dir_path):
            item_path = os.path.join(dir_path, item).replace("\\", "/")
            stat = sftp_client.stat(item_path)
            if self.is_directory(stat.st_mode):
                self._delete_remote_directory(sftp_client, item_path)
            else:
                sftp_client.remove(item_path)
        sftp_client.rmdir(dir_path)
    
    def run(self):
        """Start GUI main loop"""
        self.root.mainloop()
