from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


class FinancialLLM:

    def __init__(self):

        print("DEBUG A: Starting tokenizer", flush=True)

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        print("DEBUG B: Tokenizer loaded", flush=True)

        print("DEBUG C: Starting model", flush=True)

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME
        )

        print("DEBUG D: Model loaded", flush=True)

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