"""Class for load testing N11 website with locust framework"""

import random
from locust import HttpUser, task, between

class N11SearchUser(HttpUser):
    # Wait time between tasks (simulates human thinking/scrolling)
    wait_time = between(1, 3)

    SEARCH_QUERIES = [
        "iphone",
        "samsung",
        "laptop",
        "macbook",
        "headphones",
        "tv",
        "playstation",
        "",
        "!!!@@@###",
    ]

    def on_start(self):
        """Executed when a user starts; good for landing on the homepage"""
        self.client.get("/")

    @task(5)
    def perform_search(self):
        """Simulates a user searching for a product and landing on the results page"""
        search_query = random.choice(self.SEARCH_QUERIES)
        self.client.get(url="/arama", params={"q": search_query}, name=f"first search of {search_query}")

    @task(5)
    def perform_search_by_popular(self):
        """Simulates a user searching for a popular product and landing on the results page"""
        self.client.get(url="/arama", params={"q": "valiz"}, name=f"first search of a popular product")

    @task(5)
    def perform_partly_search(self):
        """Simulates a user searching for a product by partly name and landing on the results page"""
        self.client.get(url="/arama", params={"q": "iph"}, name=f"Partly search")

    @task(4)
    def infinite_scroll_pagination(self):
        """Simulates the infinite scroll by requesting subsequent pages"""
        # We simulate loading page 2 and 3
        search_query = "iphone+16"
        for page in range(2, 4):
            self.client.get(f"/arama?q={search_query}&pg={page}", name=f"pagination with search {search_query}")

    @task(2)
    def apply_filters(self):
        """Simulates filtering by Brand, Model, and Capacity"""
        params = {
            "q": "iphone+16",
            "m": "Apple",
            "md": "Iphone%2013",
            "dahilihafiza": "128%20GB"
        }
        self.client.get(url="/arama", params=params, name="search with filltering")
    
    @task(2)
    def apply_filters_by_prise(self):
        """Simulates filtering by Brand, Model, and Capacity"""
        params = {
            "q": "iphone+16",
            "m": "Apple",
            "md": "Iphone%2013",
            "dahilihafiza": "128%20GB",
            "minp": 20000,
            "max": 40000
        }
        self.client.get(url="/arama", params=params, name="search with filltering by prise")
    
    @task(2)
    def apply_filters_by_prise_from(self):
        """Simulates filtering by Brand, Model, and Capacity"""
        params = {
            "q": "iphone+16",
            "m": "Apple",
            "md": "Iphone%2013",
            "dahilihafiza": "128%20GB",
            "minp": 20000
        }
        self.client.get(url="/arama", params=params, name="search with filltering by prise to")

    @task(2)
    def apply_filters_by_prise_to(self):
        """Simulates filtering by Brand, Model, and Capacity"""
        params = {
            "q": "iphone+16",
            "m": "Apple",
            "md": "Iphone%2013",
            "dahilihafiza": "128%20GB",
            "maxp": 40000
        }
        self.client.get(url="/arama", params=params, name="search with filltering by prise to")
