import cv2
import time

# Cria o detector de obj / Create object detection
# Cascade = cv2.CascadeClassifier("cascade/cascade2/cascade.xml")
Cascade = cv2.CascadeClassifier("cascade/cascade7/cascade.xml")

# Captura de vídeo da câmera/Capturing the video
video_capture = cv2.VideoCapture(0)

while True:
    # Lê o frame da câmera/Read the camera frame
    ret, frame = video_capture.read()

    # Converte para escala de cinza/Convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detecta obj no frame/Detect the object in the frame
    obj = Cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(obj) > 0:
        x, y, w, h = obj[0][0], obj[0][1], obj[0][2], obj[0][3]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Para cada face detectada/For each face detected
    """for x, y, w, h in obj:"""
    # Desenha um retângulo ao redor da face/Draw a rectangle around the face

    # Mostra o frame na tela/Show the frame in the screen
    cv2.imshow("Video", frame)

    # Espera por um evento de teclado/Wait for keyboard input
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Libera os recursos/Close all
video_capture.release()
cv2.destroyAllWindows()
