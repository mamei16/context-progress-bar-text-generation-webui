"""
An example of extension. It does nothing, but you can add transformations
before the return statements to customize the webui behavior.

Starting from history_modifier and ending in output_modifier, the
functions are declared in the same order that they are called at
generation time.
"""
from pathlib import Path

import gradio as gr

from modules import chat, shared
from modules.llama_cpp_python_hijack import llama_cpp_lib


params = {
    "display_name": "Example Extension",
    "is_tab": False,
}

extension_dir = Path(__file__).parent
context_window_size = 1


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
    with open(extension_dir / "script.js", "r") as f:
        return f.read()

def setup():
    """
    Gets executed only once, when the extension is imported.
    """
    pass

def get_current_context_percentage():
    if not shared.model:
        return 0
    return (shared.model.model.n_tokens / context_window_size) * 100

def set_context_window_size():
    global context_window_size
    if not shared.model:
        return
    context_window_size = llama_cpp_lib().llama_n_ctx(shared.model.model.ctx)

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
    #usage_percentage_input = gr.Slider(label="Context Usage (0.0 - 1.0)", value=0.2, minimum=0., maximum=1., step=0.1)
    hidden_text = gr.Text(visible=False, elem_id="percentage_color_elem")

    #usage_percentage_input.change(lambda x: x*100, usage_percentage_input, hidden_text)
    hidden_text.change(None, None, None, js=f'() => {{ {custom_js()}; updateProgressBar(document.getElementById("percentage_color_elem").children[1].children[1].value); }}')

    shared.gradio['model_status'].change(set_context_window_size, None, None)
    shared.gradio['display'].change(get_current_context_percentage, None, hidden_text)
    shared.gradio['theme_state'].change(None, None, None, js=f"() => {{ {custom_js()}; toggleDarkMode() }}")
