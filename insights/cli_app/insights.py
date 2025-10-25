
from datetime import datetime
from pathlib import Path
from tabulate import tabulate
import json

from order_pipeline.analyzer import ShoplinkAnalyzer

session_log = set()

def load_data(path="shoplink/sales_data/cleaned.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return []


def print_menu():
    print("\n📊 What insight would you like to explore?")
    print("[1] Best Selling Items")
    print("[2] Price Anomalies (>25% variance)")
    print("[3] Peak Sales Hours")
    print("[4] Money Tracker")
    print("[5] Daily Sales")
    print("[6] Item Frequency")
    print("[7] Refund Loss")
    print("[8] Conversion Rate")
    print("[9] Average Order Value")
    print("[10] High-Value Orders (₦100+)")
    print("[11] Payment Status Summary")
    print("[12] Exit")



def write_to_file(title: str, content: str):
    # Get the directory where insights.py lives
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "shoplink_insights.txt"

    # Create the file if it doesn't exist
    if not file_path.exists():
        file_path.touch()

    # Format the entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n{'='*60}\n🕒 {timestamp}\n📌 {title}\n{'='*60}\n"
    
    # Write to the file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(content)
        f.write("\n")



def run_insight(choice, records, analyzer):
    """ Execute the selected insight and display/save results. """
    
    if choice == "1":
        title = "Best Selling Items"
        if title not in session_log:
            session_log.add(title)
            top_items = analyzer.top_sellers(records, by="total", top_n=5)
            table = tabulate(top_items, headers="keys", tablefmt="fancy_grid")
            write_to_file(title, table)
        print("\n🏆 Best Selling Items")
        print(tabulate(analyzer.top_sellers(records, by="total", top_n=5), headers="keys", tablefmt="fancy_grid"))

    elif choice == "2":
        title = "Price Anomalies"
        anomalies = analyzer.detect_price_anomalies(records, threshold=0.25)
        table = tabulate(anomalies, headers="keys", tablefmt="fancy_grid") if anomalies else "No significant price anomalies found."
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n📉 Price Anomalies")
        print(table)

    elif choice == "3":
        title = "Peak Sales Hours"
        hourly = analyzer.sales_by_hour(records)
        rows = [{"Hour": f"{hour}:00", "Revenue": round(total, 2)} for hour, total in hourly.items()]
        table = tabulate(rows, headers="keys", tablefmt="fancy_grid")
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n⏰ Peak Sales Hours")
        print(table)

    elif choice == "4":
        title = "Money Tracker"
        refund = analyzer.refund_loss(records)
        conversion = analyzer.conversion_rate(records)
        avg_order = analyzer.average_order_value(records)
        status_summary = analyzer.aggregate_by_status(records)
        summary = (
            f"Total Refund Loss: ₦{refund}\n"
            f"Conversion Rate: {conversion}%\n"
            f"Average Order Value: ₦{avg_order}\n\n"
            + tabulate(status_summary, headers="keys", tablefmt="fancy_grid")
        )
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, summary)
        print("\n💸 Money Tracker")
        print(summary)

    elif choice == "5":
        title = "Daily Sales"
        daily = analyzer.sales_by_day(records)
        rows = [{"Date": day, "Revenue": round(total, 2)} for day, total in daily.items()]
        table = tabulate(rows, headers="keys", tablefmt="fancy_grid")
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n📅 Daily Sales")
        print(table)

    elif choice == "6":
        title = "Item Frequency"
        freq = analyzer.item_frequency(records)
        rows = [{"Item": item, "Count": count} for item, count in freq.items()]
        table = tabulate(rows, headers="keys", tablefmt="fancy_grid")
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n🔁 Item Frequency")
        print(table)

    elif choice == "7":
        title = "Refund Loss"
        loss = analyzer.refund_loss(records)
        summary = f"Total Refund Loss: ₦{loss}"
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, summary)
        print("\n💸 Refund Loss")
        print(summary)

    elif choice == "8":
        title = "Conversion Rate"
        rate = analyzer.conversion_rate(records)
        summary = f"Conversion Rate: {rate}%"
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, summary)
        print("\n📈 Conversion Rate")
        print(summary)

    elif choice == "9":
        title = "Average Order Value"
        avg = analyzer.average_order_value(records)
        summary = f"Average Order Value: ₦{avg}"
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, summary)
        print("\n💰 Average Order Value")
        print(summary)

    elif choice == "10":
        title = "High-Value Orders"
        high_orders = analyzer.high_value_orders(records, threshold=100.0)
        table = tabulate(high_orders, headers="keys", tablefmt="fancy_grid") if high_orders else "No high-value orders found."
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n💎 High-Value Orders (₦100+)")
        print(table)

    elif choice == "11":
        title = "Payment Status Summary"
        status_summary = analyzer.aggregate_by_status(records)
        table = tabulate(status_summary, headers="keys", tablefmt="fancy_grid")
        if title not in session_log:
            session_log.add(title)
            write_to_file(title, table)
        print("\n💳 Payment Status Summary")
        print(table)

    elif choice == "12":
        print("\n👋 Session ended. Your insights report has been saved to 'shoplink_insights.txt'.")
        return False


def main():
    print("📦 Welcome to Shoplink BI — your one-stop shop for business insights!")
    print("⚠️ Due to limitations, our system cannot show you visualizations right now, but our Engineering team is working on it!")

    records = load_data()
    if not records:
        print("No data available. Please check your input file.")
        return

    analyzer = ShoplinkAnalyzer()

    while True:
        print_menu()
        choice = input("\nEnter the number of the insight you want to view: ").strip()
        keep_running = run_insight(choice, records, analyzer)
        if not keep_running:
            break
        again = input("\nWould you like to view another insight? (y/n): ").strip().lower()
        if again != "y":
            print("\n👋 Thanks for using Shoplink BI. Goodbye!")
            break

if __name__ == "__main__":
    main()
