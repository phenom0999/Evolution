import numpy as np
from config import ACC_LIMIT

class Brain:
    def __init__(self, input_size, hidden_size, output_size, genes=None):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Calculate total weights needed
        self.gene_size = ((input_size * hidden_size) + hidden_size + 
                          (hidden_size * output_size) + output_size)
        
        if genes is not None:
            self.genes = genes.copy()
        else:
            self.genes = np.random.uniform(-1, 1, self.gene_size)

    def predict(self, inputs):
        # Unpack genes into weights/biases (using split logic from your original code)
        Wih, Bih, Who, Bho = np.split(self.genes, [
            self.input_size * self.hidden_size, 
            self.input_size * self.hidden_size + self.hidden_size,
            (self.input_size * self.hidden_size) + self.hidden_size + (self.hidden_size * self.output_size)
        ])

        # Reshape
        Wih = Wih.reshape(self.input_size, self.hidden_size)
        Who = Who.reshape(self.hidden_size, self.output_size)

        # Forward pass
        input_vector = np.array(inputs).reshape(1, -1)
        hidden = np.tanh(input_vector @ Wih + Bih)
        output = np.tanh(hidden @ Who + Bho) * ACC_LIMIT
        
        return np.squeeze(output)

    def mutate(self, rate, magnitude=1.0):
        mutation_mask = np.random.random(self.genes.shape) < rate
        self.genes[mutation_mask] += np.random.normal(0, magnitude, size=np.sum(mutation_mask))