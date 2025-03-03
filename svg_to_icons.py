#!/usr/bin/env python3
# svg_to_icons.py
import os
import cairosvg
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Create necessary directories
os.makedirs('resources/icons', exist_ok=True)
os.makedirs('resources/images', exist_ok=True)

# Path to your SVG file
svg_file = "dj-mixer-logo-tool.svg"

# Icon sizes needed
ICON_SIZES = [16, 32, 48, 64, 96, 128, 256, 512, 1024]

def convert_svg_to_png(svg_path, output_path, size):
    """Convert SVG to PNG at specified size"""
    cairosvg.svg2png(
        url=svg_path,
        write_to=output_path,
        output_width=size,
        output_height=size
    )
    print(f"Created icon: {output_path}")

def create_windows_ico(base_dir):
    """Create a Windows ICO file with multiple sizes"""
    try:
        from PIL import Image
        images = []
        for size in [16, 32, 48, 64, 128, 256]:
            icon_path = os.path.join(base_dir, f"app_icon_{size}x{size}.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                # Ensure image is in RGBA mode for transparent background
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                images.append(img)
        
        if images:
            ico_path = os.path.join(base_dir, "app_icon.ico")
            # Save as ICO with multiple sizes
            images[0].save(
                ico_path, 
                format='ICO', 
                sizes=[(img.width, img.height) for img in images],
                append_images=images[1:]
            )
            print(f"Created ICO file: {ico_path}")
        else:
            print("No icon images found to create ICO file.")
    except Exception as e:
        print(f"Error creating ICO file: {e}")
        print("You may need to use an online converter instead.")

def create_macos_iconset(base_dir):
    """Create files needed for Mac OS ICNS conversion"""
    # Create iconset directory
    iconset_dir = os.path.join(base_dir, "app.iconset")
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Mac OS icon naming convention
    mac_icon_sizes = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024)
    ]
    
    for filename, size in mac_icon_sizes:
        source_path = os.path.join(base_dir, f"app_icon_{size}x{size}.png")
        if os.path.exists(source_path):
            output_path = os.path.join(iconset_dir, filename)
            img = Image.open(source_path)
            img.save(output_path)
            print(f"Created Mac icon: {output_path}")
    
    print("\nTo create ICNS file on macOS, run this command:")
    print(f"iconutil -c icns {iconset_dir}")
    print("This will generate app.icns - rename it to app_icon.icns")
    print("\nOr use an online converter to convert the PNG files to ICNS")

def create_splash_screen(svg_path):
    """Create a professional splash screen using the logo"""
    # First convert SVG to PNG for the logo
    logo_path = os.path.join('resources', 'images', 'logo.png')
    cairosvg.svg2png(
        url=svg_path,
        write_to=logo_path,
        output_width=400,
        output_height=400
    )
    
    # Create splash image
    width, height = 700, 500
    splash = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(splash)
    
    # Draw rounded rectangle background
    radius = 20
    
    # Draw the main rectangle
    draw.rectangle(
        [(radius, 0), (width - radius, height)],
        fill=(35, 35, 35, 230)
    )
    draw.rectangle(
        [(0, radius), (width, height - radius)],
        fill=(35, 35, 35, 230)
    )
    
    # Draw the four corner circles
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=(35, 35, 35, 230))
    draw.ellipse((width - radius * 2, 0, width, radius * 2), fill=(35, 35, 35, 230))
    draw.ellipse((0, height - radius * 2, radius * 2, height), fill=(35, 35, 35, 230))
    draw.ellipse((width - radius * 2, height - radius * 2, width, height), fill=(35, 35, 35, 230))
    
    # Load and paste the logo
    try:
        logo = Image.open(logo_path)
        # Calculate position to center the logo
        logo_x = (width - logo.width) // 2
        logo_y = 50
        splash.paste(logo, (logo_x, logo_y), logo)
    except Exception as e:
        print(f"Error adding logo to splash: {e}")
    
    # Add title text
    try:
        title_font_size = 36
        try:
            title_font = ImageFont.truetype("Arial Bold.ttf", title_font_size)
        except:
            try:
                title_font = ImageFont.truetype("Arial.ttf", title_font_size)
            except:
                try: 
                    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", title_font_size)
                except:
                    title_font = ImageFont.load_default()
                    title_font_size = 24
        
        title = "MIDI/HID Inspektr"
        left, top, right, bottom = draw.textbbox((0, 0), title, font=title_font)
        title_width = right - left
        title_position = ((width - title_width) // 2, height - 150)
        
        # Draw title with shadow
        shadow_pos = (title_position[0] + 2, title_position[1] + 2)
        draw.text(shadow_pos, title, font=title_font, fill=(0, 0, 0, 150))
        draw.text(title_position, title, font=title_font, fill=(13, 110, 253, 255))
    except Exception as e:
        print(f"Error drawing title: {e}")
    
    # Add version
    try:
        version_font_size = 24
        try:
            version_font = ImageFont.truetype("Arial.ttf", version_font_size)
        except:
            try:
                version_font = ImageFont.truetype("DejaVuSans.ttf", version_font_size)
            except:
                version_font = ImageFont.load_default()
                version_font_size = 18
        
        version = "Version 1.0.0"
        left, top, right, bottom = draw.textbbox((0, 0), version, font=version_font)
        version_width = right - left
        version_position = ((width - version_width) // 2, height - 100)
        
        # Draw version
        draw.text(version_position, version, font=version_font, fill=(200, 200, 200, 255))
    except Exception as e:
        print(f"Error drawing version: {e}")
    
    # Add status text area at bottom
    try:
        status_font_size = 16
        try:
            status_font = ImageFont.truetype("Arial.ttf", status_font_size)
        except:
            try:
                status_font = ImageFont.truetype("DejaVuSans.ttf", status_font_size)
            except:
                status_font = ImageFont.load_default()
                status_font_size = 14
        
        status = "Initializing..."
        left, top, right, bottom = draw.textbbox((0, 0), status, font=status_font)
        status_width = right - left
        status_position = ((width - status_width) // 2, height - 50)
        
        # Draw status
        draw.text(status_position, status, font=status_font, fill=(180, 180, 180, 255))
    except Exception as e:
        print(f"Error drawing status: {e}")
    
    # Save the splash screen
    output_path = os.path.join('resources', 'images', 'splash.png')
    splash.save(output_path)
    print(f"Created splash screen: {output_path}")

def main():
    if not os.path.exists(svg_file):
        print(f"Error: SVG file {svg_file} not found!")
        return
        
    print("Converting SVG to PNG icons...")
    
    # Convert SVG to PNG at different sizes
    for size in ICON_SIZES:
        output_path = os.path.join('resources', 'icons', f'app_icon_{size}x{size}.png')
        convert_svg_to_png(svg_file, output_path, size)
    
    # Create main app icon file
    convert_svg_to_png(
        svg_file, 
        os.path.join('resources', 'icons', 'app_icon.png'),
        512
    )
    
    # Create Windows ICO
    print("\nCreating Windows ICO file...")
    create_windows_ico(os.path.join('resources', 'icons'))
    
    # Create files for macOS ICNS
    print("\nPreparing files for macOS ICNS...")
    create_macos_iconset(os.path.join('resources', 'icons'))
    
    # Create splash screen
    print("\nCreating splash screen...")
    create_splash_screen(svg_file)
    
    print("\nAll done! Icon files and splash screen have been generated.")
    print("Check the resources directory for your files.")

if __name__ == "__main__":
    main()