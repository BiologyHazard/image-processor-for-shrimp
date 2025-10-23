# Image Processor for Shrimp

## Overview

This project provides a command-line tool for processing images, specifically targeting the application of a bottom-half blur effect and the addition of a watermark.

## Features

- Apply Gaussian blur to the bottom half of an image
- Add a customizable watermark text
- Support for various image formats

## Requirements

- Python 3.9 or higher
- Pillow library
- Times New Roman font installed

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/image-processor-for-shrimp.git
   cd image-processor-for-shrimp
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the image processor:

   ```bash
   python -m image_processor_for_shrimp --file-path /path/to/image.jpg --output-path /path/to/output.jpg
   ```

## License

This project is licensed under the MIT License.
