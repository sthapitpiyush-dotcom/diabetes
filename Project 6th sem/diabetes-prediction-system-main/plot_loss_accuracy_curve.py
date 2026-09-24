
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from diabetes_prediction import DiabetesPredictor, download_dataset


def main():
    dataset_path = download_dataset()
    predictor = DiabetesPredictor(dataset_path)
    predictor.load_data()
    predictor.clean_data()
    predictor.feature_selection()
    predictor.transform_features()
    predictor.split_data()

    X_train = predictor.X_train
    X_test = predictor.X_test
    y_train = predictor.y_train
    y_test = predictor.y_test

    k_values = list(range(1, 31))
    train_losses = []
    test_accuracies = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        train_acc = knn.score(X_train, y_train)
        test_acc = knn.score(X_test, y_test)
        train_losses.append(1.0 - train_acc)
        test_accuracies.append(test_acc)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_loss = "#e74c3c"
    color_acc = "#2980b9"

    ax1.set_xlabel("n_neighbors (k)", fontsize=12)
    ax1.set_ylabel("Training loss (1 − train accuracy)", color=color_loss, fontsize=12)
    ax1.plot(k_values, train_losses, color=color_loss, marker="o", markersize=3, label="Training loss")
    ax1.tick_params(axis="y", labelcolor=color_loss)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Test accuracy", color=color_acc, fontsize=12)
    ax2.plot(k_values, test_accuracies, color=color_acc, marker="s", markersize=3, label="Test accuracy")
    ax2.tick_params(axis="y", labelcolor=color_acc)
    ax2.set_ylim(0.65, 1.0)

    best_k = k_values[int(np.argmax(test_accuracies))]
    fig.suptitle(
        f"KNN: training loss vs test accuracy (best k={best_k}, acc={max(test_accuracies):.4f})",
        fontsize=13,
    )

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")

    fig.tight_layout()
    out_path = "loss_vs_accuracy_curve.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\nPlot saved as '{out_path}'")


if __name__ == "__main__":
    main()
