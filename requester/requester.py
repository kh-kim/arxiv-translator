import json
import os

import gradio as gr


CONFIG_FN = "config.json"


def read_config(fn):
    with open(fn, "r") as f:
        return json.load(f)
    
config = read_config(CONFIG_FN)


def check_dir(arxiv_id):
    dir_path = os.path.join(config["PAPER_DIR"], arxiv_id)

    if not os.path.exists(dir_path):
        return True
    
    return False


def request_btn_clicked(arxiv_id):
    with open(config["QUEUE_FN"], "r") as f:
        queue = [line.strip() for line in f.readlines() if line.strip() != ""]

    if arxiv_id in queue:
        return "This paper is already in the queue."
    
    if not check_dir(arxiv_id):
        return "This paper is already translated. You can check https://github.com/kh-kim/arxiv-translator"
    
    with open(config["QUEUE_FN"], "a") as f:
        f.write(arxiv_id + "\n")

    return f"Request submitted. Usually, sec/paper is 80. Queue length: {len(queue) + 1}. You can check https://github.com/kh-kim/arxiv-translator after a few mins."


with gr.Blocks() as demo:
    label = gr.Label("Request to translate an arXiv paper to Korean. The translated paper will be available at https://github.com/kh-kim/arxiv-translator")

    with gr.Row():
        arxiv_id_text = gr.Textbox(lines=1, label="arXiv ID (e.g. 2312.12345)")
        request_btn = gr.Button(value="Request to translate")
    
    request_btn.click(
        fn=request_btn_clicked,
        inputs=[arxiv_id_text],
        outputs=[label],
    )    

    demo.launch(
        server_name="0.0.0.0",
        server_port=31215,
        share=True,
    )
