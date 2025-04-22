import gradio as gr
from src.agent import agent

def chat(user_message, history):
    reply = agent.handle(user_message)
    history.append((user_message, reply))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("## BMO AI Assistant 🤖")
    chatbot = gr.Chatbot()
    state   = gr.State([])
    txt     = gr.Textbox(placeholder="Ask about your balance, transactions, policies…")
    txt.submit(chat, [txt, state], [chatbot, state])
    demo.launch()
