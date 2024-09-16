import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.images = []  # Store multiple images
        self.displayed_image = None
        self.tk_image = None
        self.crop_rect = None
        self.start_x = self.start_y = None
        self.crop_start_x = self.crop_start_y = self.crop_end_x = self.crop_end_y = None
        self.canvas_width, self.canvas_height = 600, 600
        self.current_image_index = 0

        # Canvas for image preview
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='gray')
        self.canvas.pack()

        # Button to select images
        self.select_button = tk.Button(root, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)

        # Button to rotate image
        self.rotate_button = tk.Button(root, text="Rotate Image", command=self.rotate_image)
        self.rotate_button.pack(pady=5)

        # Button to navigate through selected images
        self.next_button = tk.Button(root, text="Next Image", command=self.next_image)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(root, text="Previous Image", command=self.prev_image)
        self.prev_button.pack(pady=5)

        # Button to convert images to PDF
        self.convert_button = tk.Button(root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack(pady=10)

        # Mouse bindings for cropping
        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.draw_crop_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if file_paths:
            self.images = [Image.open(file_path) for file_path in file_paths]
            self.current_image_index = 0  # Reset to the first image
            self.display_image(self.current_image_index)

    def display_image(self, image_index):
        if self.images:
            self.current_image = self.images[image_index]
            self.displayed_image = ImageOps.contain(self.current_image, (self.canvas_width, self.canvas_height))
            self.tk_image = ImageTk.PhotoImage(self.displayed_image)
            self.canvas.create_image(300, 300, image=self.tk_image)

    def rotate_image(self):
        if self.images:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.images[self.current_image_index] = self.current_image
            self.display_image(self.current_image_index)

    def next_image(self):
        if self.images and self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.display_image(self.current_image_index)

    def prev_image(self):
        if self.images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_image(self.current_image_index)

    def start_crop(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.crop_rect:
            self.canvas.delete(self.crop_rect)
            self.crop_rect = None

    def draw_crop_rectangle(self, event):
        if self.crop_rect:
            self.canvas.delete(self.crop_rect)
        self.crop_rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red')

    def end_crop(self, event):
        self.crop_end_x = event.x
        self.crop_end_y = event.y

        if self.images and self.start_x and self.start_y and self.crop_end_x and self.crop_end_y:
            orig_width, orig_height = self.current_image.size

            start_x = int(self.start_x * orig_width / self.canvas_width)
            start_y = int(self.start_y * orig_height / self.canvas_height)
            end_x = int(self.crop_end_x * orig_width / self.canvas_width)
            end_y = int(self.crop_end_y * orig_height / self.canvas_height)

            if start_x < end_x and start_y < end_y:
                self.current_image = self.current_image.crop((start_x, start_y, end_x, end_y))
                self.images[self.current_image_index] = self.current_image
                self.display_image(self.current_image_index)

    def convert_to_pdf(self):
        if self.images:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                # Create a canvas for the PDF
                pdf = canvas.Canvas(file_path, pagesize=letter)

                # Loop through all selected images and add each as a page
                for img in self.images:
                    image_width, image_height = img.size
                    aspect_ratio = image_width / image_height
                    pdf_width, pdf_height = letter

                    if aspect_ratio > 1:
                        new_width = pdf_width
                        new_height = pdf_width / aspect_ratio
                    else:
                        new_height = pdf_height
                        new_width = pdf_height * aspect_ratio

                    x_pos = (pdf_width - new_width) / 2
                    y_pos = (pdf_height - new_height) / 2

                    # Add the image directly to the PDF without saving to a temporary file
                    pdf.drawInlineImage(img, x_pos, y_pos, width=new_width, height=new_height)

                    # Create a new page if it's not the last image
                    pdf.showPage()

                # Save the PDF
                pdf.save()

                messagebox.showinfo("Success", "Images converted to PDF successfully!")


# Initialize Tkinter window
root = tk.Tk()
app = ImageToPDFConverter(root)
root.mainloop()
