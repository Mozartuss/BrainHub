import torch
import torch.utils.data as data


class CustomLoader(data.Dataset):

    def __init__(self, train_data_, test_data_, train_label_, test_label_, label):
        test_label = []
        test_data = []
        train_label = []
        train_data = []

        if label.lower == 'tr':
            for i in range(len(train_label_)):
                train_label.append(train_label_.iloc[i][0])
                train_data.append(train_data_.iloc[i].tolist())

            self.len = len(train_label)
            self.target = torch.tensor(train_label)
            self.train_data = torch.tensor(train_data)

        else:
            for i in range(len(test_label_)):
                test_label.append(test_label_.iloc[i][0])
                test_data.append(test_data_.iloc[i].tolist())

            self.len = len(test_label)
            self.target = torch.tensor(test_label)
            self.train_data = torch.tensor(test_data)

    def __getitem__(self, index):
        return self.train_data[index], self.target[index]

    def __len__(self):
        return self.len
