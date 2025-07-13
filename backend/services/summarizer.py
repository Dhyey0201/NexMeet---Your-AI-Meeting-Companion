from transformers import T5Tokenizer, T5ForConditionalGeneration

class TranscriptSummarizer:
    def __init__(self, model_name="t5-small", max_chunk_tokens=450):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.max_chunk_tokens = max_chunk_tokens

    def chunk_text(self, text):
        tokens = self.tokenizer.encode(text, return_tensors="pt")[0]
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + self.max_chunk_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
            start = end
        return chunks

    def summarize_text(self, text):
        input_text = "summarize: " + text.strip().replace("\n", " ")
        inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = self.model.generate(
            inputs,
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def summarize_transcript(self, transcript):
        chunks = self.chunk_text(transcript)
        summaries = [self.summarize_text(chunk) for chunk in chunks]

        combined_summary = " ".join(summaries)

        # If combined summary still too long, summarize again
        if len(self.tokenizer.encode(combined_summary)) > 512:
            combined_summary = self.summarize_text(combined_summary)

        return combined_summary

