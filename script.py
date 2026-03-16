from pathlib import Path
from enum import Enum
import re
import logging

import gradio as gr

from modules import chat, shared
try:
    from modules.llama_cpp_python_hijack import llama_cpp_lib
except ImportError:
    llama_cpp_lib = None


params = {
    "display_name": "Context progress bar",
    "is_tab": False,
}


class ModelLoader(Enum):
    LLAMA_CPP = 1
    EXLLAMA = 2
    EXLLAMA_HF = 3
    LLAMA_SERVER = 4


logger = logging.getLogger('text-generation-webui')
extension_dir = Path(__file__).parent
context_window_size = 1
js_code = None
model_loader = None
warning_logged = False


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
    with open(extension_dir / "setup.js", "r") as f:
       return f.read() + js_code


def get_current_context_percentage():
    global warning_logged
    if not shared.model:
        return 0
    if context_window_size == 1:
        set_context_window_size()

    if model_loader == ModelLoader.LLAMA_CPP:
        num_context_tokens = shared.model.model.n_tokens
    elif model_loader == ModelLoader.EXLLAMA:
        num_context_tokens = shared.model.cache.current_seq_len
    elif model_loader == ModelLoader.EXLLAMA_HF:
        num_context_tokens = shared.model.ex_cache.current_seq_len
    elif model_loader == ModelLoader.LLAMA_SERVER:
        num_context_tokens = shared.model.tokens_evaluated + shared.model.tokens_predicted
    else:
        if not warning_logged:
            logger.warning(f"context-progress-bar: 'model_loader' has unexpected value: {model_loader}")
            warning_logged = True
        return 0

    return (num_context_tokens / context_window_size) * 100


def reset_context_window_size():
    global context_window_size
    context_window_size = 1


def set_context_window_size():
    global context_window_size, model_loader, warning_logged
    if not shared.model:
        context_window_size = 1
        return

    warning_logged = False

    model_class_name = type(shared.model).__name__.lower()
    if model_class_name.startswith("llamacpp"):
        model_loader = ModelLoader.LLAMA_CPP
        context_window_size = llama_cpp_lib().llama_n_ctx(shared.model.model.ctx)
    elif model_class_name == "exllamav2model":
        model_loader = ModelLoader.EXLLAMA
        if hasattr(shared.args, "max_seq_len"):
            context_window_size = shared.args.max_seq_len
        else:
            context_window_size = shared.args.ctx_size
    elif model_class_name == "exllamav2hf":
        model_loader = ModelLoader.EXLLAMA_HF
        if hasattr(shared.args, "max_seq_len"):
            context_window_size = shared.args.max_seq_len
        else:
            context_window_size = shared.args.ctx_size
    elif model_class_name == "llamaserver":
        model_loader = ModelLoader.LLAMA_SERVER
        context_window_size = shared.args.ctx_size


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
    hidden_checkbox = gr.Checkbox(visible=False, elem_id="change_notify_checkbox")
    hidden_text = gr.Text(visible=False, elem_id="percentage_elem")

    hidden_text.change(None, None, None,
                       js=f'() => {{ {js_code}; updateProgressBar(document.getElementById("percentage_elem").children[1].children[1].value); }}')

    shared.gradio['load_model'].click(reset_context_window_size, None, None)

    hidden_checkbox.change(get_current_context_percentage, None, hidden_text)
    shared.gradio['theme_state'].change(None, None, None, js=f"() => {{ {js_code}; toggleDarkMode() }}")
