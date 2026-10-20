# Model notes

- The default Q&A endpoint uses TF-IDF retrieval and returns source passages. It does **not** call a generative LLM.
- OCR for image files is optional and requires the Python packages plus the system Tesseract executable. Scanned PDFs may require rendering pages to images before OCR; that flow is not enabled by default.
- LayoutLMv3 is a layout-aware transformer; meaningful use requires OCR words, bounding boxes, image inputs, and a task-appropriate checkpoint.
- Qwen2.5-VL requires substantial model dependencies/hardware. The status endpoint intentionally reports adapter status instead of silently downloading model weights.
- The current knowledge graph is heuristic co-occurrence, not validated entity linking or relation extraction.
