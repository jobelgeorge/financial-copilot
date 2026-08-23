from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


class FinancialLLM:

    def __init__(self):
        # we download the tokenizer associated with the model
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        #loads the actual pretrained decoder-only Transformer
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME
        )

    def generate(self, prompt: str) -> str:

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        )

        #asks the model to generate the continuation
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200
        )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response