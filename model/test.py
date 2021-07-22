

from example_networks import *
from model_storage import *


net = AND(32)

a = torch.tensor([1.])
b = torch.tensor([1.])
print(net(a, b))

# save model
saveModel(net)

# load model
model_dict = loadModel(net.__class__.__name__)
model = model_dict['class']
model.load_state_dict(model_dict['state_dict'])

print(model(a, b))




