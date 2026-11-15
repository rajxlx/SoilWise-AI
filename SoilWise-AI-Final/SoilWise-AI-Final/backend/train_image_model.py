"""Train a ResNet-50 transfer-learning classifier from an ImageFolder dataset."""
from __future__ import annotations
import argparse
from pathlib import Path
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--output", default=Path("ml/artifacts/soil_resnet50.pt"), type=Path)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        parser.error("epochs and batch-size must be positive")
    if not (args.data_dir / "train").is_dir() or not (args.data_dir / "val").is_dir():
        parser.error("data-dir must contain train/ and val/ ImageFolder directories")

    train_tf = transforms.Compose([
        transforms.Resize((256, 256)), transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(), transforms.ColorJitter(0.12, 0.12, 0.12, 0.04),
        transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((224, 224)), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    train_ds = datasets.ImageFolder(args.data_dir / "train", transform=train_tf)
    val_ds = datasets.ImageFolder(args.data_dir / "val", transform=eval_tf)
    if train_ds.classes != val_ds.classes or len(train_ds.classes) < 2:
        parser.error("train and val must have the same >=2 class folders")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, len(train_ds.classes))
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    criterion = nn.CrossEntropyLoss()
    best_acc = -1.0
    args.output.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * labels.size(0)
        model.eval()
        correct = count = 0
        with torch.inference_mode():
            for images, labels in val_loader:
                logits = model(images.to(device))
                correct += (logits.argmax(1).cpu() == labels).sum().item()
                count += labels.size(0)
        accuracy = correct / max(count, 1)
        print(f"epoch={epoch + 1} train_loss={total_loss / max(len(train_ds), 1):.4f} val_accuracy={accuracy:.4f}")
        if accuracy > best_acc:
            best_acc = accuracy
            torch.save({"state_dict": model.cpu().state_dict(), "classes": train_ds.classes,
                        "validation_accuracy": best_acc}, args.output)
            model.to(device)
    print(f"best_validation_accuracy={best_acc:.4f}; artifact={args.output}")


if __name__ == "__main__":
    main()
