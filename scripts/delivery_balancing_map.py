import pandas as pd

def map_delivery_to_ba_and_queue(path_delivery, path_ba):
    print(f"🔍 Mapping delivery companies and BAs...")
    delivery = pd.read_excel(path_delivery)
    ba = pd.read_excel(path_ba)
    print("📊 Sample delivery:\n", delivery.head(2))
    print("📊 Sample balancing authorities:\n", ba.head(2))
    # TODO: Join or spatial match utilities to BAs
    # TODO: Create mapping dictionary for queue resolution

if __name__ == "__main__":
    map_delivery_to_ba_and_queue("data/Delivery_Companies_2023.xlsx", "data/Balancing_Authority_2023.xlsx")
