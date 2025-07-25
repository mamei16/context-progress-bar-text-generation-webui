from pathlib import Path
from enum import Enum
import re
import logging


import gradio as gr
import requests

from modules import chat, shared
try:
    from modules.llama_cpp_python_hijack import llama_cpp_lib
except ImportError:
    llama_cpp_lib = None


params = {
    "display_name": "Example Extension",
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
kv_cache_tokens_pat = re.compile("llamacpp:kv_cache_tokens ([0-9]+)")
session = requests.Session()


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
    if not shared.model:
        return 0

    if model_loader == ModelLoader.LLAMA_CPP:
        num_context_tokens = shared.model.model.n_tokens
    elif model_loader == ModelLoader.EXLLAMA:
        num_context_tokens = shared.model.cache.current_seq_len
    elif model_loader == ModelLoader.EXLLAMA_HF:
        num_context_tokens = shared.model.ex_cache.current_seq_len
    elif model_loader == ModelLoader.LLAMA_SERVER:
        response = session.get(f"http://localhost:{shared.model.port}/metrics")
        if response.status_code == 501:
            raise ValueError("Please activate llama-server metrics to use the context-progress-bar extension.")
            num_context_tokens = 0
        else:
            kv_cache_tokens_match = kv_cache_tokens_pat.search(response.text)
            if not kv_cache_tokens_match:
                from importlib.metadata import version
                logger.error("context-progress-bar only supports 'llama-cpp-binaries' versions <= v0.14.0,"
                                 f"but you have version {version('llama-cpp-binaries')}.")
            num_context_tokens = int(kv_cache_tokens_match.group(1))
    else:
        logger.warning(f"context-progress-bar: 'model_loader' has unexpected value: {model_loader}")
        return 0

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
        context_window_size = shared.settings["truncation_length"]


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
    hidden_text = gr.Text(visible=False, elem_id="percentage_elem")
    hidden_chat_tab_button = gr.Button(visible=False, elem_id="hidden-chat-tab-button")

    hidden_text.change(None, None, None,
                       js=f'() => {{ {js_code}; updateProgressBar(document.getElementById("percentage_elem").children[1].children[1].value); }}')

    # this should ideally be 'shared.gradio['model_status'].change', but due to bug
    # https://github.com/gradio-app/gradio/issues/9103, this workaround is needed
    hidden_chat_tab_button.click(set_context_window_size, None, None)

    shared.gradio['display'].change(get_current_context_percentage, None, hidden_text)
    shared.gradio['theme_state'].change(None, None, None, js=f"() => {{ {js_code}; toggleDarkMode() }}")
