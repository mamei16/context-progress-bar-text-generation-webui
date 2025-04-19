# Context Progress Bar for text-generation-webui
Displays an animated progress bar below the chat input field that shows how much of the available context window is filled.

![image](https://github.com/user-attachments/assets/06deba7e-8c34-4112-a715-f1e67ad92294)


Right now, only the `llama.cpp`, `llamacpp_HF`, `ExLlamav2` and `ExLlamav2_HF` model loaders are supported.

To use this extension with the [new llama.cpp loader](https://github.com/oobabooga/text-generation-webui/pull/6846), you need to activate metrics for the llama server. To do this, add `"--metrics"` to the [`cmd` list](https://github.com/oobabooga/text-generation-webui/blob/main/modules/llama_cpp_server.py#L253) in the `_start_server` method located in the file `llama_cpp_server.py`.