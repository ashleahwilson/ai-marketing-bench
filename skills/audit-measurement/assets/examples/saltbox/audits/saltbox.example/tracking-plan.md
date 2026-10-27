# Tracking plan: Saltbox Coffee Roasters
2026-10-22 · Analytics: GA4 through GTM-SB31KQ · Ad tags: Meta Pixel 290018833471652 · Status key: keep / fix / new

| Event | Fires when | Where | Parameters | Conversion? | Sent to | Status |
|---|---|---|---|---|---|---|
| purchase | The order confirmation page loads | order-confirmed.html (data layer push) | transaction_id, value, currency | Yes (key event) | GA4, Meta (Purchase) | fix: remove customer_email |
| sign_up | The /subscribed page loads after the newsletter form posts | /subscribed (new page) | method | Yes (key event) | GA4 | new |
| add_to_cart | The Add to cart button succeeds | product.html, after the cart updates | item_id, value, currency | No | GA4, Meta (AddToCart) | new |
| begin_checkout | The checkout page loads | /checkout | value, currency | No | GA4 | new |

Naming: the analytics tool's recommended event names, lowercase with underscores.
Parameters never include email, name, phone, address or free-text form contents.
Campaign links: utm_source, utm_medium, utm_campaign in lowercase; never on internal links.
Meta events fire only after marketing consent.
Verify: place a test order and subscribe once; each event should appear exactly once in GA4 DebugView and Meta's test events.
