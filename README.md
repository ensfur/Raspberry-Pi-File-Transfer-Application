# Raspberry Pi File Transfer Application / Raspberry Pi Dosya Transfer Uygulaması

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()

A professional GUI application for secure file transfer between Windows PC and Raspberry Pi devices using SSH/SFTP protocol. Perfect for Raspberry Pi to Raspberry Pi transfers as well.

SSH/SFTP protokolü kullanarak Windows PC ve Raspberry Pi cihazları arasında güvenli dosya transferi için profesyonel GUI uygulaması. Raspberry Pi'dan Raspberry Pi'a transferler için de mükemmeldir.

---

## 🌟 Features / Özellikler

### 🔗 Connection Management / Bağlantı Yönetimi
- **Secure SSH/SFTP Connection**: Encrypted file transfer protocol / Güvenli SSH/SFTP Bağlantısı: Şifreli dosya transfer protokolü
- **Connection Profiles**: Save and load connection settings / Bağlantı Profilleri: Bağlantı ayarlarını kaydet ve yükle
- **Quick Connect**: Pre-configured buttons for common Raspberry Pi addresses / Hızlı Bağlantı: Yaygın Raspberry Pi adresleri için önceden yapılandırılmış butonlar
- **Connection Status**: Real-time connection status indicator / Bağlantı Durumu: Gerçek zamanlı bağlantı durumu göstergesi

### 📁 File Management / Dosya Yönetimi
- **Dual-Panel Interface**: Side-by-side local and remote file browsing / Çift Panel Arayüzü: Yan yana yerel ve uzak dosya tarama
- **File Operations**: Upload, download, rename, delete files and folders / Dosya İşlemleri: Yükle, indir, yeniden adlandır, dosya ve klasörleri sil
- **Bulk Operations**: Select and transfer multiple files simultaneously / Toplu İşlemler: Birden fazla dosyayı seç ve aynı anda transfer et
- **File Information**: Detailed file properties and metadata / Dosya Bilgileri: Detaylı dosya özellikleri ve metadata
- **Safe Deletion**: Confirm before deleting files and folders / Güvenli Silme: Dosya ve klasörleri silmeden önce onayla

### 🎯 User Experience / Kullanıcı Deneyimi
- **Auto-Save Settings**: Remember last connection automatically / Otomatik Ayar Kaydetme: Son bağlantıyı otomatik hatırla
- **Context Menus**: Right-click operations for quick access / Bağlam Menüleri: Hızlı erişim için sağ tıklama işlemleri
- **Error Handling**: User-friendly error messages and recovery / Hata Yönetimi: Kullanıcı dostu hata mesajları ve kurtarma
- **Cross-Platform**: Works on Windows and Linux systems / Çapraz Platform: Windows ve Linux sistemlerinde çalışır
- **Root Directory Start**: Perfect for Raspberry Pi to Raspberry Pi transfers / Kök Dizin Başlangıcı: Raspberry Pi'dan Raspberry Pi'a transferler için mükemmel

---

## 📋 Requirements / Gereksinimler

- Python 3.7 or higher / Python 3.7 veya üzeri
- Raspberry Pi with SSH enabled / SSH etkin Raspberry Pi
- Network connectivity between devices / Cihazlar arası ağ bağlantısı

---

## 🚀 Installation / Kurulum

1. **Clone the repository / Depoyu klonla**
   ```bash
   git clone https://github.com/ensfur/raspberry-pi-file-transfer.git
   cd raspberry-pi-file-transfer
   ```

2. **Install dependencies / Bağımlılıkları yükle**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application / Uygulamayı çalıştır**
   ```bash
   python main.py
   ```

---

## 📖 Usage / Kullanım

### Initial Setup / İlk Kurulum

1. **Enable SSH on Raspberry Pi / Raspberry Pi'da SSH'ı etkinleştir**
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

2. **Find your Raspberry Pi's IP address / Raspberry Pi IP adresini bul**
   ```bash
   hostname -I
   ```

### Connecting to Raspberry Pi / Raspberry Pi'a Bağlanma

1. **Manual Connection / Manuel Bağlantı**
   - Enter IP address (e.g., `192.168.1.100`) / IP adresini gir (örn. `192.168.1.100`)
   - Enter username (usually `pi`) / Kullanıcı adını gir (genellikle `pi`)
   - Enter password / Şifreyi gir
   - Enter port (default: `22`) / Port gir (varsayılan: `22`)
   - Click "Connect" / "Bağlan"a tıkla

2. **Quick Connect / Hızlı Bağlantı**
   - Use pre-configured buttons for common addresses / Yaygın adresler için önceden yapılandırılmış butonları kullan
   - `pi@192.168.1.100:22`
   - `pi@raspberrypi.local:22`

3. **Save Connection / Bağlantıyı Kaydet**
   - Fill connection details / Bağlantı detaylarını doldur
   - Click "Save" to store connection profile / Bağlantı profilini kaydetmek için "Kaydet"e tıkla
   - Use dropdown to load saved connections / Kaydedilmiş bağlantıları yüklemek için açılır menüyü kullan

### File Operations / Dosya İşlemleri

#### Basic Transfer / Temel Transfer
1. **Upload Files**: Select files in left panel → Click "→ Send to Raspberry Pi" / **Dosya Yükle**: Sol panelde dosyaları seç → "→ Raspberry Pi'a Gönder"e tıkla
2. **Download Files**: Select files in right panel → Click "← Download to PC" / **Dosya İndir**: Sağ panelde dosyaları seç → "← PC'ye İndir"e tıkla

#### Bulk Transfer / Toplu Transfer
1. **Select Multiple Files**: Use Ctrl+Click to select multiple items / **Birden Fazla Dosya Seç**: Birden fazla öğe seçmek için Ctrl+Click kullan
2. **Select All**: Click "📁 Select All" buttons / **Tümünü Seç**: "📁 Tümünü Seç" butonlarına tıkla
3. **Transfer**: Use transfer buttons as normal / **Transfer**: Transfer butonlarını normal şekilde kullan

#### File Management / Dosya Yönetimi
1. **Rename**: Right-click → "Rename" (file extension preserved automatically) / **Yeniden Adlandır**: Sağ tık → "Yeniden Adlandır" (dosya uzantısı otomatik korunur)
2. **Delete**: Right-click → "Delete" (with confirmation) / **Sil**: Sağ tık → "Sil" (onay ile)
3. **File Info**: Right-click → "File Information" / **Dosya Bilgisi**: Sağ tık → "Dosya Bilgisi"
4. **Create Folder**: Click "📁 Create Folder" buttons / **Klasör Oluştur**: "📁 Klasör Oluştur" butonlarına tıkla

#### Transfer Monitoring / Transfer İzleme
1. **Progress Bar**: Shows transfer percentage / **İlerleme Çubuğu**: Transfer yüzdesini gösterir
2. **Speed Display**: Shows transfer speed (MB/s) / **Hız Gösterimi**: Transfer hızını gösterir (MB/s)
3. **ETA**: Shows estimated time remaining / **Tahmini Süre**: Kalan tahmini süreyi gösterir
4. **Cancel Transfer**: Click "❌ Cancel Transfer" button / **Transferi İptal Et**: "❌ Transferi İptal Et" butonuna tıkla

#### Transfer History / Transfer Geçmişi
1. **View Log**: Click "📋 Transfer Log" button / **Log Görüntüle**: "📋 Transfer Log" butonuna tıkla
2. **View Details**: See transfer history with timestamps / **Detayları Görüntüle**: Zaman damgaları ile transfer geçmişini gör

---

## ⌨️ Keyboard Shortcuts / Klavye Kısayolları

| Shortcut / Kısayol | Action / İşlem |
|-------------------|----------------|
| `F5` | Refresh local files / Yerel dosyaları yenile |
| `Ctrl+R` | Refresh remote files / Uzak dosyaları yenile |
| `Ctrl+F5` | Refresh remote files / Uzak dosyaları yenile |

---

## 📁 Project Structure / Proje Yapısı

```
raspberry-pi-file-transfer/
├── main.py                 # Main application entry point / Ana uygulama giriş noktası
├── config_manager.py       # Configuration and settings management / Yapılandırma ve ayar yönetimi
├── connection_manager.py   # SSH/SFTP connection handling / SSH/SFTP bağlantı yönetimi
├── file_transfer.py        # File transfer operations / Dosya transfer işlemleri
├── gui_components.py       # Reusable GUI components and dialogs / Yeniden kullanılabilir GUI bileşenleri ve diyaloglar
├── config.json            # Application configuration (auto-generated) / Uygulama yapılandırması (otomatik oluşturulur)
├── requirements.txt       # Python dependencies / Python bağımlılıkları
├── run.bat               # Windows batch file for easy execution / Kolay çalıştırma için Windows batch dosyası
└── README.md             # This file / Bu dosya
```

---

## 🔧 Configuration / Yapılandırma

The application automatically creates a `config.json` file to store:

Uygulama otomatik olarak şunları saklamak için `config.json` dosyası oluşturur:

- Saved connection profiles / Kaydedilmiş bağlantı profilleri
- Last used connection / Son kullanılan bağlantı
- Transfer history (last 100 operations) / Transfer geçmişi (son 100 işlem)

### Connection Profile Format / Bağlantı Profili Formatı
```json
{
    "connections": [
        {
            "name": "pi@192.168.1.100:22",
            "ip": "192.168.1.100",
            "user": "pi",
            "port": 22
        }
    ],
    "last_connection": "pi@192.168.1.100:22"
}
```

---

## 🛠️ Development / Geliştirme

### Adding New Features / Yeni Özellikler Ekleme

1. **New GUI Components**: Add to `gui_components.py` / **Yeni GUI Bileşenleri**: `gui_components.py`'ye ekle
2. **Transfer Operations**: Extend `file_transfer.py` / **Transfer İşlemleri**: `file_transfer.py`'yi genişlet
3. **Connection Handling**: Modify `connection_manager.py` / **Bağlantı Yönetimi**: `connection_manager.py`'yi değiştir
4. **Configuration**: Update `config_manager.py` / **Yapılandırma**: `config_manager.py`'yi güncelle

### Code Style / Kod Stili
- Follow PEP 8 guidelines / PEP 8 yönergelerini takip et
- Use type hints where possible / Mümkün olduğunda tip ipuçları kullan
- Include docstrings for all functions / Tüm fonksiyonlar için docstring ekle
- English comments and documentation / İngilizce yorumlar ve dokümantasyon

---

## 🐛 Troubleshooting / Sorun Giderme

### Common Issues / Yaygın Sorunlar

1. **Connection Failed / Bağlantı Başarısız**
   - Check IP address and network connectivity / IP adresini ve ağ bağlantısını kontrol et
   - Verify SSH is enabled on Raspberry Pi / Raspberry Pi'da SSH'ın etkin olduğunu doğrula
   - Check username and password / Kullanıcı adı ve şifreyi kontrol et
   - Ensure firewall allows SSH connections / Güvenlik duvarının SSH bağlantılarına izin verdiğinden emin ol

2. **Transfer Interrupted / Transfer Kesildi**
   - Check network stability / Ağ kararlılığını kontrol et
   - Verify sufficient disk space / Yeterli disk alanı olduğunu doğrula
   - Check file permissions on Raspberry Pi / Raspberry Pi'da dosya izinlerini kontrol et

3. **Large File Transfer Issues / Büyük Dosya Transfer Sorunları**
   - Application automatically handles large files / Uygulama büyük dosyaları otomatik olarak işler
   - Progress may not show for very large files / Çok büyük dosyalar için ilerleme gösterilmeyebilir
   - Use transfer cancellation if needed / Gerekirse transfer iptalini kullan

4. **Permission Errors / İzin Hataları**
   - Ensure user has write permissions on target directory / Kullanıcının hedef dizinde yazma izni olduğundan emin ol
   - Check SSH key authentication if password fails / Şifre başarısız olursa SSH anahtar kimlik doğrulamasını kontrol et

### Debug Mode / Hata Ayıklama Modu

Enable debug logging by modifying the application:

Uygulamayı değiştirerek hata ayıklama günlüğünü etkinleştir:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🤝 Contributing / Katkıda Bulunma

1. Fork the repository / Depoyu çatalla
2. Create a feature branch (`git checkout -b feature/amazing-feature`) / Özellik dalı oluştur (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`) / Değişikliklerini kaydet (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`) / Dala gönder (`git push origin feature/amazing-feature`)
5. Open a Pull Request / Pull Request aç

---

## 📄 License / Lisans

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Acknowledgments / Teşekkürler

- [Paramiko](https://github.com/paramiko/paramiko) - SSH2 protocol library / SSH2 protokol kütüphanesi
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI toolkit / Python GUI araç seti

---

## 📞 Support / Destek

- **Issues**: [GitHub Issues](https://github.com/ensfur/raspberry-pi-file-transfer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ensfur/raspberry-pi-file-transfer/discussions)
- **Wiki**: [Project Wiki](https://github.com/ensfur/raspberry-pi-file-transfer/wiki)

---

**Made with ❤️ for the Raspberry Pi community / Raspberry Pi topluluğu için ❤️ ile yapıldı**

*This application simplifies file management between your PC and Raspberry Pi, making development and file sharing more efficient. Perfect for Raspberry Pi to Raspberry Pi transfers as well.*

*Bu uygulama PC ve Raspberry Pi arasındaki dosya yönetimini basitleştirir, geliştirme ve dosya paylaşımını daha verimli hale getirir. Raspberry Pi'dan Raspberry Pi'a transferler için de mükemmeldir.*