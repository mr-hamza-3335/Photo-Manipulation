import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import io
import cv2

st.set_page_config(" Advanced Photo Editor", layout="centered")
st.title(" Advanced Photo Editor App")
st.caption("Enhance your photos with awesome effects and tools ")

uploaded_file = st.file_uploader(" Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Original Image", use_column_width=True)

    # Sidebar Tools
    st.sidebar.header("🎨 Editing Tools")

    # Brightness
    brightness = st.sidebar.slider("☀️ Brightness", 0.1, 3.0, 1.0)
    image = ImageEnhance.Brightness(image).enhance(brightness)

    # Contrast
    contrast = st.sidebar.slider("🎚️ Contrast", 0.1, 3.0, 1.0)
    image = ImageEnhance.Contrast(image).enhance(contrast)

    # Blur
    blur = st.sidebar.slider("🌫️ Blur", 0, 10, 0)
    if blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur))

    # Grayscale
    if st.sidebar.checkbox("⚫ Grayscale"):
        image = image.convert("L")

    # Sepia
    if st.sidebar.checkbox("🎨 Sepia Filter"):
        sepia_img = np.array(image.convert("RGB"))
        tr = [0.393, 0.769, 0.189]
        tg = [0.349, 0.686, 0.168]
        tb = [0.272, 0.534, 0.131]
        r, g, b = sepia_img[:,:,0], sepia_img[:,:,1], sepia_img[:,:,2]
        sepia = np.stack([
            np.clip(r*tr[0]+g*tr[1]+b*tr[2], 0, 255),
            np.clip(r*tg[0]+g*tg[1]+b*tg[2], 0, 255),
            np.clip(r*tb[0]+g*tb[1]+b*tb[2], 0, 255)
        ], axis=2).astype(np.uint8)
        image = Image.fromarray(sepia)

    # Invert Colors
    if st.sidebar.checkbox(" Invert Colors"):
        image = ImageOps.invert(image.convert("RGB"))

    # Flip
    flip_option = st.sidebar.selectbox("↔ Flip Image", ["None", "Horizontal", "Vertical"])
    if flip_option == "Horizontal":
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_option == "Vertical":
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Rotate
    rotate = st.sidebar.slider(" Rotate Image", 0, 360, 0, step=5)
    if rotate != 0:
        image = image.rotate(rotate)

    # Crop Tool
    st.sidebar.subheader("✂️ Crop Image")
    crop = st.sidebar.checkbox("Enable Crop")
    if crop:
        width, height = image.size
        left = st.sidebar.slider("Left", 0, width, 0)
        top = st.sidebar.slider("Top", 0, height, 0)
        right = st.sidebar.slider("Right", left+1, width, width)
        bottom = st.sidebar.slider("Bottom", top+1, height, height)
        image = image.crop((left, top, right, bottom))

    # Sketch Filter
    if st.sidebar.checkbox("✏️ Sketch Filter"):
        img_np = np.array(image.convert("L"))
        inv = 255 - img_np
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(img_np, 255 - blur, scale=256)
        image = Image.fromarray(sketch)

    # Cartoon Effect
    if st.sidebar.checkbox("🌈 Cartoon Effect"):
        img_np = np.array(image.convert("RGB"))
        img_color = cv2.bilateralFilter(img_np, d=9, sigmaColor=200, sigmaSpace=200)
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
        img_edges = cv2.adaptiveThreshold(cv2.medianBlur(img_gray, 5), 255,
                                          cv2.ADAPTIVE_THRESH_MEAN_C,
                                          cv2.THRESH_BINARY, 9, 10)
        img_cartoon = cv2.bitwise_and(img_color, img_color, mask=img_edges)
        image = Image.fromarray(img_cartoon)

    # Show Final Image
    st.image(image, caption="✨ Edited Image", use_column_width=True)

    # Download
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    st.download_button("💾 Download Image", img_bytes.getvalue(), file_name="edited_image.png", mime="image/png")

    # Instructions
    with st.expander("📖 How to Use"):
        st.markdown("""
        - Upload an image from your device 📤  
        - Use sidebar to apply effects and filters 🎨  
        - Download final edited image 💾  
        - Enjoy editing! ✨
        """)

else:
    st.info("⬆️ Upload an image to get started...")

# Footer
st.markdown("---")
st.markdown("🔧 Made with ❤️ using Python & Streamlit")
