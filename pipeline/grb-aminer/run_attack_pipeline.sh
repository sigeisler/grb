python attack_pipeline.py \
--n_epoch 2000 \
--lr 0.01 \
--dataset grb-aminer \
--dataset_mode full \
--data_dir /home/stanislas/Research/GRB/data/grb-aminer/ \
--config_dir /home/stanislas/Research/GRB/pipeline/grb-aminer/ \
--feat_norm arctan \
--model gcn \
--model_dir /home/stanislas/Research/GRB/saved_models/grb-aminer-arctan-ind-sur/ \
--model_file 0/checkpoint.pt \
--save_dir /home/stanislas/Research/GRB/results/grb-aminer-arctan-ind/ \
--n_attack 1 \
--n_inject 1500 \
--n_edge_max 100 \
--feat_lim_min -1 \
--feat_lim_max 1 \
--gpu 1
