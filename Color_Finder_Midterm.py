import cv2
import numpy as np

print("Project Idea: Find the Color")
print("This Python app processes color images to identify the regions in the image")
print("that match the colors of the user's choice. It will show both the original")
print("and processed images along with a metric for color amount.\n")

print("Welcome to 'Find the Color'!")

preset_images = {
    "beach": "beach.jpg",
    "forest": "forest.jpg",
    "city": "city.jpg"
}

color_ranges = {
    "red": [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
    "green": [([36, 50, 70], [89, 255, 255])],
    "blue": [([90, 50, 70], [128, 255, 255])]
}

color_amounts = []

while True:
    print("\nAvailable images:", ", ".join(preset_images.keys()))
    image_choice = input("Type the name of the image you want (beach, forest, city): ").lower()

    if image_choice in preset_images:
        image_file = preset_images[image_choice]
    else:
        print("Invalid choice. Defaulting to beach.")
        image_file = preset_images["beach"]

    img = cv2.imread(image_file)
    if img is None:
        print(f"Could not load '{image_file}'. Make sure the file exists in the folder.")
        continue

    cv2.imshow("Original Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    user_color = input("Enter the color you want to find (e.g., red, green, blue): ").lower()

    if user_color not in color_ranges:
        print(f"Color '{user_color}' is not supported yet.")
        print("Expected output: No regions highlighted, color amount: 0%\n")
        color_amounts.append(0)
    else:
        print(f"Processing image for {user_color} regions...")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_total = None

        for lower, upper in color_ranges[user_color]:
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            mask = cv2.inRange(hsv, lower_np, upper_np)
            mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

        result = cv2.bitwise_and(img, img, mask=mask_total)

        cv2.imshow(f"{user_color.capitalize()} Regions", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        color_percentage = np.sum(mask_total > 0) / mask_total.size * 100
        color_amounts.append(color_percentage)

        print(f"Highlighted {user_color} regions. Approximate color amount: {color_percentage:.2f}%\n")

    cont = input("Would you like to process another color/image? Type 'yes' or 'no': ").lower()
    if cont == "no":
        print("\nThank you for using 'Find the Color'! Goodbye.")
        break