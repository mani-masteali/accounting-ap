class Category:
    def __init__(self, file="categories.txt"):
        self.file = file
        self.categoriesList = self.load_categories(self)

    def load_categories(self):
        try:
            with open(self.file, mode='r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
