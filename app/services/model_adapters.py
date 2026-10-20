"""Optional heavyweight model adapters. Kept lazy so the MVP runs on a CPU-only laptop."""

def layoutlmv3_status() -> dict:
    return {"model": "microsoft/layoutlmv3-base", "status": "not_loaded", "note": "Use a task-specific fine-tuned checkpoint and OCR boxes for production extraction."}

def qwen_vl_status() -> dict:
    return {"model": "Qwen/Qwen2.5-VL-3B-Instruct", "status": "not_loaded", "note": "Load with Transformers and suitable hardware; model weights are not bundled."}
