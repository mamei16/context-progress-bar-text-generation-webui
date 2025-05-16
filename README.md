# Context Progress Bar for text-generation-webui
Displays an animated progress bar below the chat input field that shows how much of the available context window is filled.

![image](https://github.com/user-attachments/assets/06deba7e-8c34-4112-a715-f1e67ad92294)


Right now, only the `llama.cpp`, `llamacpp_HF`, `ExLlamav2` and `ExLlamav2_HF` model loaders are supported.

To use this extension with the [new llama.cpp loader](https://github.com/oobabooga/text-generation-webui/pull/6846), you need to activate metrics for the llama server. To do this, put the word `metrics` into the "extra-flags" field of the "Model" tab. Alternatively, add the command line flag `--extra-flags metrics` when starting the web UI or add it to the file `text-generation-webui/user_data/CMD_FLAGS.txt`.