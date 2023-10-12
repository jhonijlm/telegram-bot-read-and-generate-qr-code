from pyzbar.pyzbar import decode
import cv2
import qrcode

class QrCodeService:
    def read(self, file_path: str) -> str:                
        img = cv2.imread(file_path)        
        data = decode(img)             
        
        text = None
        if len(data) > 0 and data[0].type == 'QRCODE':
            text = data[0].data.decode('utf-8')
        
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