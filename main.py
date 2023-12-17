import os
import csv
import shutil
import random

def create_annotation_file(dataset_path, annotation_file_path):
    with open(annotation_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Absolute Path', 'Relative Path', 'Class Label'])
        subfolders = [f.path for f in os.scandir(dataset_path) if f.is_dir()]
        if len(subfolders) > 0:
            class_labels = os.listdir(dataset_path)
            for class_label in class_labels:
                for root, _, files in os.walk(os.path.join(dataset_path, class_label)):
                    for file in files:
                        absolute_path = os.path.join(root, file)
                        relative_path = os.path.relpath(absolute_path, dataset_path)
                        writer.writerow([absolute_path, relative_path, class_label])
        else:
            for root, _, files in os.walk(os.path.join(dataset_path)):
                    for file in files:
                        absolute_path = os.path.join(root, file)
                        relative_path = os.path.relpath(absolute_path, dataset_path)
                        writer.writerow([absolute_path, relative_path])
if __name__ == "__main__":
    class_labels = ['1', '2', '3', '4', '5']
    home = os.path.expanduser('~')
    home_path = os.path.join("C:\\")
    
    dataset_dir = os.path.join(home_path, "dataset")
    target_dir = os.path.join(home_path, "dataset\\annotation.csv")
    create_annotation_file(dataset_dir, target_dir)