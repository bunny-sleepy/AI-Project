import torch
from transformers import BertTokenizer, BertModel
import numpy as np

Tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
Model = BertModel.from_pretrained('bert-base-uncased')

def encode_nlp(text, model = Model, tokenizer = Tokenizer):
    tokenized_text = tokenizer.tokenize(text)
    indexed_tokens=tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    model.eval()
#    tokens_tensor = tokens_tensor.to('cuda')
#    model.to('cuda')

    with torch.no_grad():
        outputs = model(tokens_tensor)
        encoded_layers = outputs[0]
    assert tuple(encoded_layers.shape) == (1, len(indexed_tokens), model.config.hidden_size)
    output = encoded_layers.numpy()[0]
    return np.array(output)

# print(len(encode_nlp("Hello world!", Model, Tokenizer)))