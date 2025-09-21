#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Transfer Manager / Dosya Transfer Yöneticisi

Handles file transfer operations between local PC and remote Raspberry Pi.
Yerel PC ve uzak Raspberry Pi arasında dosya transfer işlemlerini yönetir.

Author / Yazar: ensfur
License / Lisans: MIT
"""

import os
import time
import threading
from typing import Optional, Callable, List, Tuple
from datetime import datetime


class FileTransfer:
    """File transfer management class / Dosya transfer yönetim sınıfı"""
    
    def __init__(self, connection_manager):
        """
        Initialize file transfer manager / Dosya transfer yöneticisini başlat
        
        Args:
            connection_manager: ConnectionManager instance / ConnectionManager örneği
        """
        self.connection_manager = connection_manager
        
        # Transfer state / Transfer durumu
        self.transfer_in_progress = False
        self.transfer_cancelled = False
        self.current_transfer_thread: Optional[threading.Thread] = None
        
        # Progress callbacks / İlerleme geri çağırma fonksiyonları
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.speed_callback: Optional[Callable] = None
        self.eta_callback: Optional[Callable] = None
        
        # Transfer log / Transfer günlüğü
        self.transfer_log: List[dict] = []
    
    def set_progress_callbacks(self,
                             progress_cb: Optional[Callable] = None,
                             status_cb: Optional[Callable] = None,
                             speed_cb: Optional[Callable] = None,
                             eta_cb: Optional[Callable] = None):
        """
        Set progress tracking callbacks / İlerleme takibi geri çağırma fonksiyonlarını ayarla
        
        Args:
            progress_cb: Progress percentage callback / İlerleme yüzdesi geri çağırma fonksiyonu
            status_cb: Status message callback / Durum mesajı geri çağırma fonksiyonu
            speed_cb: Transfer speed callback / Transfer hızı geri çağırma fonksiyonu
            eta_cb: Estimated time callback / Tahmini süre geri çağırma fonksiyonu
        """
        self.progress_callback = progress_cb
        self.status_callback = status_cb
        self.speed_callback = speed_cb
        self.eta_callback = eta_cb
    
    def is_transfer_in_progress(self) -> bool:
        """
        Check if transfer is in progress / Transfer devam edip etmediğini kontrol et
        
        Returns:
            True if transfer is in progress / Transfer devam ediyorsa True
        """
        return self.transfer_in_progress
    
    def cancel_transfer(self):
        """Cancel current transfer / Mevcut transferi iptal et"""
        self.transfer_cancelled = True
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        Upload single file / Tek dosya yükle
        
        Args:
            local_path: Local file path / Yerel dosya yolu
            remote_path: Remote file path / Uzak dosya yolu
            
        Returns:
            True if successful / Başarılı ise True
        """
        if not self.connection_manager.is_connected_to_server():
            return False
        
        sftp_client = self.connection_manager.get_sftp_client()
        if not sftp_client:
            return False
        
        try:
            file_size = os.path.getsize(local_path)
            uploaded = 0
            start_time = time.time()
            
            def callback(bytes_transferred):
                nonlocal uploaded
                if self.transfer_cancelled:
                    raise Exception("Transfer cancelled / Transfer iptal edildi")
                
                uploaded = bytes_transferred  # Paramiko gives total bytes / Paramiko toplam bayt sayısını verir
                
                if self.progress_callback:
                    progress = (uploaded / file_size) * 100
                    self.progress_callback(progress)
                
                # Calculate speed and ETA / Hız ve ETA hesapla
                elapsed = time.time() - start_time
                if elapsed > 0:
                    speed = uploaded / elapsed
                    speed_str = self.format_size(speed) + "/s"
                    
                    if self.speed_callback:
                        self.speed_callback(speed_str)
                    
                    if self.eta_callback:
                        eta = (file_size - uploaded) / speed if speed > 0 else 0
                        eta_str = f"ETA: {self.format_time(eta)}"
                        self.eta_callback(eta_str)
            
            # Upload with progress tracking / İlerleme takibi ile yükle
            try:
                sftp_client.put(local_path, remote_path, callback=callback, confirm=False)
            except Exception as e:
                # Fallback without callback if callback causes issues / Callback sorun çıkarırsa callback olmadan dene
                if "callback" in str(e).lower():
                    sftp_client.put(local_path, remote_path, confirm=False)
                    if self.progress_callback:
                        self.progress_callback(100)
                else:
                    raise e
            
            return True
            
        except Exception as e:
            print(f"Upload error / Yükleme hatası: {e}")
            return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """
        Download single file / Tek dosya indir
        
        Args:
            remote_path: Remote file path / Uzak dosya yolu
            local_path: Local file path / Yerel dosya yolu
            
        Returns:
            True if successful / Başarılı ise True
        """
        if not self.connection_manager.is_connected_to_server():
            return False
        
        sftp_client = self.connection_manager.get_sftp_client()
        if not sftp_client:
            return False
        
        try:
            file_size = sftp_client.stat(remote_path).st_size
            downloaded = 0
            start_time = time.time()
            
            def callback(bytes_transferred):
                nonlocal downloaded
                if self.transfer_cancelled:
                    raise Exception("Transfer cancelled / Transfer iptal edildi")
                
                downloaded = bytes_transferred  # Paramiko gives total bytes / Paramiko toplam bayt sayısını verir
                
                if self.progress_callback:
                    progress = (downloaded / file_size) * 100
                    self.progress_callback(progress)
                
                # Calculate speed and ETA / Hız ve ETA hesapla
                elapsed = time.time() - start_time
                if elapsed > 0:
                    speed = downloaded / elapsed
                    speed_str = self.format_size(speed) + "/s"
                    
                    if self.speed_callback:
                        self.speed_callback(speed_str)
                    
                    if self.eta_callback:
                        eta = (file_size - downloaded) / speed if speed > 0 else 0
                        eta_str = f"ETA: {self.format_time(eta)}"
                        self.eta_callback(eta_str)
            
            # Download with progress tracking / İlerleme takibi ile indir
            try:
                sftp_client.get(remote_path, local_path, callback=callback)
            except Exception as e:
                # Fallback without callback if callback causes issues / Callback sorun çıkarırsa callback olmadan dene
                if "callback" in str(e).lower():
                    sftp_client.get(remote_path, local_path)
                    if self.progress_callback:
                        self.progress_callback(100)
                else:
                    raise e
            
            return True
            
        except Exception as e:
            print(f"Download error / İndirme hatası: {e}")
            return False
    
    def upload_directory(self, local_path: str, remote_path: str) -> bool:
        """
        Upload directory recursively / Klasörü özyinelemeli yükle
        
        Args:
            local_path: Local directory path / Yerel klasör yolu
            remote_path: Remote directory path / Uzak klasör yolu
            
        Returns:
            True if successful / Başarılı ise True
        """
        if not self.connection_manager.is_connected_to_server():
            return False
        
        sftp_client = self.connection_manager.get_sftp_client()
        if not sftp_client:
            return False
        
        try:
            # Create remote directory / Uzak klasörü oluştur
            try:
                sftp_client.mkdir(remote_path)
            except:
                pass  # Directory already exists / Klasör zaten var
            
            # Upload files and subdirectories / Dosyaları ve alt klasörleri yükle
            for item in os.listdir(local_path):
                local_item_path = os.path.join(local_path, item)
                remote_item_path = os.path.join(remote_path, item).replace("\\", "/")
                
                if os.path.isdir(local_item_path):
                    self.upload_directory(local_item_path, remote_item_path)
                else:
                    self.upload_file(local_item_path, remote_item_path)
            
            return True
            
        except Exception as e:
            print(f"Directory upload error / Klasör yükleme hatası: {e}")
            return False
    
    def download_directory(self, remote_path: str, local_path: str) -> bool:
        """
        Download directory recursively / Klasörü özyinelemeli indir
        
        Args:
            remote_path: Remote directory path / Uzak klasör yolu
            local_path: Local directory path / Yerel klasör yolu
            
        Returns:
            True if successful / Başarılı ise True
        """
        if not self.connection_manager.is_connected_to_server():
            return False
        
        sftp_client = self.connection_manager.get_sftp_client()
        if not sftp_client:
            return False
        
        try:
            # Create local directory / Yerel klasörü oluştur
            os.makedirs(local_path, exist_ok=True)
            
            # Download files and subdirectories / Dosyaları ve alt klasörleri indir
            for item in sftp_client.listdir_attr(remote_path):
                remote_item_path = os.path.join(remote_path, item.filename).replace("\\", "/")
                local_item_path = os.path.join(local_path, item.filename)
                
                if self.is_directory(item.st_mode):
                    self.download_directory(remote_item_path, local_item_path)
                else:
                    self.download_file(remote_item_path, local_item_path)
            
            return True
            
        except Exception as e:
            print(f"Directory download error / Klasör indirme hatası: {e}")
            return False
    
    def transfer_files(self, file_list: List[Tuple[str, str]], direction: str) -> bool:
        """
        Transfer multiple files / Birden fazla dosya transfer et
        
        Args:
            file_list: List of (source, destination) tuples / (kaynak, hedef) demetlerinin listesi
            direction: 'upload' or 'download' / 'yükle' veya 'indir'
            
        Returns:
            True if all transfers successful / Tüm transferler başarılı ise True
        """
        if self.transfer_in_progress:
            return False
        
        def transfer_thread():
            try:
                self.transfer_in_progress = True
                self.transfer_cancelled = False
                
                total_files = len(file_list)
                
                for i, (source, destination) in enumerate(file_list):
                    if self.transfer_cancelled:
                        break
                    
                    if self.status_callback:
                        filename = os.path.basename(source)
                        status = f"Transferring ({i+1}/{total_files}): {filename}"
                        self.status_callback(status)
                    
                    start_time = time.time()
                    success = False
                    
                    try:
                        if direction == "upload":
                            if os.path.isdir(source):
                                success = self.upload_directory(source, destination)
                            else:
                                success = self.upload_file(source, destination)
                        else:  # download
                            success = self.download_file(source, destination)
                        
                        if success and not self.transfer_cancelled:
                            # Log transfer / Transferi kaydet
                            duration = time.time() - start_time
                            file_size = self.get_file_size(source, direction == "download")
                            self.log_transfer(direction, os.path.basename(source), file_size, duration)
                    
                    except Exception as e:
                        print(f"File transfer error / Dosya transfer hatası: {e}")
                    
                    # Update progress / İlerleme güncelle
                    if not self.transfer_cancelled:
                        progress = ((i + 1) / total_files) * 100
                        if self.progress_callback:
                            self.progress_callback(progress)
                
                if self.status_callback:
                    if self.transfer_cancelled:
                        self.status_callback("Transfer cancelled")
                    else:
                        self.status_callback("Transfer completed")
                
            except Exception as e:
                print(f"Transfer thread error / Transfer thread hatası: {e}")
            finally:
                self.transfer_in_progress = False
                self.transfer_cancelled = False
        
        self.current_transfer_thread = threading.Thread(target=transfer_thread, daemon=True)
        self.current_transfer_thread.start()
        return True
    
    def get_file_size(self, path: str, is_remote: bool = False) -> Optional[int]:
        """
        Get file size / Dosya boyutunu al
        
        Args:
            path: File path / Dosya yolu
            is_remote: True if remote file / Uzak dosya ise True
            
        Returns:
            File size in bytes or None / Bayt cinsinden dosya boyutu veya None
        """
        try:
            if is_remote:
                sftp_client = self.connection_manager.get_sftp_client()
                if sftp_client:
                    return sftp_client.stat(path).st_size
            else:
                return os.path.getsize(path)
        except:
            return None
    
    def is_directory(self, mode: int) -> bool:
        """
        Check if mode represents a directory / Mod'un klasör olup olmadığını kontrol et
        
        Args:
            mode: Unix file mode / Unix dosya modu
            
        Returns:
            True if directory / Klasör ise True
        """
        return (mode & 0o040000) != 0
    
    def format_size(self, size: float) -> str:
        """
        Format size in human readable format / Boyutu okunabilir formata çevir
        
        Args:
            size: Size in bytes / Bayt cinsinden boyut
            
        Returns:
            Formatted size string / Formatlanmış boyut dizisi
        """
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
    
    def format_time(self, seconds: float) -> str:
        """
        Format time in human readable format / Süreyi okunabilir formata çevir
        
        Args:
            seconds: Time in seconds / Saniye cinsinden süre
            
        Returns:
            Formatted time string / Formatlanmış süre dizisi
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds//60)}m {int(seconds%60)}s"
        else:
            return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m"
    
    def log_transfer(self, action: str, filename: str, size: Optional[int] = None, duration: Optional[float] = None):
        """
        Log transfer operation / Transfer işlemini kaydet
        
        Args:
            action: Transfer action / Transfer işlemi
            filename: File name / Dosya adı
            size: File size / Dosya boyutu
            duration: Transfer duration / Transfer süresi
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "filename": filename,
            "size": size,
            "duration": duration
        }
        self.transfer_log.append(log_entry)
        
        # Keep only last 100 entries / Sadece son 100 kaydı tut
        if len(self.transfer_log) > 100:
            self.transfer_log = self.transfer_log[-100:]
    
    def get_transfer_log(self) -> List[dict]:
        """
        Get transfer log / Transfer günlüğünü al
        
        Returns:
            List of transfer log entries / Transfer günlük kayıtlarının listesi
        """
        return self.transfer_log.copy()
    
    def clear_transfer_log(self):
        """Clear transfer log / Transfer günlüğünü temizle"""
        self.transfer_log.clear()
