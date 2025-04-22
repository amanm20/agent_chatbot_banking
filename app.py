import gradio as gr
from src.agent import agent

def chat_fn(user, history):
    bot = agent.handle(user)
    history.append((user, bot))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("# BMO AI Assistant 🤖 💰")
    chatbot = gr.Chatbot()
    state = gr.State([])
    txt = gr.Textbox(placeholder="Ask me about your BMO account…")
    txt.submit(chat_fn, [txt, state], [chatbot, state])
    demo.launch()
