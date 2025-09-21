#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connection Manager / Bağlantı Yöneticisi

Handles SSH/SFTP connections to Raspberry Pi devices.
Raspberry Pi cihazlarına SSH/SFTP bağlantılarını yönetir.

Author / Yazar: GitHub User
License / Lisans: MIT
"""

import paramiko
import socket
from typing import Optional, Callable, Tuple


class ConnectionManager:
    """SSH/SFTP connection management class / SSH/SFTP bağlantı yönetim sınıfı"""
    
    def __init__(self):
        """Initialize connection manager / Bağlantı yöneticisini başlat"""
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.sftp_client: Optional[paramiko.SFTPClient] = None
        self.current_connection: Optional[dict] = None
        self.is_connected = False
        
        # Callbacks for connection events / Bağlantı olayları için geri çağırma fonksiyonları
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        self.on_error_callback: Optional[Callable] = None
    
    def set_connection_callbacks(self, 
                                on_connect: Optional[Callable] = None,
                                on_disconnect: Optional[Callable] = None,
                                on_error: Optional[Callable] = None):
        """
        Set connection event callbacks / Bağlantı olay geri çağırma fonksiyonlarını ayarla
        
        Args:
            on_connect: Called when connection is established / Bağlantı kurulduğunda çağrılır
            on_disconnect: Called when connection is closed / Bağlantı kapandığında çağrılır
            on_error: Called when connection error occurs / Bağlantı hatası oluştuğunda çağrılır
        """
        self.on_connect_callback = on_connect
        self.on_disconnect_callback = on_disconnect
        self.on_error_callback = on_error
    
    def connect(self, ip: str, username: str, password: str, port: int = 22, timeout: int = 10) -> Tuple[bool, str]:
        """
        Establish SSH/SFTP connection / SSH/SFTP bağlantısı kur
        
        Args:
            ip: IP address / IP adresi
            username: Username / Kullanıcı adı
            password: Password / Şifre
            port: SSH port / SSH portu
            timeout: Connection timeout / Bağlantı zaman aşımı
            
        Returns:
            Tuple of (success, error_message) / (başarı, hata_mesajı) demeti
        """
        try:
            # Disconnect if already connected / Zaten bağlıysa bağlantıyı kes
            if self.is_connected:
                self.disconnect()
            
            # Create SSH client / SSH istemcisi oluştur
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to SSH server / SSH sunucusuna bağlan
            self.ssh_client.connect(
                hostname=ip,
                port=port,
                username=username,
                password=password,
                timeout=timeout
            )
            
            # Open SFTP session / SFTP oturumu aç
            self.sftp_client = self.ssh_client.open_sftp()
            
            # Optimize for large file transfers / Büyük dosya transferleri için optimize et
            self.sftp_client.MAX_REQUEST_SIZE = 32768 * 4  # 128KB
            self.sftp_client.MAX_PACKET_SIZE = 32768 * 4   # 128KB
            
            # Store connection info / Bağlantı bilgilerini sakla
            self.current_connection = {
                "ip": ip,
                "username": username,
                "port": port,
                "name": f"{username}@{ip}:{port}"
            }
            
            self.is_connected = True
            
            # Call connect callback / Bağlantı geri çağırma fonksiyonunu çağır
            if self.on_connect_callback:
                self.on_connect_callback()
            
            return True, ""
            
        except paramiko.AuthenticationException:
            error_msg = "Authentication failed / Kimlik doğrulama başarısız"
            if self.on_error_callback:
                self.on_error_callback(error_msg)
            return False, error_msg
            
        except paramiko.SSHException as e:
            error_msg = f"SSH error / SSH hatası: {str(e)}"
            if self.on_error_callback:
                self.on_error_callback(error_msg)
            return False, error_msg
            
        except socket.timeout:
            error_msg = "Connection timeout / Bağlantı zaman aşımı"
            if self.on_error_callback:
                self.on_error_callback(error_msg)
            return False, error_msg
            
        except socket.gaierror:
            error_msg = "Host not found / Sunucu bulunamadı"
            if self.on_error_callback:
                self.on_error_callback(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Connection error / Bağlantı hatası: {str(e)}"
            if self.on_error_callback:
                self.on_error_callback(error_msg)
            return False, error_msg
    
    def disconnect(self):
        """Close SSH/SFTP connection / SSH/SFTP bağlantısını kapat"""
        try:
            if self.sftp_client:
                self.sftp_client.close()
                self.sftp_client = None
            
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
            
            self.is_connected = False
            self.current_connection = None
            
            # Call disconnect callback / Bağlantı kesme geri çağırma fonksiyonunu çağır
            if self.on_disconnect_callback:
                self.on_disconnect_callback()
                
        except Exception as e:
            print(f"Disconnect error / Bağlantı kesme hatası: {e}")
    
    def is_connected_to_server(self) -> bool:
        """
        Check if connected to server / Sunucuya bağlı olup olmadığını kontrol et
        
        Returns:
            True if connected / Bağlı ise True
        """
        return self.is_connected and self.ssh_client and self.sftp_client
    
    def get_current_connection(self) -> Optional[dict]:
        """
        Get current connection info / Mevcut bağlantı bilgilerini al
        
        Returns:
            Current connection dictionary or None / Mevcut bağlantı sözlüğü veya None
        """
        return self.current_connection
    
    def get_sftp_client(self) -> Optional[paramiko.SFTPClient]:
        """
        Get SFTP client instance / SFTP istemci örneğini al
        
        Returns:
            SFTP client or None / SFTP istemci veya None
        """
        return self.sftp_client if self.is_connected else None
    
    def get_ssh_client(self) -> Optional[paramiko.SSHClient]:
        """
        Get SSH client instance / SSH istemci örneğini al
        
        Returns:
            SSH client or None / SSH istemci veya None
        """
        return self.ssh_client if self.is_connected else None
    
    def test_connection(self) -> bool:
        """
        Test if connection is still alive / Bağlantının hala aktif olup olmadığını test et
        
        Returns:
            True if connection is alive / Bağlantı aktif ise True
        """
        if not self.is_connected_to_server():
            return False
        
        try:
            # Try to get remote directory listing / Uzak dizin listesini almaya çalış
            self.sftp_client.listdir("/")
            return True
        except:
            # Connection is dead, disconnect / Bağlantı ölmüş, bağlantıyı kes
            self.disconnect()
            return False
    
    def get_remote_path(self) -> str:
        """
        Get default remote path / Varsayılan uzak yol
        
        Returns:
            Default remote path / Varsayılan uzak yol
        """
        if self.current_connection:
            username = self.current_connection.get("username", "pi")
            return f"/home/{username}"
        return "/home/pi"
