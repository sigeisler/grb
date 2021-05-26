python attack_pipeline.py \
--n_epoch 5000 \
--lr 0.001 \
--dataset grb-reddit \
--dataset_mode normal \
--data_dir /home/stanislas/Research/GRB/data/grb-reddit/ \
--config_dir /home/stanislas/Research/GRB/pipeline/grb-reddit/ \
--feat_norm arctan \
--model_dir /home/stanislas/Research/GRB/saved_models/grb-reddit-arctan-ind-sur/ \
--model gcn \
--save_dir /home/stanislas/Research/GRB/results/grb-reddit-arctan-ind/ \
--n_attack 10 \
--n_inject 500 \
--n_edge_max 100 \
--feat_lim_min -1 \
--feat_lim_max 1
