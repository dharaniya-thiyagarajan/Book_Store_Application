from django.apps import AppConfig


class BookStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book_store"

    def ready(self):
        import book_store.signals
