import torch
import yaml
import os

class D2_SizeSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(config_dir, "config.yaml")

        with open(config_file, "r", encoding="utf-8") as file:
            config_value = yaml.safe_load(file)

        cls.size_dict = config_value["size_dict"]
        cls.size_list = ["custom"]
        cls.size_list.extend(cls.size_dict.keys())

        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "preset": (cls.size_list,),
                "swap_dimensions": (["Off", "On"],),
                "upscale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step":0.1}),
                "prescale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 100.0, "step":0.1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT", "INT", "LATENT",)
    RETURN_NAMES = ("width", "height", "upscale_factor", "prescale_factor", "batch_size", "empty_latent",)
    FUNCTION = "size_selector"
    CATEGORY = "utils"

    def size_selector(self, width, height, preset, swap_dimensions, upscale_factor, prescale_factor, batch_size):

        width = self.__class__.size_dict.get(preset).get("width", width)
        height = self.__class__.size_dict.get(preset).get("height", height)

        if swap_dimensions == "On":
            width, height = height, width

        width = int(width*prescale_factor)
        height = int(height*prescale_factor)

        latent = torch.zeros([batch_size, 4, height // 8, width // 8])


        return(width, height, upscale_factor, prescale_factor, batch_size, {"samples":latent}, )
