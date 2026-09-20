from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)

y_true = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1] 
y_pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] 

def main():
    matriz = confusion_matrix(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    precisao = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Matriz: {matriz.tolist()}")
    print(f"Acurácia: {acc:.2f} | Precisão: {precisao:.2f} | Recall: {recall:.2f} | F1: {f1:.2f}")


if __name__ == "__main__":
    main()