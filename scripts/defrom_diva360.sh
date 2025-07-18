gpu_idx=$1
object_name=$2
idx_from=$3
idx_to=$4
cam_idx=$5
wandb_group_name=$object_name

CUDA_VISIBLE_DEVICES=$gpu_idx python train.py -s data/Diva360/$object_name \
    --frame_from $idx_from \
    --frame_to $idx_to \
    --cam_idx $cam_idx \
    --GESI \
    --wandb_group $wandb_group_name \
    --model_path "models/Diva360/$object_name" &&



# TODO: NTC warm-up in .py file implementation
# CUDA_VISIBLE_DEVICES=$gpu_idx python train_frames.py \
#     --read_config \
#     --config_path test/flame_steak_suite/cfg_args.json \
#     -o output/Code-Release \
#     -m test/flame_steak_suite/flame_steak_init/ \
#     -v <scene> \
#     --image images_2 \
#     --first_load_iteration 15000 \
#     --quiet \
#     --frame_from $idx_from \
#     --frame_to $idx_to \
#     --cam_idx $cam_idx \
#     --GESI \
#     --wandb_group $wandb_group_name



CUDA_VISIBLE_DEVICES=5 python train.py -s data/Diva360/bunny \
    --frame_from 0000 \
    --frame_to 1000 \
    --cam_idx 00 \
    --GESI \
    --wandb_group "Debug" \
    --model_path "models/Diva360/bunny"
