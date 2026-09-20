import numpy as np
from sklearn.ensemble import IsolationForest

trafego = np.array([
    [100, 5], [120, 6], [110, 5], [105, 4], [50000, 500], [109, 5], [111, 6], [45000, 450],
])


def main():
    modelo = IsolationForest(contamination=0.25, random_state=42)
    predicoes = modelo.fit_predict(trafego)  # -1 = anomalia, 1 = normal

    for i, (amostra, pred) in enumerate(zip(trafego, predicoes)):
        status = "ANOMALIA" if pred == -1 else "Normal"
        if status == "ANOMALIA":
            print(f"Amostra {i}: {[int(v) for v in amostra]} -> {status}")

    print("Demais -> Normal")


if __name__ == "__main__":
    main()