from PIL import Image
import os


def combine_imgs_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """

    # files = os.listdir(folder_path)
    # png_files = []
    # sources = []
    # for file in files:
    #     if 'png' in file or 'jpg' in file:
    #         png_files.append(folder_path + file)
    # png_files.sort()
    png_files = []
    sources = []
    for i in range(150):
        png_files.append(folder_path + str(i) + '.jpg')

    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)


if __name__ == "__main__":
    folder = r"/Volumes/my_disk/company/sensedeal/buffer_disk/a/20220608/images/"
    pdfFile = r"/Volumes/my_disk/company/sensedeal/buffer_disk/a/20220608/images.pdf"
    combine_imgs_pdf(folder, pdfFile)
