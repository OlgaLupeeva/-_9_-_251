import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_events(json_path: str) -> pd.DataFrame:
    """
    Загружает events.json и возвращает DataFrame.
    JSON ожидается в формате: {"events": [ { "timestamp": "...", "signature": "..." }, ... ]}
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "events" not in data or not isinstance(data["events"], list):
        raise ValueError("Неверный формат JSON: ожидается ключ 'events' со списком событий")

    df = pd.DataFrame(data["events"])

    # Базовая проверка нужных полей
    required_cols = {"timestamp", "signature"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"В данных нет обязательных колонок: {missing}")

    # Приведём timestamp к типу datetime (удобно для анализа, даже если сейчас не требуется)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df


def analyze_signatures(df: pd.DataFrame) -> pd.DataFrame:
    """
    Анализ распределения по типам событий (по полю signature).
    Возвращает таблицу: signature + count
    """
    counts = (
        df["signature"]
        .value_counts(dropna=False)
        .reset_index()
        .rename(columns={"index": "signature", "signature": "count"})
    )
    return counts


def plot_signature_distribution(df: pd.DataFrame) -> None:
    """
    Строит график распределения событий по signature.
    """
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x="signature", order=df["signature"].value_counts().index)

    plt.title("Распределение типов событий информационной безопасности по signature")
    plt.xlabel("Тип события (signature)")
    plt.ylabel("Количество событий")

    # Поворот подписей оси X, чтобы не налезали
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()


def main():
    # Путь к файлу данных рядом со скриптом
    json_path = "events.json"

    df = load_events(json_path)

    # Анализ
    counts = analyze_signatures(df)
    print("Топ типов событий (signature) по количеству:")
    print(counts.to_string(index=False))

    # Визуализация
    plot_signature_distribution(df)


if __name__ == "__main__":
    main()
