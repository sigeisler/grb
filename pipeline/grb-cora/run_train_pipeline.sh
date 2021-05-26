python train_pipeline.py \
--n_epoch 8000 \
--dataset grb-cora \
--feat_norm arctan \
--data_dir /home/stanislas/Research/GRB/data/grb-cora \
--model_dir /home/stanislas/Research/GRB/saved_models/grb-cora-arctan-ind/ \
--config_dir /home/stanislas/Research/GRB/pipeline/grb-cora/ \
--dropout 0.5 \
--eval_every 1 \
--save_after 0 \
--early_stop \
--n_train 1 \
--train_mode inductive \
--gpu 0