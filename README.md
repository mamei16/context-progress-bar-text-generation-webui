# Context Progress Bar for text-generation-webui
Displays an animated progress bar below the chat input field that shows how much of the available context window is filled.

![image](https://github.com/user-attachments/assets/06deba7e-8c34-4112-a715-f1e67ad92294)


Right now, only the `llama.cpp`, `ExLlamav2` and `ExLlamav2_HF` model loaders are supported.


To use the `llama.cpp` loader with this extension, you need to apply the following patch in the `text-generation-webui` folder, which adds two new member variables, `tokens_evaluated` and `tokens_predicted`, to the `LlamaServer` class: https://gist.github.com/mamei16/f7a30f95c4ea1413c0cc49c686342aff