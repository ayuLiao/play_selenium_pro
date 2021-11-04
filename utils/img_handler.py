from PIL import Image, ImageChops


def get_diff_position(before, after):
    before_img = Image.open(before)
    after_img = Image.open(after)
    # PNG文件是PngImageFile对象，与RGBA模式
    # ImageChops.difference方法只能对比RGB模式，所以需要转换一下格式
    before_img = before_img.convert('RGB')
    after_img = after_img.convert('RGB')
    # 对比2张图片中像素不同的位置
    diff = ImageChops.difference(before_img, after_img)
    # 获取图片差异位置坐标
    # 坐标顺序为左、上、右、下
    diff_position = diff.getbbox()
    position_x = diff_position[0]
    return position_x
