#!/usr/bin/env python3
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def detect_cubes(cv_image):
    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Aplica un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Realiza la detección de bordes
    edges = cv2.Canny(blurred, 50, 150)

    # Encuentra los contornos en la imagen
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibuja un rectángulo alrededor de los objetos detectados
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Considera solo contornos con 4 esquinas (cubos)
            cv2.drawContours(cv_image, [approx], 0, (0, 255, 0), 2)

    return cv_image

def image_callback(msg):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv = bridge.imgmsg_to_cv2(msg,'bgr8')
    # Llama a la función de detección de objetos
    cv_image_with_object = detect_cubes(cv_image)
    # Procesa la imagen (puedes agregar tu lógica de procesamiento aquí)
    # Por ejemplo, mostrar la imagen en una ventana:
    cv2.imshow("image camera",cv)
    cv2.imshow("Image with detection", cv_image)
    cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("image_subscriber")

    node.create_subscription(
        Image,
        "/camera_sensor/image_raw",
        image_callback,
        10  # QoS profile depth
    )

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
