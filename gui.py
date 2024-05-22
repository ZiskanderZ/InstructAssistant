import gradio as gr
import random
import time
from llm import AiSimpleClient


class GradioGUI:


    def __init__(self) -> None:
        
        self.css = """
        h1 {
            text-align: center;
            display:block;
        }
        """

        self.theme = gr.themes.Default(primary_hue=gr.themes.colors.sky)
        self.create_blocks()

        self.model = AiSimpleClient()


    def create_assistant(self, promt):

        self.model.init_agent_from_promt(promt)

        return []

    
    def answer_model(self, question, id, history):

        self.model.reply(question, id)

        history_from_model = self.model.get_session_history(id).messages
        history.append((history_from_model[-2].content, history_from_model[-1].content))

        return '', history


    def create_blocks(self):

        self.demo = gr.Blocks(css=self.css, theme=self.theme)
        with self.demo:

            gr.Markdown('<h1 style="font-size:36px;">Time Series Classification Transformer</h1>')
            self.promt_box = gr.Textbox(label='Enter assistant settings')
            self.create_bot_bttn = gr.Button('Create assistant')

            self.chatbot = gr.Chatbot()
            self.user_question_box = gr.Textbox()
            self.mook = gr.Textbox(value=1, visible=False)
            self.submit_bttn = gr.Button('Submit', variant='primary')

            self.create_bot_bttn.click(self.create_assistant, inputs=[self.promt_box], outputs=[self.chatbot])
            self.promt_box.submit(self.create_assistant, inputs=[self.promt_box], outputs=[self.chatbot])

            self.submit_bttn.click(self.answer_model, inputs=[self.user_question_box, self.promt_box, self.chatbot], \
                                                      outputs=[self.user_question_box, self.chatbot])
            
            self.user_question_box.submit(self.answer_model, inputs=[self.user_question_box, self.promt_box, self.chatbot],\
                                                             outputs=[self.user_question_box, self.chatbot])

    
    def start(self):

        self.demo.launch()

if __name__ == '__main__':

    gui = GradioGUI()
    gui.start()