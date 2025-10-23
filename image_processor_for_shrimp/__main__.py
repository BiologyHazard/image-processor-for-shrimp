import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def _process_image_pure(image: Image.Image) -> Image.Image:
    original_format = image.format
    logging.debug(
        f"Original format: {original_format}, mode: {image.mode}, size: {image.size}"
    )
    width, height = image.size

    # Ensure image mode is suitable for drawing/saving (JPEG needs RGB)
    if (
        original_format
        and original_format.upper() in ("JPEG", "JPG")
        and image.mode != "RGB"
    ):
        image = image.convert("RGB")

    # Apply Gaussian blur to bottom half
    middle = height // 2
    bottom = height
    bottom_region = image.crop((0, middle, width, bottom))
    blurred = bottom_region.filter(
        ImageFilter.GaussianBlur(radius=max(5, min(width, height) // 80))
    )
    image.paste(blurred, (0, middle))
    logging.info("Applied Gaussian blur to bottom half")

    # Prepare text: top is "Sample" (大一倍)，下行为提示文字（小）
    top_text = "Sample"
    bottom_text = "Legal use requires purchase"
    draw = ImageDraw.Draw(image)

    # Choose font sizes: bottom 为 base，大为两倍
    small_size = max(14, width // 20)
    large_size = small_size * 2

    # Load fonts for both sizes (尝试常见 ttf，失败则回退到默认)
    font_large = None
    font_small = None
    for fname in ("times.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            font_large = ImageFont.truetype(fname, large_size)
            font_small = ImageFont.truetype(fname, small_size)
            break
        except Exception:
            font_large = None
            font_small = None
    if font_large is None or font_small is None:
        font_small = ImageFont.load_default()
        font_large = ImageFont.load_default()
        logging.warning("Could not load TTF font; using default font(s).")

    # compute combined block and positions (centered at 3/4 height)
    target_x = round(width / 2)
    target_y = round(height * 3 / 4)

    # stroke widths relative to font size
    draw.text(
        (target_x, target_y), top_text, font=font_large, fill="black", anchor="md"
    )
    draw.text(
        (target_x, target_y), bottom_text, font=font_small, fill="black", anchor="ma"
    )
    logging.info(f"Rendered watermark text block at x={target_x}, y={target_y}")

    return image


def _process_image(
    file_path: Union[Path, str],
    output_path: Optional[Union[Path, str]] = None,
) -> str:
    logging.info(f"Processing image: {file_path}")
    file_path = Path(file_path)
    if not file_path.is_file():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(file_path)

    image = Image.open(file_path)
    original_format = image.format

    # Process image
    image = _process_image_pure(image)

    # Determine output path
    if output_path:
        out_path = Path(output_path)
        if out_path.exists() and out_path.is_dir():
            name = file_path.stem
            ext = file_path.suffix
            new_name = f"{name}_Shrimp{ext}"
            out_path = out_path / new_name
        else:
            # treat as file path; add extension if missing
            if out_path.suffix:
                out_path = out_path
            else:
                out_path = out_path.with_suffix(file_path.suffix)
    else:
        # Default behavior: save in the same directory as the original
        name = file_path.stem
        ext = file_path.suffix
        new_name = f"{name}_Shrimp{ext}"
        out_path = file_path.parent / new_name

    # Ensure saving mode/format compatibility
    save_kwargs = {}
    if original_format:
        save_format = original_format
    else:
        # fallback based on extension of out_path
        save_format = out_path.suffix.replace(".", "").upper() or None

    if save_format and save_format.upper() in ("JPEG", "JPG"):
        if image.mode in ("RGBA", "LA"):
            image = image.convert("RGB")
        save_kwargs["format"] = "JPEG"
    elif save_format:
        save_kwargs["format"] = save_format

    image.save(str(out_path), **save_kwargs)
    logging.info(f"Saved processed image to: {out_path}")
    return str(out_path)


parser = argparse.ArgumentParser(
    description="Apply bottom-half blur and watermark to an image."
)
parser.add_argument(
    "--file-path",
    "-f",
    dest="file_path",
    required=False,
    help="Path to the image file to process. If not provided, you will be prompted to enter it.",
)
parser.add_argument(
    "--output-path",
    "-o",
    dest="output_path",
    required=False,
    help="Optional output file path or directory. If a directory is provided, output will be saved there with the original name + _Shrimp. If a file path is provided, it will be used as the output path (extension will be added if missing).",
)


def main(argv=None):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(module)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Parse arguments
    args = parser.parse_args(argv)

    # If no file path from command line, prompt user
    file_path = args.file_path
    try:
        while not file_path:
            file_path = input("请输入图片文件路径: ").strip()
            if not file_path:
                print("未输入路径，请重试或按 Ctrl+C 退出。")
                continue
            if not Path(file_path).is_file():
                print(f"文件不存在: {file_path}\n请重新输入有效的文件路径。")
                file_path = None
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(1)

    # Process the image
    try:
        _process_image(file_path, output_path=args.output_path)
    except Exception as e:
        logging.exception(f"Failed to process image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
