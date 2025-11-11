import cv2
from pyzbar.pyzbar import decode

def read_barcode(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        # Decodifica os dados do código de barras
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        
        # Desenha o retângulo ao redor do código de barras
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Mostra os dados do código de barras na tela
        text = f'{barcode_data} ({barcode_type})'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f'Tipo: {barcode_type} | Dados: {barcode_data}')

def main():
    # Inicia a captura de vídeo (use 0 para a webcam padrão)
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Lê os códigos de barras no quadro capturado
        read_barcode(frame)
        
        # Exibe o vídeo em tempo real
        cv2.imshow('Leitor de Código de Barras', frame)
        
        # Pressione 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libera a captura de vídeo e fecha todas as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
