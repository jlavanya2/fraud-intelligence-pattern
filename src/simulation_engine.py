def inject_attack(df, intensity=0.3):
    attack = df.sample(frac=intensity)
    attack["amount"] *= 5
    return pd.concat([df, attack])
