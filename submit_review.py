import csv
import os
from playwright.sync_api import sync_playwright

CSV_PATH = "reviews.csv"

def get_next_review():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return None, None

    with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        for idx, row in enumerate(reader):
            if row.get("status", "").strip().lower() == "pending":
                return idx, row
    return None, None

def mark_completed(target_idx):
    rows = []
    with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for idx, row in enumerate(reader):
            if idx == target_idx:
                row["status"] = "completed"
            rows.append(row)

    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def run():
    idx, review = get_next_review()
    if review is None:
        print("No pending reviews found in reviews.csv.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"Opening: {review['product_url']}")
        page.goto(str(review["product_url"]), wait_until="domcontentloaded", timeout=60000)

        # 1. Wait for form
        page.locator("#commentform").wait_for(state="attached", timeout=15000)
        page.locator("#comment").scroll_into_view_if_needed()

        # 2. Select Star Rating
        star_val = int(review["rating"])
        star_selector = f"p.stars a.star-{star_val}"

        if page.locator(star_selector).count() > 0:
            page.locator(star_selector).click(force=True)

        page.evaluate(
            """([val]) => {
                const select = document.querySelector('#rating');
                if (select) {
                    select.value = val;
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""",
            [str(star_val)],
        )

        # 3. Fill Review Data
        page.fill("#comment", str(review["comment"]))
        page.fill("#author", str(review["username"]))
        page.fill("#email", str(review["email"]))

        # 4. Optional MailPoet Checkbox
        mailpoet_box = page.locator("#mailpoet_subscribe_on_comment")
        if mailpoet_box.count() > 0 and mailpoet_box.is_checked():
            mailpoet_box.uncheck()

        # 5. Submit Form
        page.locator("#submit").click()
        page.wait_for_timeout(4000)

        browser.close()

    mark_completed(idx)
    print(f"Successfully posted review for {review['product_url']} by {review['username']}")

if __name__ == "__main__":
    run()