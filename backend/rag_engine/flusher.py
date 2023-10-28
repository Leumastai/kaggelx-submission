

import gc
import torch

  
def flush(model, pipeline):
  
    """
    This function flushes/clears out loaded model and pipeline out of memory.
    Freeing up space.
    """
    del model
    del pipeline
    
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()


def bytes_to_giga_bytes(bytes):
  return f"Used memory after fushing: {bytes / 1024 / 1024 / 1024} GB"

bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
