"""
Product Recommendation System

A console-based program that recommends products based on user search history
for different categories like clothes, mobile, toys, games, etc.
"""

from typing import Dict, List, Set
import random


class ProductRecommender:
    def __init__(self):
        # Product database organized by categories
        self.products = {
            "clothes": {
                "casual": ["T-Shirt", "Jeans", "Sneakers", "Hoodie", "Sweatpants"],
                "formal": ["Suit", "Dress Shirt", "Tie", "Dress Shoes", "Blazer"],
                "sports": ["Sports Jersey", "Athletic Shorts", "Running Shoes", "Sports Bra", "Track Pants"],
                "winter": ["Winter Jacket", "Sweater", "Scarf", "Gloves", "Boots"]
            },
            "mobile": {
                "smartphones": ["iPhone 15", "Samsung Galaxy S24", "Google Pixel 8", "OnePlus 12", "Xiaomi 14"],
                "accessories": ["Phone Case", "Screen Protector", "Wireless Charger", "Power Bank", "Bluetooth Headphones"],
                "tablets": ["iPad Pro", "Samsung Galaxy Tab", "Amazon Fire Tablet", "Lenovo Tab", "Microsoft Surface"]
            },
            "toys": {
                "educational": ["Building Blocks", "Puzzle Set", "Science Kit", "Art Supplies", "Learning Tablet"],
                "action": ["Action Figures", "Remote Control Car", "Drones", "Nerf Guns", "Robot Toys"],
                "board_games": ["Chess", "Monopoly", "Scrabble", "Risk", "Catan"],
                "outdoor": ["Bicycle", "Scooter", "Trampoline", "Swimming Pool", "Tennis Racket"]
            },
            "games": {
                "pc_games": ["Cyberpunk 2077", "Elden Ring", "Red Dead Redemption 2", "The Witcher 3", "GTA V"],
                "console_games": ["God of War", "Spider-Man", "Zelda: Tears of Kingdom", "Mario Kart", "FIFA 24"],
                "mobile_games": ["PUBG Mobile", "Candy Crush", "Among Us", "Clash of Clans", "Pokemon Go"]
            },
            "electronics": {
                "laptops": ["MacBook Pro", "Dell XPS", "HP Spectre", "Lenovo ThinkPad", "ASUS ROG"],
                "gaming": ["Gaming Mouse", "Mechanical Keyboard", "Gaming Headset", "Graphics Card", "Gaming Monitor"],
                "home": ["Smart TV", "Bluetooth Speaker", "Smart Bulbs", "Security Camera", "Robot Vacuum"]
            },
            "books": {
                "fiction": ["The Great Gatsby", "1984", "To Kill a Mockingbird", "Pride and Prejudice", "The Hobbit"],
                "non_fiction": ["Sapiens", "Atomic Habits", "Rich Dad Poor Dad", "The Power of Now", "Thinking Fast and Slow"],
                "self_help": ["The 7 Habits", "How to Win Friends", "The Secret", "Mindset", "Deep Work"]
            }
        }
        
        # User search history
        self.user_history: List[str] = []
        
        # Category mappings for better search
        self.category_mappings = {
            "clothes": ["clothes", "clothing", "apparel", "fashion", "wear", "dress"],
            "mobile": ["mobile", "phone", "smartphone", "cellphone", "telephone"],
            "toys": ["toys", "toy", "play", "children", "kids"],
            "games": ["games", "game", "gaming", "play", "entertainment"],
            "electronics": ["electronics", "electronic", "tech", "technology", "gadgets"],
            "books": ["books", "book", "reading", "literature", "novel"]
        }

    def add_to_history(self, search_term: str) -> None:
        """Add search term to user history."""
        self.user_history.append(search_term.lower())

    def get_category_from_search(self, search_term: str) -> str:
        """Determine category from search term."""
        search_lower = search_term.lower()
        
        for category, keywords in self.category_mappings.items():
            if any(keyword in search_lower for keyword in keywords):
                return category
        
        return "general"

    def get_recommendations(self, search_term: str, num_recommendations: int = 3) -> List[str]:
        """Get product recommendations based on search term and user history."""
        category = self.get_category_from_search(search_term)
        recommendations = []
        
        # Get products from the category
        if category in self.products:
            category_products = self.products[category]
            
            # Flatten all subcategories
            all_products = []
            for subcategory, products in category_products.items():
                all_products.extend(products)
            
            # Add category products to recommendations
            recommendations.extend(random.sample(all_products, min(num_recommendations, len(all_products))))
        
         # Add recommendations based on user history
        if self.user_history:
            history_recommendations = self.get_history_based_recommendations(num_recommendations)
            recommendations.extend(history_recommendations)
        
        # Remove duplicates and limit to requested number
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:num_recommendations]

    def get_history_based_recommendations(self, num_recommendations: int = 2) -> List[str]:
        """Get recommendations based on user search history."""
        history_recommendations = []
        
        # Look at recent searches (last 3)
        recent_searches = self.user_history[-3:]
        
        for search in recent_searches:
            category = self.get_category_from_search(search)
            if category in self.products:
                category_products = self.products[category]
                
                # Get products from random subcategory
                subcategories = list(category_products.keys())
                if subcategories:
                    random_subcategory = random.choice(subcategories)
                    products = category_products[random_subcategory]
                    if products:
                        history_recommendations.append(random.choice(products))
        
        return history_recommendations

    def display_categories(self) -> None:
        """Display available product categories."""
        print("\n=== Available Categories ===")
        for i, category in enumerate(self.products.keys(), 1):
            print(f"{i}. {category.title()}")
        print()

    def display_user_history(self) -> None:
        """Display user search history."""
        if self.user_history:
            print("\n=== Your Search History ===")
            for i, search in enumerate(self.user_history, 1):
                print(f"{i}. {search}")
        else:
            print("\nNo search history yet.")
        print()


def main():
    """Main program function."""
    recommender = ProductRecommender()
    
    print("=== Product Recommendation System ===")
    print("Search for products and get personalized recommendations!")
    print("Type 'quit' to exit, 'history' to see your search history, 'categories' to see available categories")
    print()
    
    while True:
        try:
            # Get user input
            search_term = input("What are you looking for? ").strip()
            
            if not search_term:
                continue
                
            if search_term.lower() == 'quit':
                print("Thank you for using the Product Recommendation System!")
                break
                
            if search_term.lower() == 'history':
                recommender.display_user_history()
                continue
                
            if search_term.lower() == 'categories':
                recommender.display_categories()
                continue
            
            # Add to history and get recommendations
            recommender.add_to_history(search_term)
            recommendations = recommender.get_recommendations(search_term, 5)
            
            # Display recommendations
            print(f"\n=== Recommendations for '{search_term}' ===")
            if recommendations:
                for i, product in enumerate(recommendations, 1):
                    print(f"{i}. {product}")
            else:
                print("No specific recommendations found. Try searching for a different category.")
            print()
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()






