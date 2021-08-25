"""Configuration for reproducing leaderboard of grb-citeseer dataset."""
import torch
import torch.nn.functional as F

from grb.evaluator import metric

model_list = ["gcn",
              "gcn_ln",
              "gcn_at",
              "graphsage",
              "graphsage_ln",
              "graphsage_at",
              "sgcn",
              "sgcn_ln",
              "sgcn_at",
              "robustgcn",
              "robustgcn_at",
              "tagcn",
              "tagcn_ln",
              "tagcn_at",
              "appnp",
              "appnp_ln",
              "appnp_at",
              "gin",
              "gin_ln",
              "gin_at",
              "gat",
              "gat_ln",
              "gat_at",
              "gcnguard",
              "gatguard",
              "gcnsvd"]

model_list_basic = ["gcn",
                    "graphsage",
                    "sgcn",
                    "tagcn",
                    "appnp",
                    "gin",
                    "gat"]

modification_attack_list = ["dice",
                            "rand",
                            "flip",
                            "fga",
                            "nea",
                            "stack"]

injection_attack_list = ["rand",
                         "fgsm",
                         "pgd",
                         "speit",
                         "tdgia"]

model_sur_list = ["gcn"]


def build_model(model_name, num_features, num_classes):
    """Hyper-parameters are determined by auto training, refer to grb.utils.trainer.AutoTrainer."""
    if model_name in ["gcn", "gcn_ln", "gcn_at", "gcn_ln_at"]:
        from grb.model.torch import GCN
        model = GCN(in_features=num_features,
                    out_features=num_classes,
                    hidden_features=128,
                    n_layers=3,
                    layer_norm=True if "ln" in model_name else False,
                    dropout=0.7)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["graphsage", "graphsage_ln", "graphsage_at", "graphsage_ln_at"]:
        from grb.model.torch import GraphSAGE
        model = GraphSAGE(in_features=num_features,
                          out_features=num_classes,
                          hidden_features=256,
                          n_layers=5,
                          layer_norm=True if "ln" in model_name else False,
                          dropout=0.5)
        train_params = {
            "lr"                 : 0.0001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["sgcn", "sgcn_ln", "sgcn_at", "sgcn_ln_at"]:
        from grb.model.torch import SGCN
        model = SGCN(in_features=num_features,
                     out_features=num_classes,
                     hidden_features=256,
                     n_layers=4,
                     k=4,
                     layer_norm=True if "ln" in model_name else False,
                     dropout=0.5)
        train_params = {
            "lr"                 : 0.01,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["tagcn", "tagcn_ln", "tagcn_at", "tagcn_ln_at"]:
        from grb.model.torch import TAGCN
        model = TAGCN(in_features=num_features,
                      out_features=num_classes,
                      hidden_features=256,
                      n_layers=3,
                      k=2,
                      layer_norm=True if "ln" in model_name else False,
                      dropout=0.5)
        train_params = {
            "lr"                 : 0.005,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["appnp", "appnp_ln", "appnp_at", "appnp_ln_at"]:
        from grb.model.torch import APPNP
        model = APPNP(in_features=num_features,
                      out_features=num_classes,
                      hidden_features=128,
                      n_layers=3,
                      k=3,
                      layer_norm=True if "ln" in model_name else False,
                      dropout=0.5)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["gin", "gin_ln", "gin_at", "gin_ln_at"]:
        from grb.model.torch import GIN
        model = GIN(in_features=num_features,
                    out_features=num_classes,
                    hidden_features=256,
                    n_layers=2,
                    layer_norm=True if "ln" in model_name else False,
                    dropout=0.6)
        train_params = {
            "lr"                 : 0.0001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["gat", "gat_ln", "gat_at", "gat_ln_at"]:
        from grb.model.dgl import GAT
        model = GAT(in_features=num_features,
                    out_features=num_classes,
                    hidden_features=64,
                    n_layers=3,
                    n_heads=6,
                    layer_norm=True if "ln" in model_name else False,
                    dropout=0.6)
        train_params = {
            "lr"                 : 0.005,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["robustgcn", "robustgcn_at"]:
        from grb.defense import RobustGCN
        model = RobustGCN(in_features=num_features,
                          out_features=num_classes,
                          hidden_features=128,
                          n_layers=3,
                          dropout=0.5)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["gcnsvd", "gcnsvd_ln"]:
        from grb.defense.gcnsvd import GCNSVD

        model = GCNSVD(in_features=num_features,
                       out_features=num_classes,
                       hidden_features=128,
                       n_layers=3,
                       dropout=0.5)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["gcnguard"]:
        from grb.defense import GCNGuard

        model = GCNGuard(in_features=num_features,
                         out_features=num_classes,
                         hidden_features=128,
                         n_layers=3,
                         dropout=0.5)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params
    if model_name in ["gatguard"]:
        from grb.defense import GATGuard

        model = GATGuard(in_features=num_features,
                         out_features=num_classes,
                         hidden_features=64,
                         n_heads=6,
                         n_layers=3,
                         dropout=0.5)
        train_params = {
            "lr"                 : 0.001,
            "n_epoch"            : 5000,
            "early_stop"         : True,
            "early_stop_patience": 500,
            "train_mode"         : "inductive",
        }
        return model, train_params


def build_optimizer(model, lr):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    return optimizer


def build_loss():
    return F.nll_loss


def build_metric():
    return metric.eval_acc


def build_attack(attack_name, device="cpu", args=None):
    if attack_name in "rnd":
        from grb.attack.injection.rnd import RAND

        attack = RAND(n_inject_max=args.n_inject,
                      n_edge_max=args.n_edge_max,
                      feat_lim_min=args.feat_lim_min,
                      feat_lim_max=args.feat_lim_max,
                      device=device)
    elif attack_name in "fgsm":
        from grb.attack.injection.fgsm import FGSM

        attack = FGSM(epsilon=args.lr,
                      n_epoch=args.n_epoch,
                      n_inject_max=args.n_inject,
                      n_edge_max=args.n_edge_max,
                      feat_lim_min=args.feat_lim_min,
                      feat_lim_max=args.feat_lim_max,
                      early_stop=args.early_stop,
                      device=device)
    elif attack_name in "pgd":
        from grb.attack.injection.pgd import PGD

        attack = PGD(epsilon=args.lr,
                     n_epoch=args.n_epoch,
                     n_inject_max=args.n_inject,
                     n_edge_max=args.n_edge_max,
                     feat_lim_min=args.feat_lim_min,
                     feat_lim_max=args.feat_lim_max,
                     early_stop=args.early_stop,
                     device=device)
    elif attack_name in "speit":
        from grb.attack.injection.speit import SPEIT

        attack = SPEIT(lr=args.lr,
                       n_epoch=args.n_epoch,
                       n_inject_max=args.n_inject,
                       n_edge_max=args.n_edge_max,
                       feat_lim_min=args.feat_lim_min,
                       feat_lim_max=args.feat_lim_max,
                       early_stop=args.early_stop,
                       device=device)
    elif attack_name in "tdgia":
        from grb.attack.injection.tdgia import TDGIA

        attack = TDGIA(lr=args.lr,
                       n_epoch=args.n_epoch,
                       n_inject_max=args.n_inject,
                       n_edge_max=args.n_edge_max,
                       feat_lim_min=args.feat_lim_min,
                       feat_lim_max=args.feat_lim_max,
                       early_stop=args.early_stop,
                       inject_mode='random',
                       sequential_step=1.0,
                       device=device)
    elif attack_name in "tdgia_random":
        from grb.attack.injection.tdgia import TDGIA

        attack = TDGIA(lr=args.lr,
                       n_epoch=args.n_epoch,
                       n_inject_max=args.n_inject,
                       n_edge_max=args.n_edge_max,
                       feat_lim_min=args.feat_lim_min,
                       feat_lim_max=args.feat_lim_max,
                       early_stop=args.early_stop,
                       inject_mode='random',
                       device=device)
    elif attack_name in "tdgia_uniform":
        from grb.attack.injection.tdgia import TDGIA

        attack = TDGIA(lr=args.lr,
                       n_epoch=args.n_epoch,
                       n_inject_max=args.n_inject,
                       n_edge_max=args.n_edge_max,
                       feat_lim_min=args.feat_lim_min,
                       feat_lim_max=args.feat_lim_max,
                       early_stop=args.early_stop,
                       inject_mode='uniform',
                       sequential_step=1.0,
                       device=device)
    else:
        raise NotImplementedError

    return attack


def build_model_autotrain(model_name):
    if model_name == "gcn":
        from grb.model.torch import GCN

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return GCN, params_search
    if model_name == "graphsage":
        from grb.model.torch import GraphSAGE

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return GraphSAGE, params_search
    if model_name == "sgcn":
        from grb.model.torch import SGCN

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return SGCN, params_search
    if model_name == "tagcn":
        from grb.model.torch import TAGCN

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "k"              : trial.suggest_categorical("k", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return TAGCN, params_search
    if model_name == "appnp":
        from grb.model.torch import APPNP

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "k"              : trial.suggest_categorical("k", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return APPNP, params_search
    if model_name == "gin":
        from grb.model.torch import GIN

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return GIN, params_search
    if model_name == "gat":
        from grb.model.dgl import GAT

        def params_search(trial):
            model_params = {
                "hidden_features": trial.suggest_categorical("hidden_features", [32, 64, 128, 256]),
                "n_layers"       : trial.suggest_categorical("n_layers", [2, 3, 4, 5]),
                "n_heads"        : trial.suggest_categorical("n_heads", [2, 4, 6, 8]),
                "dropout"        : trial.suggest_categorical("dropout", [0.5, 0.6, 0.7, 0.8]),
            }
            other_params = {
                "lr"                 : trial.suggest_categorical("lr", [1e-2, 1e-3, 5e-3, 1e-4]),
                "n_epoch"            : 5000,
                "early_stop"         : True,
                "early_stop_patience": 500,
            }
            return model_params, other_params

        return GAT, params_search
