from openai import OpenAI 
import gradio as gr
import os

GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_story(issue, impact, helpers, desired_change, location, facts, language, variations):
    prompt = f"""
    Create an inspiring social good story in {language}.
    Details:
    - Issue: {issue}
    - Impact: {impact}
    - Helpers: {helpers}
    - Desired Change: {desired_change}
    - Location: {location}
    - Facts: {facts}
    Format:
    **Title: <Story Title>**
    <Paragraph 1>
    <Paragraph 2>
    <Call to Action>
    """
    try:
        stories = []
        for _ in range(variations):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Model supported via Groq
                messages=[{"role": "user", "content": prompt}]
            )
            stories.append(response.choices[0].message.content)
        return "\n\n---\n\n".join(stories)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def save_to_file(story):
    filename = "social_good_story.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(story)
    return filename

css = """
body {
    background: linear-gradient(to bottom right, #e6f2ff, #ffffff);
}
h1, h2, h3 { text-align: center; font-family: 'Trebuchet MS', sans-serif; font-size: 32px; font-weight: bold; color: #004080; margin-bottom: 20px; }
textarea, input, select {
    background-color: sky-blue !important; border: 1px solid #99c2ff !important;
    border-radius: 10px !important; padding: 10px !important; font-size: 16px !important;
}
input[type=range] { accent-color: #004080 !important; }
"""

with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
    gr.Markdown("## 🌍 Social Good Storytelling Chatbot\nGenerate inspiring stories for a better world ✨")

    with gr.Row():
        issue = gr.Textbox(label="Issue", placeholder="e.g. Lack of clean water")
        location = gr.Textbox(label="Location", placeholder="e.g. Rural village in India")
    with gr.Row():
        impact = gr.Textbox(label="Impact", placeholder="e.g. Affects children’s health")
        helpers = gr.Textbox(label="Helpers", placeholder="e.g. Local volunteers, NGOs")
    desired_change = gr.Textbox(label="Desired Change", placeholder="e.g. Build clean water wells")
    facts = gr.Textbox(label="Facts", placeholder="e.g. 60% families don’t have clean water access")
    with gr.Row():
        language = gr.Dropdown(["English", "Hindi"], value="English", label="Language")
        variations = gr.Slider(1, 3, step=1, value=1, label="Number of Story Variations")
    output = gr.Textbox(label="Generated Story", lines=14)

    with gr.Row():
        btn_generate = gr.Button("✨ Generate Story")
        btn_download = gr.Button("💾 Download Story")
    btn_generate.click(generate_story, inputs=[issue, impact, helpers, desired_change, location, facts, language, variations], outputs=output)
    btn_download.click(save_to_file, inputs=output, outputs=gr.File(label="Download File"))

demo.launch(share=True, debug=False)
