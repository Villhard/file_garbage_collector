import logging
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TRASH_FILES: list[str]
    TRASH_PREFIXES: list[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

logging.basicConfig(level=logging.INFO)


def delete_trash_files(user_path: pathlib.Path):
    counter = 0
    for file_path in user_path.rglob("*"):
        if file_path.is_file() and file_path.name in settings.TRASH_FILES:
            try:
                file_path.unlink()
                counter += 1
                logging.debug(f"Удален файл: {file_path}")
            except Exception as e:
                logging.error(f"Не удалось удалить файл {file_path}: {e}")
    logging.info(f"Удалено {counter} файлов")


def remove_trash_prefix(file_name: str) -> str:
    for prefix in settings.TRASH_PREFIXES:
        if file_name.startswith(prefix):
            return file_name[len(prefix) :]
    return file_name


def rename_files(user_path: pathlib.Path):
    counter = 0
    for file_path in user_path.rglob("*"):
        new_name = remove_trash_prefix(file_path.name)
        if new_name != file_path.name:
            new_path = file_path.with_name(new_name)
            try:
                file_path.rename(new_path)
                logging.debug(f"Переименован файл {file_path} в {new_path}")
                counter += 1
            except Exception as e:
                logging.error(f"Не удалось переименовать файл {file_path}: {e}")
    logging.info(f"Переименовано {counter} файлов")


def main():
    user_input = input("Введите путь к директории: ")
    user_path = pathlib.Path(user_input)
    if not user_path.exists():
        raise FileNotFoundError(f"Путь {user_path} не найден")

    delete_trash_files(user_path)
    rename_files(user_path)


if __name__ == "__main__":
    main()
