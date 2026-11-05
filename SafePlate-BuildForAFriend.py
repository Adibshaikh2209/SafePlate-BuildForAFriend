import torch
import gradio as gr
from transformers import pipeline

# Load lightweight open-weight model (Ungated, no login required)
pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

def plan_meal_for_friend(friend_name, allergies, pantry_items):
    system_instruction = (
        "You are an empathetic, precise meal planner designed for the 'Build for a Friend' challenge. "
        "Your top priority is food safety and simplicity. "
        "Output format:\n"
        "1. Dish Name (Safe & custom-made for the friend)\n"
        "2. Safety Verification (explicitly confirm why the dangerous allergens are omitted)\n"
        "3. 3-Step Simple Recipe (clear instructions under 20 minutes)\n"
        "End with a short, warm note to serve to the friend."
    )
    
    user_query = (
        f"Friend's Name: {friend_name}\n"
        f"Strict Allergies/Dislikes: {allergies}\n"
        f"Available Ingredients: {pantry_items}"
    )
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    response = pipe(messages, max_new_tokens=300, temperature=0.6)
    return response[0]["generated_text"][-1]["content"]

# Build Gradio UI
with gr.Blocks(theme=gr.themes.Soft(), title="SafePlate: Cook for a Friend") as demo:
    gr.Markdown("# 🍲 SafePlate: Build for a Friend")
    gr.Markdown("Create safe, personalized home-cooked meals tailored around your friend's strict food allergies.")
    
    with gr.Row():
        name_input = gr.Textbox(label="Friend's Name", placeholder="e.g., Rahul / Sarah")
        allergies_input = gr.Textbox(label="Strict Allergies / Restrictions", placeholder="e.g., Peanuts, Dairy, Gluten")
        
    pantry_input = gr.Textbox(label="Available Pantry Ingredients", placeholder="e.g., Rice, chicken, carrots, olive oil, garlic, soy sauce")
    action_btn = gr.Button("Generate Safe Meal Plan", variant="primary")
    output_display = gr.Markdown(label="Custom Safe Recipe")
    
    action_btn.click(
        fn=plan_meal_for_friend, 
        inputs=[name_input, allergies_input, pantry_input], 
        outputs=output_display
    )

if __name__ == "__main__":
    demo.launch(share=True)