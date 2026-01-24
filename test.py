import numpy as np
from creature import Creature, TARGET, ACC_LIMIT


c = Creature()

c.gene_size

print(len(c.genes))
Wih, Bih, Who, Bho = np.split(c.genes, [c.input_size * c.hidden_size, 
                                            c.input_size * c.hidden_size + c.hidden_size,
                                            (c.input_size * c.hidden_size) + c.hidden_size + (c.hidden_size * c.output_size)])


Wih = Wih.reshape(c.input_size, c.hidden_size)
Bih = Bih.reshape(1,-1)
Who = Who.reshape(c.hidden_size, c.output_size)
Bho = Bho.reshape(1,-1)

I = np.hstack((c.position, c.velocity, TARGET)).reshape(1,-1)
I = (I - I.mean()) / (I.std() + 1e-8)


print(I.shape, Wih.shape)

H = np.tanh(I @ Wih + Bih)


O = np.tanh(H @ Who + Bho) * ACC_LIMIT

print(np.squeeze(O))



print(np.random.rand(10))