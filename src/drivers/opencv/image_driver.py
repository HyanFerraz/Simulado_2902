import cv2
import numpy as np
from math import atan, degrees
from drivers.numpy.driver import create_hsv_filter

class ImageProcessor:
    new_img = None
    mass_centers = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    def __init__(self, img_path):
        self.img = cv2.imread(img_path)
        

    def convert_to_HSV(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def convert_to_RGB(self):
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def create_black_and_white_mask(self) :
        lower_filter = [0,115,0]
        upper_filter = [180,255,255]
        hsv_filter = create_hsv_filter(lower_filter, upper_filter)

        return cv2.inRange(self.convert_to_HSV(), hsv_filter["lower"], hsv_filter["upper"])

    def find_two_biggest_areas(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        biggest_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            biggest_contours.append((area, contour))

        biggest_contours.sort(key=lambda x: x[0], reverse=True)
    
        return biggest_contours[:2]

    def find_mass_center(self, contours):
        self.new_img = np.zeros_like(self.img)
        for contour in contours:
            cv2.drawContours(self.new_img, [contour[1]], -1, (255, 255, 255), cv2.FILLED)
            figure_moment = cv2.moments(contour[1])

            cx = int(figure_moment['m10']/figure_moment['m00'])
            cy = int(figure_moment['m01']/figure_moment['m00'])
            self.mass_centers.append({
                "cx" : cx,
                "cy" : cy
            })

            size = 20
            color = (255,0,0)
            
            for center in self.mass_centers:
                cv2.line(self.new_img,(center["cx"] - size,center["cy"]),(center["cx"] + size,center["cy"]),color,3)
                cv2.line(self.new_img,(center["cx"],center["cy"] - size),(center["cx"], center["cy"] + size),color,3)
                text = center["cx"], center["cy"]

                text_point = (center["cx"] - 75, center["cy"] - 50)

                cv2.putText(self.new_img, str(text), text_point, self.font, 1, color, 2, cv2.LINE_AA)
        
        return self.new_img

    def draw_line_between_centers(self):
        cv2.line(self.new_img,(self.mass_centers[0]["cx"], self.mass_centers[0]["cy"]),(self.mass_centers[1]["cx"] , self.mass_centers[1]["cy"]), (0,255,0), 3)

        total_height = self.mass_centers[0]["cy"] - self.mass_centers[1]["cy"]
        total_width = self.mass_centers[0]["cx"] - self.mass_centers[1]["cx"]

        if total_width > 0:
            angle = atan(abs(total_height)/abs(total_width))
            angle_degrees = degrees(angle)
        else:
            angle_degrees = 90

        formatted_number = format(angle_degrees, '.2f')

        cv2.putText(self.new_img, str(formatted_number), (300, 300), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        return self.new_img
        