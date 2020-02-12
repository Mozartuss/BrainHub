import os

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as f
from torch.utils.data import DataLoader

DEVICE = ("cuda" if torch.cuda.is_available() else "cpu")


class Net(nn.Module):
    """
    The neural network model by it self.
    Here we define all the layers, wights and bias
    """

    def __init__(self, inputs):
        super(Net, self).__init__()
        # define of the layers
        # fc: full connected layer
        # input_layer -> hidden_layer -> output_layer
        # 56 = 14 (Channels) * 4 (Brainwaves)
        # 35 = output of fc1
        # 11 = output of fc2
        # 4 = very low, low, high, very high
        self.fc1 = nn.Linear(inputs, 45)
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.zeros_(self.fc1.bias)

        self.fc2 = nn.Linear(45, 25)
        nn.init.xavier_uniform_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)

        self.fc3 = nn.Linear(25, 4)
        nn.init.xavier_uniform_(self.fc3.weight)
        nn.init.zeros_(self.fc3.bias)

        self.dropout = nn.Dropout(p=0.1)

    def forward(self, x):
        """
        The forward function of the neural network
        :param x: Torch.tensor data input
        :return: Torch.tensor
        """
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)

        return f.softmax(x)


def train(model, optimizer, criterion, train_set, test_set, epochs, batch_size, scheduler, save_path):
    """
    train the model
    :param save_path: the path where you can save the model
    :param scheduler: get the scheduler to adjust the learning rate
    :param batch_size: the amount of samples where no changes will be done
    :param test_set: the test data
    :param train_set: the train data
    :param model: Neural network (class Net)
    :param optimizer: optimization algorithm to optimize the weights
    :param criterion: loss Function
    :param epochs: amount of epochs(runs)
    :return: NONE
    """

    for parameter in model.parameters():
        parameter.requires_grad = True

    train_log, test_log, val_acc_log, tra_acc_log, ra_acc_log, lr_log = [], [], [], [], [], []
    last_loss = 2

    for epoch in range(epochs):
        train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
        training_loss = 0
        train_accuracy = 0
        model.train()

        for data, target in train_loader:
            data.to(device=DEVICE, non_blocking=True)
            target.to(device=DEVICE, non_blocking=True)
            optimizer.zero_grad()
            out = model(data)
            loss = criterion(out, target)
            loss.backward()
            optimizer.step()
            predict = out.data.max(1, keepdim=True)[1]
            train_accuracy += predict.eq(target.data.view_as(predict)).sum().float()
            training_loss += loss.item()

        train_accuracy = 100. * train_accuracy / len(train_loader.dataset)

        # adjust learning rate
        scheduler.step()

        training_loss /= len(train_loader.dataset)

        val_loss, val_accuracy = test(model, criterion, test_set, batch_size)

        last_loss = checkpoint(model, last_loss, val_loss, save_path)

        val_acc_log.append(val_accuracy)
        tra_acc_log.append(train_accuracy)
        train_log.append(training_loss)
        test_log.append(val_loss)
        lr_log.append(optimizer.state_dict()["param_groups"][0]["lr"])

        print_status(epoch, epochs, training_loss, val_loss, val_accuracy, train_accuracy, epoch + 1, epochs,
                     prefix='Training:')
    show(train_log, test_log, val_acc_log, tra_acc_log, lr_log)


def test(model, criterium, test_set, batch_size):
    """
    :param test_set: the testing dataset
    :param batch_size: the amount of samples where no changes will be done
    :param model: Neural Network
    :param criterium: loss Function
    :return: testing_loss, test_accuracy
    """
    test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=False)
    loss = 0
    accuracy = 0
    model.eval()

    for data, target in test_loader:
        with torch.no_grad():
            data.to(device=DEVICE, non_blocking=True)
            target.to(device=DEVICE, non_blocking=True)
            out = model(data)
            loss += criterium(out, target).item()
            predict = out.data.max(1, keepdim=True)[1]
            accuracy += predict.eq(target.data.view_as(predict)).cpu().sum().float()

    return loss / len(test_loader.dataset), 100. * accuracy / len(test_loader.dataset)


def print_status(epoch, epochs, training_loss, testing_loss, val_accuracy, train_accuracy, iteration, total, prefix='',
                 suffix='', decimals=1, length=40, fill='█'):
    """
    print the status of current epoch
    :param fill:
    :param length:
    :param decimals:
    :param suffix:
    :param prefix:
    :param total:
    :param iteration:
    :param train_accuracy:
    :param epoch: current epoch
    :param epochs: amount of epochs
    :param training_loss: loss of the training data
    :param testing_loss: loss of the testing data
    :param val_accuracy: amount of right matches
    :return: NONE
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print("Epoch [{}/{}] ({:.0f}%)]\t|  ".format(epoch + 1, epochs, 100. * (epoch + 1) / epochs),
          "Train loss: {:.2f} ".format(training_loss),
          "Train Acc: {:.2f}%  |  ".format(train_accuracy),
          "Val loss: {:.2f} ".format(testing_loss),
          "Val Acc: {:.2f}%  | ".format(val_accuracy),
          '%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print()


def show(training_loss, testing_loss, val_accuracy, train_accuracy, lr=None):
    """
    :param train_accuracy:
    :param lr: learning rate
    :param training_loss: loss of the training data
    :param testing_loss: loss of the testing data
    :param val_accuracy: amount of right matches
    :return: NONE
    """
    if lr is None:
        lr = []
    if abs(lr[0] - lr[-1]) != 0:
        fig, axs = plt.subplots(3, sharex=True)
    else:
        fig, axs = plt.subplots(2, sharex=True)

    plt.xlabel('Time')
    axs[0].plot(training_loss, label='Training loss', color='mediumturquoise')
    axs[0].annotate('%0.2f' % training_loss[-1], xy=(1, training_loss[-1]), xytext=(8, 5),
                    xycoords=('axes fraction', 'data'), textcoords='offset points', color='mediumturquoise')

    axs[0].plot(testing_loss, label='Testing loss', color='palevioletred')
    axs[0].annotate('%0.2f' % testing_loss[-1], xy=(1, testing_loss[-1]), xytext=(8, -5),
                    xycoords=('axes fraction', 'data'), textcoords='offset points', color='palevioletred')

    axs[0].legend(frameon=False)

    axs[1].set_ylim([0, 100])
    axs[1].plot(train_accuracy, label='Training accuracy', color='mediumturquoise')
    axs[1].annotate('%0.2f' % train_accuracy[-1], xy=(1, train_accuracy[-1]), xytext=(8, 5),
                    xycoords=('axes fraction', 'data'), textcoords='offset points', color='mediumturquoise')
    axs[1].axhline(y=train_accuracy[-1], color='mediumturquoise', linestyle='-.')

    axs[1].plot(val_accuracy, label='Testing accuracy', color='palevioletred')
    axs[1].annotate('%0.2f' % val_accuracy[-1], xy=(1, val_accuracy[-1]), xytext=(8, -5),
                    xycoords=('axes fraction', 'data'), textcoords='offset points', color='palevioletred')
    axs[1].axhline(y=val_accuracy[-1], color='hotpink', linestyle='-.')

    axs[1].legend(frameon=False)

    if abs(lr[0] - lr[-1]) != 0:
        axs[2].plot(lr, label='Learning rate', color='darkgrey')
        axs[2].annotate('{:.5f}'.format(lr[-1]), xy=(1, lr[-1]), xytext=(8, 0),
                        xycoords=('axes fraction', 'data'), textcoords='offset points', color='darkgrey')
        axs[2].legend(frameon=False)
    plt.savefig('./arousal_fig.png', bbox_inches='tight')
    # plt.show()
    plt.close(fig)


def checkpoint(model, best_loss, actual_loss, save_path):
    """
    :param model: Neural Network
    :param best_loss: smallest loss
    :param actual_loss: current loss of the epoch
    :return: smallest loss
    """

    if actual_loss < best_loss:

        """
        Saves the model if the loss decrease 
        and return the actual or the last loss
        """

        # print("\t\tLoss decreased, saving the model..")

        dirs = os.path.sep.join(save_path.split(os.path.sep)[:-1])

        if not os.path.exists('./' + dirs):
            os.makedirs('./' + dirs)
        torch.save(model, './' + save_path)
        return actual_loss
    else:
        return best_loss
