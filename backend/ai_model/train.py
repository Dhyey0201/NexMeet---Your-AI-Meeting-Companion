from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from dataset_loader import ActionItemDataset
import torch

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Label maps
label2id = {"O": 0, "B-ACT": 1, "I-ACT": 2}
id2label = {v: k for k, v in label2id.items()}

# Load tokenizer and dataset
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
train_dataset = ActionItemDataset("data/train.txt", tokenizer, label2id)

# Load model
model = BertForTokenClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id,
).to(device)

training_args = TrainingArguments(
    output_dir="./backend/ai_model/model",
    per_device_train_batch_size=8,
    num_train_epochs=5,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=100,
    save_total_limit=2,
    #evaluation_strategy="epoch",
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Start training
trainer.train()

# Save final model and tokenizer
model.save_pretrained("./backend/ai_model/model")
tokenizer.save_pretrained("./backend/ai_model/model")

print("✅ Training complete. Model saved in backend/ai_model/model/")
