from drivers.opencv.image_driver import ImageProcessor
from drivers.matplot.driver import plot_figure

img_path = 'images/video.PNG'
# img_path = 'images/circulo.PNG'
processor = ImageProcessor(img_path)
img_mask = processor.create_black_and_white_mask()
biggest_contours = processor.find_two_biggest_areas(img_mask)
img_with_centers = processor.find_mass_center(biggest_contours)
new_img = processor.draw_line_between_centers()

plot_figure(new_img)
