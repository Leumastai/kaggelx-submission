
from typing import Any
import transformers
import torch
from torch import bfloat16, float16
from rag_engine.configs.config_loader import model_configs, device
from rag_engine.configs.envs_loader import credentials


class RAGModel:

    """
    ### Model Initializer
    Iniitializes and quantize the LLM model used from huggin face
    """
    def __init__(self) -> None:
        
        self.hf_auth = credentials['HF_AUTH']
        self.model_id = model_configs['model_id']
        self.dtype = torch.float16
    
        self.bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype= bfloat16,
        )

        self.model_config = transformers.AutoConfig.from_pretrained(
            self.model_id,
            use_auth_token=self.hf_auth,
        )

        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            config=self.model_config,
            quantization_config=self.bnb_config,
            device_map=device,#"auto", #
            use_auth_token=self.hf_auth,
            #torch_dtype = self.dtype,
        )

        print(f"Model loaded on {device}")

        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id,
            use_auth_token=self.hf_auth,
        )

    def __call__(self, ) -> Any:
        text_generateion_pipeline = transformers.pipeline(
            model = self.model, tokenizer=self.tokenizer,
            return_full_text=True,
            **model_configs['model_params'],
        )

        return text_generateion_pipeline

