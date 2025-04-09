"""
An example of extension. It does nothing, but you can add transformations
before the return statements to customize the webui behavior.

Starting from history_modifier and ending in output_modifier, the
functions are declared in the same order that they are called at
generation time.
"""
from pathlib import Path
from enum import Enum

import gradio as gr

from modules import chat, shared
from modules.llama_cpp_python_hijack import llama_cpp_lib


params = {
    "display_name": "Example Extension",
    "is_tab": False,
}


class ModelLoader(Enum):
    LLAMA_CPP = 1
    EXLLAMA = 2
    EXLLAMA_HF = 3


extension_dir = Path(__file__).parent
context_window_size = 1
js_code = None
model_loader = None


def custom_css():
    """
    Returns a CSS string that gets appended to the CSS for the webui.
    """
    with open(extension_dir / "style.css", "r") as f:
        return f.read()

def custom_js():
    """
    Returns a javascript string that gets appended to the javascript
    for the webui.
    """
    global js_code
    with open(extension_dir / "script.js", "r") as f:
        js_code = f.read()
        return js_code

def get_current_context_percentage():
    if not shared.model:
        return 0

    if model_loader == ModelLoader.LLAMA_CPP:
        num_context_tokens = shared.model.model.n_tokens
    elif model_loader == ModelLoader.EXLLAMA:
        num_context_tokens = shared.model.cache.current_seq_len
    elif model_loader == ModelLoader.EXLLAMA_HF:
        num_context_tokens = shared.model.ex_cache.current_seq_len

    return (num_context_tokens / context_window_size) * 100

def set_context_window_size():
    global context_window_size, model_loader
    if not shared.model:
        return

    model_class_name = type(shared.model).__name__.lower()
    if model_class_name.startswith("llamacpp"):
        model_loader = ModelLoader.LLAMA_CPP
        context_window_size = llama_cpp_lib().llama_n_ctx(shared.model.model.ctx)
    elif model_class_name == "exllamav2model":
        model_loader = ModelLoader.EXLLAMA
        context_window_size = shared.args.max_seq_len
    elif model_class_name == "exllamav2hf":
        model_loader = ModelLoader.EXLLAMA_HF
        context_window_size = shared.args.max_seq_len

def ui():
    """
    Gets executed when the UI is drawn. Custom gradio elements and
    their corresponding event handlers should be defined here.

    To learn about gradio components, check out the docs:
    https://gradio.app/docs/
    """
    HTML = """
    <body>
        <div class="progress-container-container">
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
        </div>
    </body>
    """
    html = gr.HTML(HTML)
    hidden_text = gr.Text(visible=False, elem_id="percentage_color_elem")

    hidden_text.change(None, None, None, js=f'() => {{ {js_code}; updateProgressBar(document.getElementById("percentage_color_elem").children[1].children[1].value); }}')

    shared.gradio['model_status'].change(set_context_window_size, None, None)
    shared.gradio['display'].change(get_current_context_percentage, None, hidden_text)
    shared.gradio['theme_state'].change(None, None, None, js=f"() => {{ {js_code}; toggleDarkMode() }}")
