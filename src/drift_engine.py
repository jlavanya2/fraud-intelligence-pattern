from scipy.stats import ks_2samp

def detect_drift(baseline, recent):
    stat, p = ks_2samp(baseline, recent)
    return p < 0.05
