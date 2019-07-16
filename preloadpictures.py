import shutil
import os

# Каталог с набором данных
data_dir = r"E:\CropNums"
neural_dir = r"E:\CropNums\ForNeural"
# Каталог с данными для обучения
train_dir = 'train'
# Каталог с данными для проверки
val_dir = 'val'
# Каталог с данными для тестирования
test_dir = 'test'
# Часть набора данных для тестирования
test_data_portion = 0.15
# Часть набора данных для проверки
val_data_portion = 0.15
# Количество элементов данных в одном классе
nb_images = 21


def create_directory(dir_name):
    if not os.path.exists(os.path.join(neural_dir, dir_name)):
        os.makedirs(os.path.join(neural_dir, dir_name))
        os.makedirs(os.path.join(neural_dir, dir_name, "nums"))
        os.makedirs(os.path.join(neural_dir, dir_name, "trash"))


def copy_images(start_index, end_index, source_dir, dest_dir):
    for i in range(start_index, end_index):
        shutil.copy2(os.path.join(source_dir, "OnlyNums", "num" + str(i) + ".bmp"), os.path.join(neural_dir, dest_dir, "nums"))
        shutil.copy2(os.path.join(source_dir, "OnlyTrash", "notnum" + str(i) + ".bmp"), os.path.join(neural_dir, dest_dir, "trash"))


create_directory(train_dir)
create_directory(val_dir)
create_directory(test_dir)


start_val_data_idx = int(nb_images * (1 - val_data_portion - test_data_portion))
start_test_data_idx = int(nb_images * (1 - test_data_portion))
print(start_val_data_idx)
print(start_test_data_idx)

copy_images(0, start_val_data_idx, data_dir, train_dir)
copy_images(start_val_data_idx, start_test_data_idx, data_dir, val_dir)
copy_images(start_test_data_idx, nb_images, data_dir, test_dir)

