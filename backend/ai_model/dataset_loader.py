from transformers import BertTokenizerFast
from torch.utils.data import Dataset
import torch

class ActionItemDataset(Dataset):
    def __init__(self, filepath, tokenizer, label2id, max_length=128):
        self.tokenizer = tokenizer
        self.label2id = label2id
        self.max_length = max_length
        self.texts, self.labels = self._read_data(filepath)

    def _read_data(self, filepath):
        texts = []
        labels = []
        with open(filepath, "r") as f:
            words = []
            tags = []
            for line in f:
                if line.strip() == "":
                    if words:
                        texts.append(words)
                        labels.append(tags)
                        words = []
                        tags = []
                else:
                    word, tag = line.strip().split()
                    words.append(word)
                    tags.append(tag)
        return texts, labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        words = self.texts[idx]
        tags = self.labels[idx]

        encoding = self.tokenizer(
            words,
            is_split_into_words=True,
            return_offsets_mapping=True,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )

        # Align labels
        labels = [-100] * self.max_length
        word_ids = encoding.word_ids(batch_index=0)

        for i, word_idx in enumerate(word_ids):
            if word_idx is None:
                continue
            labels[i] = self.label2id.get(tags[word_idx], 0)

        encoding = {k: v.squeeze() for k, v in encoding.items()}
        encoding["labels"] = torch.tensor(labels)

        return encoding
