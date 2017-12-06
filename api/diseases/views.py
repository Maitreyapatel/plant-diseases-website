from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.core.files.storage import FileSystemStorage
from .forms import ProfileForm
import PIL
import torch.tensor as tensor
from PIL import Image
import pickle

# Create your views here.


'''
Code for computer vision starts here
'''

import time
import os

import numpy as np
import torch
import torch.optim as optim
from torch import nn
from torch.autograd import Variable

import torchvision
import torchvision.models as models
import torch.utils.model_zoo as model_zoo
import torchvision.transforms as transforms
from torchvision import datasets


from itertools import accumulate
from functools import reduce

#configuration
model_urls = {
    'alexnet': 'https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth',
}

model_names = model_urls.keys()

input_sizes = {
    'alexnet' : (224,224),
}

models_to_test = ['alexnet']

batch_size = 20
use_gpu = torch.cuda.is_available()


# Generic pretrained model loading

# We solve the dimensionality mismatch between
# final layers in the constructed vs pretrained
# modules at the data level.
def diff_states(dict_canonical, dict_subset):
    names1, names2 = (list(dict_canonical.keys()), list(dict_subset.keys()))

    # Sanity check that param names overlap
    # Note that params are not necessarily in the same order
    # for every pretrained model
    not_in_1 = [n for n in names1 if n not in names2]
    not_in_2 = [n for n in names2 if n not in names1]
    assert len(not_in_1) == 0
    assert len(not_in_2) == 0

    for name, v1 in dict_canonical.items():
        v2 = dict_subset[name]
        assert hasattr(v2, 'size')
        if v1.size() != v2.size():
            yield (name, v1)


def load_defined_model(name, num_classes):
    model = models.__dict__[name](num_classes=num_classes)

    # Densenets don't (yet) pass on num_classes, hack it in for 169
    if name == 'densenet169':
        model = torchvision.models.DenseNet(num_init_features=64, growth_rate=32, \
                                            block_config=(6, 12, 32, 32), num_classes=num_classes)

    pretrained_state = model_zoo.load_url(model_urls[name])

    # Diff
    diff = [s for s in diff_states(model.state_dict(), pretrained_state)]
    print("Replacing the following state from initialized", name, ":", \
          [d[0] for d in diff])

    for name, value in diff:
        pretrained_state[name] = value

    assert len([s for s in diff_states(model.state_dict(), pretrained_state)]) == 0

    # Merge
    model.load_state_dict(pretrained_state)
    return model, diff


def filtered_params(net, param_list=None):
    def in_param_list(s):
        for p in param_list:
            if s.endswith(p):
                return True
        return False
        # Caution: DataParallel prefixes '.module' to every parameter name

    params = net.named_parameters() if param_list is None \
        else (p for p in net.named_parameters() if in_param_list(p[0]))
    return params

'''
And ends here
'''





def diseases(request):
    return render(request, 'diseases/home.html')

def res(request):
    if request.method == 'POST':
        q=request.POST['search']

        try:
            es=Elasticsearch()

            res = es.search(index="hackathon", doc_type="plant-diseases", size=3, body={"query": {"multi_match": {"fields": ["crop^5", "disease^2", "symptoms^3", "cause","comment"], "query": q}}})
            results=[]
            for i in range(len(res['hits']['hits'])):
                temp=[]
                temp.append(res['hits']['hits'][i]['_source']['crop'])
                temp.append(res['hits']['hits'][i]['_source']['disease'])
                temp.append(res['hits']['hits'][i]['_source']['cause'])
                temp.append(res['hits']['hits'][i]['_source']['symptoms'])
                temp.append(res['hits']['hits'][i]['_source']['manage'])
                temp.append(res['hits']['hits'][i]['_source']['comment'])

                results.append(temp)
        except:
            return render(request, 'diseases/home.html')
        return render(request, 'diseases/results.html',{'result':results})
    else:
        return render(request, 'diseases/home.html')

def SaveProfile(request):
    saved = False

    if request.method == "POST":
        print ("in")
        MyProfileForm = ProfileForm(request.POST,request.FILES)
        if MyProfileForm.is_valid():
            print ("in1")
            pic = MyProfileForm.cleaned_data["picture"]
            '''
            Error in getting display uploaded images we are gonna send direct result only.
            But we have to solve this.
            '''
            mainfolder = "/home/maitreya/Desktop/hackinfinity/PlantVillage/test/" #Plz enter the path to local dir we need to change this
            prep = transforms.Compose([transforms.Scale(int(max((224, 224)) / 224 * 256)),
                                       transforms.CenterCrop(max((224, 224))),
                                       transforms.ToTensor(),
                                       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                       ])
            file = mainfolder+str(pic)

            net = pickle.load(open("save.pickle", "rb"))
            l = pickle.load(open("save_l.pickle", "rb"))

            img = Image.open(file)
            img = prep(img)
            img = Variable(img.unsqueeze(0))

            out = net(img).data[0]
            _, idx = torch.max(out, 0)
            idx = idx.numpy()[0]

            result = l[idx]

            if result == "background":
                result = "Please upload the image of leaf. If you have uploaded image still you get this result then please mail us regradig this issue."
            # profile.save()
            saved = True
            return render(request, 'diseases/saved.html',{'result':result})
        else:
            MyProfileForm = ProfileForm()


def up(request):
    return render(request, 'diseases/photo.html')