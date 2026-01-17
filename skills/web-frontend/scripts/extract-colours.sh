#!/bin/bash
# Extract dominant colours from an image using ImageMagick
# Usage: ./extract-colours.sh path/to/logo.png

IMAGE="$1"

if [ -z "$IMAGE" ]; then
    echo "Usage: ./extract-colours.sh path/to/image.png"
    exit 1
fi

# Check for ImageMagick (v7 uses magick, v6 uses convert)
if command -v magick &> /dev/null; then
    IM_CMD="magick"
elif command -v convert &> /dev/null; then
    IM_CMD="convert"
else
    echo "ImageMagick not installed. Install with: brew install imagemagick"
    exit 1
fi

if [ ! -f "$IMAGE" ]; then
    echo "File not found: $IMAGE"
    exit 1
fi

echo "Extracting colours from: $IMAGE"
echo "================================"
echo ""

# Get 5 most dominant colours as hex
echo "Dominant colours (hex):"
$IM_CMD "$IMAGE" -resize 100x100! -colors 5 -unique-colors txt:- | \
    grep -oE '#[A-Fa-f0-9]{6}' | \
    while read hex; do
        echo "  $hex"
    done

echo ""
echo "Tailwind config:"
echo "  colors: {"
echo "    brand: {"

$IM_CMD "$IMAGE" -resize 100x100! -colors 5 -unique-colors txt:- | \
    grep -oE '#[A-Fa-f0-9]{6}' | \
    head -3 | \
    nl | \
    while read num hex; do
        case $num in
            1) echo "      primary: '$hex'," ;;
            2) echo "      secondary: '$hex'," ;;
            3) echo "      accent: '$hex'," ;;
        esac
    done

echo "    }"
echo "  }"
