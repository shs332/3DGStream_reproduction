gpu_idx=$1
object_name=$2
idx_from=$3
idx_to=$4
cam_idx=$5
wandb_group_name=$object_name

# CUDA_VISIBLE_DEVICES=$gpu_idx python train.py -s data/Diva360/$object_name \
#     --frame_from $idx_from \
#     --frame_to $idx_to \
#     --cam_idx $cam_idx \
#     --GESI \
#     --wandb_group $wandb_group_name \
#     --model_path "models/Diva360/$object_name" &&

# CUDA_VISIBLE_DEVICES=$gpu_idx python ntc_warmup.py $object_name &&

CUDA_VISIBLE_DEVICES=$gpu_idx python train_frames.py \
    -o output/Diva360/$object_name \
    -m models/Diva360/$object_name \
    -v data/Diva360/$object_name \
    --ntc_conf_path configs/cache/cache_F_4.json \
    --ntc_path ntc/${object_name}_F_4.pth \
    --first_load_iteration 15000 \
    --frame_from $idx_from \
    --frame_to $idx_to \
    --cam_idx $cam_idx \
    --GESI \
    --wandb_group $wandb_group_name \
    --iterations 150 \
    --iterations_s2 100