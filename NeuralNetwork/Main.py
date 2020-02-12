import pandas as pd
from sklearn.model_selection import train_test_split
from torch import optim

from NeuralNetwork.Loader import CustomLoader
from NeuralNetwork.Model import *

# uncomment if you don't use pycharm
# from Loader import CustomLoader
# from Model import *

DEVICE = ("cuda" if torch.cuda.is_available() else "cpu")


def load_checkpoint(filepath):
    model = torch.load(filepath)
    # model.load_state_dict(cp['state_dict'])
    for parameter in model.parameters():
        parameter.requires_grad = False

    model.eval()

    return model


def run(ta_data, tr_data, epochs=100, save_path='arousal.pth', inputs=56):
    train_data_, test_data_, train_label_, test_label_ = train_test_split(tr_data, ta_data, test_size=0.3)
    train_set = CustomLoader(train_data_, test_data_, train_label_, test_label_, 'tr')
    test_set = CustomLoader(train_data_, test_data_, train_label_, test_label_, 'v')
    # if os.path.exists('./net/arousal.pth'):
    # model = load_checkpoint('./net/arousal.pth')
    # print('Load saved Model')
    # else:
    model = Net(inputs=inputs).to(DEVICE)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.5)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=int(epochs * 0.25), gamma=0.6)
    # optimizer = optim.Adam(model.parameters(), lr=1, weight_decay=0.5)
    train(model, optimizer, criterion, train_set, test_set, epochs, batch_size=8, scheduler=scheduler,
          save_path=save_path)


if __name__ == '__main__':
    ta_data = pd.read_csv('../Validation/arousal.csv', header=None)
    tr_data = pd.read_csv('../Converted/Deap/6.Deap_Data_Mean/afd.csv', header=None)
    run(ta_data, tr_data)
