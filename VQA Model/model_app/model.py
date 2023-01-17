import torch
import torch.nn as nn
import math

class VQAModel(nn.Module):
    
    def __init__(self,num_labels):
        
        super(VQAModel,self).__init__()
        
        self.num_labels = num_labels
        self.fc1 = nn.Linear(768,256)
        self.bn1 = nn.BatchNorm1d(256)
        
        self.relu = nn.ReLU()
        self.dropout=nn.Dropout(0.3)
        
        self.final_layer = nn.Linear(256,num_labels)
        self.parameter = nn.Parameter(torch.Tensor(768,768))
        
        nn.init.kaiming_uniform_(self.parameter, a=math.sqrt(5))
        
    def forward(self,image_embeddings,text_embeddings):
        
        im1 = torch.nn.functional.normalize(image_embeddings)
        te = torch.nn.functional.normalize(text_embeddings)
        
        cross = im1 * te
        
        weighted = self.relu(torch.mm(cross,self.parameter.t()))
        
        down = self.bn1(self.fc1(weighted))
        
        down = self.dropout(down)
        
        classify = self.final_layer(down)
        
        # loss = self.criterion(classify.view(-1,self.num_labels),label.view(-1))
        
        return classify