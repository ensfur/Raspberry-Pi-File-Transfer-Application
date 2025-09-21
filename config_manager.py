#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager / Konfigürasyon Yöneticisi

Handles application configuration including connection profiles and settings.
Uygulama konfigürasyonunu yönetir, bağlantı profilleri ve ayarları içerir.

Author / Yazar: ensfur
License / Lisans: MIT
"""

import json
import os
from typing import Dict, List, Optional, Any


class ConfigManager:
    """Configuration management class / Konfigürasyon yönetim sınıfı"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration manager / Konfigürasyon yöneticisini başlat
        
        Args:
            config_file: Path to configuration file / Konfigürasyon dosyası yolu
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file / Dosyadan konfigürasyonu yükle
        
        Returns:
            Configuration dictionary / Konfigürasyon sözlüğü
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._create_default_config()
        except Exception as e:
            print(f"Config loading error / Konfigürasyon yükleme hatası: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """
        Create default configuration / Varsayılan konfigürasyon oluştur
        
        Returns:
            Default configuration dictionary / Varsayılan konfigürasyon sözlüğü
        """
        return {
            "connections": [],
            "last_connection": None,
            "settings": {
                "default_remote_path": "/home/pi",
                "auto_save_connections": True,
                "show_hidden_files": False,
                "transfer_timeout": 300
            }
        }
    
    def save_config(self) -> bool:
        """
        Save configuration to file / Konfigürasyonu dosyaya kaydet
        
        Returns:
            True if successful, False otherwise / Başarılı ise True, aksi halde False
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Config saving error / Konfigürasyon kaydetme hatası: {e}")
            return False
    
    def get_connections(self) -> List[Dict[str, Any]]:
        """
        Get all saved connections / Kayıtlı tüm bağlantıları al
        
        Returns:
            List of connection dictionaries / Bağlantı sözlüklerinin listesi
        """
        return self.config.get("connections", [])
    
    def add_connection(self, name: str, ip: str, user: str, port: int) -> bool:
        """
        Add or update a connection profile / Bağlantı profili ekle veya güncelle
        
        Args:
            name: Connection name / Bağlantı adı
            ip: IP address / IP adresi
            user: Username / Kullanıcı adı
            port: Port number / Port numarası
            
        Returns:
            True if successful / Başarılı ise True
        """
        try:
            connection = {
                "name": name,
                "ip": ip,
                "user": user,
                "port": port
            }
            
            # Check if connection already exists / Bağlantı zaten var mı kontrol et
            connections = self.config.get("connections", [])
            for i, conn in enumerate(connections):
                if conn["name"] == name:
                    connections[i] = connection
                    break
            else:
                connections.append(connection)
            
            self.config["connections"] = connections
            return self.save_config()
        except Exception as e:
            print(f"Add connection error / Bağlantı ekleme hatası: {e}")
            return False
    
    def remove_connection(self, name: str) -> bool:
        """
        Remove a connection profile / Bağlantı profili sil
        
        Args:
            name: Connection name to remove / Silinecek bağlantı adı
            
        Returns:
            True if successful / Başarılı ise True
        """
        try:
            connections = self.config.get("connections", [])
            self.config["connections"] = [conn for conn in connections if conn["name"] != name]
            return self.save_config()
        except Exception as e:
            print(f"Remove connection error / Bağlantı silme hatası: {e}")
            return False
    
    def get_connection(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get connection by name / Ada göre bağlantı al
        
        Args:
            name: Connection name / Bağlantı adı
            
        Returns:
            Connection dictionary or None / Bağlantı sözlüğü veya None
        """
        connections = self.config.get("connections", [])
        for conn in connections:
            if conn["name"] == name:
                return conn
        return None
    
    def set_last_connection(self, name: str) -> bool:
        """
        Set last used connection / Son kullanılan bağlantıyı ayarla
        
        Args:
            name: Connection name / Bağlantı adı
            
        Returns:
            True if successful / Başarılı ise True
        """
        try:
            self.config["last_connection"] = name
            return self.save_config()
        except Exception as e:
            print(f"Set last connection error / Son bağlantı ayarlama hatası: {e}")
            return False
    
    def get_last_connection(self) -> Optional[str]:
        """
        Get last used connection / Son kullanılan bağlantıyı al
        
        Returns:
            Last connection name or None / Son bağlantı adı veya None
        """
        return self.config.get("last_connection")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration setting / Konfigürasyon ayarı al
        
        Args:
            key: Setting key / Ayar anahtarı
            default: Default value / Varsayılan değer
            
        Returns:
            Setting value / Ayar değeri
        """
        settings = self.config.get("settings", {})
        return settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """
        Set a configuration setting / Konfigürasyon ayarı ayarla
        
        Args:
            key: Setting key / Ayar anahtarı
            value: Setting value / Ayar değeri
            
        Returns:
            True if successful / Başarılı ise True
        """
        try:
            if "settings" not in self.config:
                self.config["settings"] = {}
            self.config["settings"][key] = value
            return self.save_config()
        except Exception as e:
            print(f"Set setting error / Ayar ayarlama hatası: {e}")
            return False
    
    def get_connection_names(self) -> List[str]:
        """
        Get list of connection names / Bağlantı adlarının listesini al
        
        Returns:
            List of connection names / Bağlantı adlarının listesi
        """
        connections = self.config.get("connections", [])
        return [conn["name"] for conn in connections]
