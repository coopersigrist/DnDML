

from example_networks import *
from model_storage import *


net1 = AND(4)
net2 = OR(4)

a = torch.tensor([0.])
b = torch.tensor([1.])
print(net1(a,b))
print(net2(a,b))


# save model
saveModel(net1)
saveModel(net2)

# load model
model_dict = loadModel(net1.__class__.__name__)
model1 = model_dict['class']
model1.load_state_dict(model_dict['state_dict'])

model_dict = loadModel(net2.__class__.__name__)
model2 = model_dict['class']
model2.load_state_dict(model_dict['state_dict'])

print(model1(a,b))
print(model2(a,b))




