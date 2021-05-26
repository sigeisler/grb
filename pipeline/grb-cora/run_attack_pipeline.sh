python attack_pipeline.py \
--n_epoch 2000 \
--lr 0.01 \
--dataset grb-cora \
--dataset_mode full \
--data_dir /home/stanislas/Research/GRB/data/grb-cora/ \
--config_dir /home/stanislas/Research/GRB/pipeline/grb-cora/ \
--feat_norm arctan \
--model gcn \
--model_dir /home/stanislas/Research/GRB/saved_models/grb-cora-arctan-ind-sur/ \
--model_file "checkpoint.pt" \
--save_dir /home/stanislas/Research/GRB/results/grb-cora-arctan-ind/ \
--n_attack 10 \
--n_inject 60 \
--n_edge_max 20 \
--feat_lim_min -1 \
--feat_lim_max 1 \
--gpu 1