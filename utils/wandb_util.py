import torch
import wandb
import numpy as np

@torch.no_grad()
def render_wandb_image(gaussians, viewpoints, render_func, pipe, background, iteration):
    def render(gaussians, viewpoint):
        # scaling_copy = gaussians._scaling
        render_pkg = render_func(viewpoint, gaussians, pipe, background)

        image = render_pkg["render"]
        gt_np = viewpoint.original_image.permute(1,2,0).cpu().numpy()
            
        image_np = image.permute(1, 2, 0).cpu().numpy()  # (H, W, 3)        
        image_np = np.concatenate((gt_np, image_np), axis=1)
        image_np = (np.clip(image_np, 0, 1) * 255).astype('uint8')
        image_np = image_np[::2, ::2, :]
        return image_np

    columns = ['image']
    image_dict = {}
    
    for idx in range(len(viewpoints)):
        image_np = render(gaussians,viewpoints[idx])
        image_dict[f"viewpoint_{idx}"] = wandb.Image(image_np, caption=f"ITER{iteration}")

    return image_dict