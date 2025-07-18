import torch
import wandb
import numpy as np
from scene import Scene
from lpipsPyTorch.modules.lpips import LPIPS
from utils.loss_utils import ssim
from utils.image_utils import psnr


@torch.no_grad()
def render_wandb_image(gaussians, viewpoints, render_func, pipe, background, iteration, split=None):
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

    image_dict = {}
    
    for idx in range(len(viewpoints)):
        image_np = render(gaussians,viewpoints[idx])
        if split == None:
            image_dict[f"viewpoint_{idx}"] = wandb.Image(image_np, caption=f"ITER{iteration}")
        else:
            image_dict[f"Image/{split}_viewpoint{idx}"] = wandb.Image(image_np, caption=f"ITER{iteration}")

    return image_dict

@torch.no_grad()
def wandb_metric_report(scene : Scene, renderFunc, renderArgs):
    torch.cuda.empty_cache()
    metric_dict = {}
    validation_configs = [{'name': 'test', 'cameras' : scene.getTestCameras()}] # only for testset metric
    lpips_vgg = LPIPS(net_type="vgg").cuda().eval()
    # lpips_alex = LPIPS(net_type="alex").cuda().eval()
    for config in validation_configs:
        if config['cameras'] and len(config['cameras']) > 0:
            # breakpoint()
            print(f"Evaluatting {config['name']} set, {len(config['cameras'])} cameras")
            ssims = []
            psnrs = []
            lpipss = []
            lpipsa = []
            ms_ssims = []
            Dssims = []
            for idx, viewpoint in enumerate(config['cameras']):
                image = torch.clamp(renderFunc(viewpoint, *renderArgs)["render"].to("cuda"), 0.0, 1.0)
                gt_image = torch.clamp(viewpoint.original_image.to("cuda"), 0.0, 1.0)
                ssims.append(ssim(image, gt_image.float()).mean())
                # lpipsa.append(lpips_alex(image, gt_image.float()).mean())
                psnrs.append(psnr(image, gt_image).mean())
                lpipss.append(lpips_vgg(image, gt_image.float()).mean())
                # ms_ssims.append(ms_ssim(image.unsqueeze(0), gt_image.unsqueeze(0).float(), data_range=1, size_average=True ))
                # Dssims.append((1-ms_ssims[-1])/2)

            metric_dict[f"{config['name']}/SSIM"] = torch.tensor(ssims).mean().item()
            metric_dict[f"{config['name']}/PSNR"] = torch.tensor(psnrs).mean().item()
            metric_dict[f"{config['name']}/LPIPS-vgg"] = torch.tensor(lpipss).mean().item()
            # metric_dict[f"Deform_{config['name']}/LPIPS-alex"] = torch.tensor(lpipsa).mean().item()
            # metric_dict[f"Deform_{config['name']}/MS-SSIM"] = torch.tensor(ms_ssims).mean().item()
            # metric_dict[f"Deform_{config['name']}/D-SSIM"] = torch.tensor(Dssims).mean().item()
            # breakpoint()
    torch.cuda.empty_cache()
    return metric_dict