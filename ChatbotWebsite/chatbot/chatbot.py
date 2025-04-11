from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import torch

# Load the base model and tokenizer
base_model_name = "model_3b"
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = AutoModelForCausalLM.from_pretrained(base_model_name)

# Load the fine-tuned adapter
adapter_path = "fine_tuned_model_3b"
peft_config = PeftConfig.from_pretrained(adapter_path)
model = PeftModel.from_pretrained(model, adapter_path).cuda()

system_message = """You are a helpful and and truthful psychology and psychotherapy assistant. Your primary role is to provide empathetic, understanding, and non-judgmental responses to users seeking emotional and psychological support.
                  Always respond with empathy and demonstrate active listening; try to focus on the user. Your responses should reflect that you understand the user's feelings and concerns. If a user expresses thoughts of self-harm, suicide, or harm to others, prioritize their safety.
                  Encourage them to seek immediate professional help and provide emergency contact numbers when appropriate.  You are not a licensed medical professional. Do not diagnose or prescribe treatments.
                  Instead, encourage users to consult with a licensed therapist or medical professional for specific advice. Avoid taking sides or expressing personal opinions. Your role is to provide a safe space for users to share and reflect.
                  Remember, your goal is to provide a supportive and understanding environment for users to share their feelings and concerns. Always prioritize their well-being and safety."""

def predict_class(message, max_length=50):
    user_input = message
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token to eos token
    
    formatted = f"<s>[INST] <<SYS>>{system_message}<</SYS>>{user_input} [/INST]"

    inputs = tokenizer(formatted, return_tensors="pt", truncation=True, max_length=2048, padding=True)
    
    input_ids = inputs['input_ids'].cuda()
    attention_mask = inputs['attention_mask'].cuda()  # Pass the attention mask here
    
    # Ensure pad token id is set correctly
    pad_token_id = tokenizer.eos_token_id

    with torch.no_grad():
        # Generate the model output
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            do_sample=True,
            top_p=0.9,
            temperature=0.95,
            max_new_tokens=1024,
            pad_token_id=pad_token_id  # Ensure pad token is set
        )

    # Decode the generated output
    translated_output = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(formatted):]
    
    return translated_output

def get_response(message):
    try:
        response = predict_class(message)
        return response
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
