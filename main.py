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

def copy_dataset_with_class_names(dataset_dir, target_dir, class_labels):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for class_label in class_labels:
        for index, filename in enumerate(os.listdir(os.path.join(dataset_dir, class_label))):
            if os.path.splitext(filename)[1] != ".txt":
                continue
            src_file = os.path.join(dataset_dir, class_label, filename)
            new_filename = f'{class_label}_{index:04}{os.path.splitext(filename)[1]}'
            dst_file = os.path.join(target_dir, new_filename)
            shutil.copyfile(src_file, dst_file)

def copy_dataset_with_random_number(dataset_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    class_labels = os.listdir(dataset_dir)
    for class_label in class_labels:
        if os.path.splitext(class_label)[1] == ".csv":
            continue
        for filename in os.listdir(os.path.join(dataset_dir, class_label)):
            if os.path.splitext(filename)[1] != ".txt":
                continue
            src_file = os.path.join(dataset_dir, class_label, filename)
            random_number = random.randint(0, 10000)
            new_filename = f'{class_label}_{random_number}{os.path.splitext(filename)[1]}'
            dst_file = os.path.join(target_dir, new_filename)
            shutil.copyfile(src_file, dst_file)

def next_instance_of_class(class_label, dataset_path, visited_instances=set()):
    instances = [os.path.join(root, file) for root, _, files in os.walk(os.path.join(dataset_path, class_label)) for file in files if file.endswith(".txt")]
    for instance in instances:
        if instance not in visited_instances:
            visited_instances.add(instance)
            return instance
    return None 

class ClassIterator:
    def __init__(self, class_label, dataset_path):
        self.class_label = class_label
        self.dataset_path = dataset_path
        self.visited_instances = set()

    def __iter__(self):
        return self

    def __next__(self):
        instances = [os.path.join(root, file) for root, _, files in os.walk(os.path.join(dataset_path, class_label)) for file in files if file.endswith(".txt")]
        for instance in instances:
            if instance not in self.visited_instances:
                self.visited_instances.add(instance)
                return instance
        
        raise StopIteration

if __name__ == "__main__":
    class_labels = ['1', '2', '3', '4', '5']
    home = os.path.expanduser('~')
    home_path = os.path.join("C:\\")
    #Create annotation file
    dataset_dir = os.path.join(home_path, "dataset")
    target_dir = os.path.join(home_path, "dataset\\annotation.csv")
    create_annotation_file(dataset_dir, target_dir)
    #Copy dataset with names
    dataset_dir = os.path.join(home_path, "dataset")
    target_dir = os.path.join(home_path, "copy_dataset")
    copy_dataset_with_class_names(dataset_dir, target_dir, class_labels)
    
    dataset_dir = os.path.join(home_path, "copy_dataset")
    target_dir = os.path.join(home_path, "copy_dataset\\annotation.csv")
    create_annotation_file(dataset_dir, target_dir)
    #Ramdom number
    dataset_dir = os.path.join(home_path, "dataset")
    target_dir = os.path.join(home_path, "random")
    copy_dataset_with_random_number(dataset_dir, target_dir)
    
    dataset_dir = os.path.join(home_path, "random")
    target_dir = os.path.join(home_path, "random\\annotation.csv")
    create_annotation_file(dataset_dir, target_dir)

    dataset_path = os.path.join(home_path, "dataset")
    class_label = '5'

    next_instance = next_instance_of_class(class_label, dataset_path)
    if next_instance:
        print(f"Next example '{class_label}': {next_instance}")
    else:
        print(f"Examples '{class_label}' ended")
    
    class_instance_iterator = ClassIterator(class_label, dataset_path)
    for instance in class_instance_iterator:
            print(f"Next example '{class_label}': {instance}")
    else:
        print(f"Examples '{class_label}' ended")