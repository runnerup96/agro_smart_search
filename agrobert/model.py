from typing import Dict
import torch
from transformers import AutoModel


class TinyRUBertForClassification(torch.nn.Module):

    def __init__(self, distil_bert_path: str, config: dict):
        super(TinyRUBertForClassification, self).__init__()
        self.model_name = distil_bert_path
        self.config = config
        self.n_classes = config["num_classes"]
        self.dropout_rate = config["dropout_rate"]
        self.bert = AutoModel.from_pretrained(distil_bert_path)

        self.pre_classifier = torch.nn.Linear(312, 312)
        self.dropout = torch.nn.Dropout(self.dropout_rate)
        self.bn = torch.nn.BatchNorm1d(312)
        self.classifier = torch.nn.Linear(312, self.n_classes)

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        #         hidden_state = output[0]
        #         hidden_state = hidden_state[:, 0]

        hidden_state = self.pre_classifier(output.last_hidden_state[:, 0, :])
        hidden_state = self.bn(hidden_state)
        hidden_state = torch.nn.ReLU()(hidden_state)
        hidden_state = self.dropout(hidden_state)
        output = self.classifier(hidden_state)
        return output
