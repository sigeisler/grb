export default {
    GITHUB_PROXY_URL: 'https://cogdl.ai/grb/github/',
    DOCS_URL: 'https://grb.readthedocs.io/en/latest',
    TEAM_URL: 'http://keg.cs.tsinghua.edu.cn/',
    GITHUB_URL: 'https://github.com/thudm/grb',
    Features: [{
        title: 'Elaborated Datasets',
        description: 'GRB introduces datasets of different scales that are preprocessed by a novel splitting scheme and feature normalization, which permits comprehensive evaluation on adversarial robustness.',
        icon: 'data'
    }, {
        title: 'Unified Evaluation',
        description: 'GRB defines a realistic threat model where attackers and defenders can compete with each other under unified settings, which facilitates fair comparisons of various methods.',
        icon: 'attack'
    }, {
        title: 'Modular Framework',
        description: 'GRB provides a coding framework with a modular design, which facilitates the implementation of all GNNs, attacks, defenses, and related evaluation processes.',
        icon: 'Module'
    }, {
        title: 'High Reproducibility',
        description: 'GRB guarantees high reproducibility of all results on the leaderboards, by providing all necessary terms including implementation of methods, hyper-parameters, trained models, easy-to-use scripts, etc.',
        icon: 'config1'
    }]
}