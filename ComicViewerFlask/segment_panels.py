from pathlib import Path
import imageio
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation
from scipy import ndimage as ndi
from skimage.measure import label, regionprops
import numpy as np
from PIL import Image
from io import BytesIO
import base64

def segment_panels(image_path):
    image_path = Path(image_path)
    im = imageio.imread(image_path)
    grayscale = rgb2gray(im)
    edges = canny(grayscale)
    thick_edges = dilation(dilation(edges))
    segmentation = ndi.binary_fill_holes(thick_edges)
    labels = label(segmentation)
    regions = regionprops(labels)
    panels = []

    def do_bboxes_overlap(a, b):
        return (
            a[0] < b[2] and
            a[2] > b[0] and
            a[1] < b[3] and
            a[3] > b[1]
        )

    def merge_bboxes(a, b):
        return (
            min(a[0], b[0]),
            min(a[1], b[1]),
            max(a[2], b[2]),
            max(a[3], b[3])
        )

    for region in regions:
        for i, panel in enumerate(panels):
            if do_bboxes_overlap(region.bbox, panel):
                panels[i] = merge_bboxes(panel, region.bbox)
                break
        else:
            panels.append(region.bbox)

    for i, bbox in reversed(list(enumerate(panels))):
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        if area < 0.01 * im.shape[0] * im.shape[1]:
            del panels[i]

    panel_images = []
    for i, bbox in enumerate(panels):
        panel = im[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        panel_image = Image.fromarray(panel)
        buffered = BytesIO()
        panel_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        panel_images.append(f"data:image/png;base64,{img_str}")

    return panel_images
