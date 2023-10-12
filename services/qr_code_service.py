import qrcode
import zxing

class QrCodeService:
    def read(self, file_path: str) -> str:                
        reader = zxing.BarCodeReader()
        barcode = reader.decode(file_path)
        
        text = None
        if barcode.format == 'QR_CODE' and len(barcode.parsed) > 0:
            text = barcode.parsed
            
        return text

    
    def generate(self, text: str, filename: str) -> object:      
        text = text[:500]
                          
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_M,            
            border = 1
        )
                
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color = 'black', back_color = 'white')
        
        path = f"./storage/files/{filename}"
        img.save(path)
        
        return {
            'path': path,
            'filename': filename
        }