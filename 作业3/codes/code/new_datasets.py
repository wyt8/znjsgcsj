import torch
from torch.utils.data import Dataset
import h5py
import json
import os

class NewCaptionDataset(Dataset):
  def __init__(self, data_folder, data_name):
    self.split = "TRAIN"
    
    self.h1 = h5py.File(os.path.join(data_folder, self.split + '_IMAGE_FEATURES_1_' + data_name + '.h5'), 'r')
    self.imgs1 = self.h1['images_features']

    self.h2 = h5py.File(os.path.join(data_folder, self.split + '_IMAGE_FEATURES_2_' + data_name + '.h5'), 'r')
    self.imgs2 = self.h2['images_features']

    with open(os.path.join(data_folder, self.split + '_CAPTIONS_' + data_name + '.json'), 'r') as f:
      self.captions = json.load(f)

    with open(os.path.join(data_folder, self.split + '_CAPLENS_' + data_name + '.json'), 'r') as f:
      self.caplens = json.load(f)
      
    with open(os.path.join(data_folder, self.split + '_SEQS_' + data_name + '.json'), 'r') as f:
      self.seqs = json.load(f)

    self.dataset_size = len(self.captions)

  def __getitem__(self, i):
    
    img1 = torch.FloatTensor(self.imgs1[i])
    img2 = torch.FloatTensor(self.imgs2[i])
    caption = torch.LongTensor(self.captions[i])
    caplen = torch.LongTensor([self.caplens[i]])
    seq = torch.LongTensor(self.seqs[i])

    return img1, img2, caption, caplen, seq

  def __len__(self):
    return self.dataset_size
