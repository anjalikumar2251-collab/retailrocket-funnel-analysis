-- ================================
-- Retailrocket Funnel Analysis
-- SQL Queries by Anjali
-- ================================

-- 1. Total unique visitors
SELECT COUNT(DISTINCT visitorid) as total_visitors
FROM events;

-- 2. Unique visitors per event type
SELECT event, COUNT(DISTINCT visitorid) as total_visitors
FROM events
GROUP BY event
ORDER BY total_visitors DESC;

-- 3. Top 10 most viewed items
SELECT itemid, COUNT(*) as total_views
FROM events
WHERE event = 'view'
GROUP BY itemid
ORDER BY total_views DESC
LIMIT 10;

-- 4. Items added to cart but never purchased
SELECT DISTINCT itemid
FROM events
WHERE event = 'addtocart'
AND itemid NOT IN (
    SELECT itemid FROM events
    WHERE event = 'transaction'
)
LIMIT 10;

-- 5. Overall conversion rate
SELECT ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'transaction' 
THEN visitorid END) / COUNT(DISTINCT visitorid), 2) as conversion_rate
FROM events;

-- 6. Busiest hours of the day
SELECT STRFTIME('%H', DATETIME(timestamp/1000, 'unixepoch')) as hour,
COUNT(*) as total_events
FROM events
GROUP BY hour
ORDER BY total_events DESC
LIMIT 5;

-- 7. Full funnel conversion rates
SELECT
COUNT(DISTINCT CASE WHEN event = 'view' THEN visitorid END) as viewers,
COUNT(DISTINCT CASE WHEN event = 'addtocart' THEN visitorid END) as cart_adders,
COUNT(DISTINCT CASE WHEN event = 'transaction' THEN visitorid END) as buyers,
ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'addtocart' THEN visitorid END) / 
COUNT(DISTINCT CASE WHEN event = 'view' THEN visitorid END), 2) as view_to_cart_percent,
ROUND(100.0 * COUNT(DISTINCT CASE WHEN event = 'transaction' THEN visitorid END) / 
COUNT(DISTINCT CASE WHEN event = 'addtocart' THEN visitorid END), 2) as cart_to_purchase_percent
FROM events;

-- 8. Visitors who viewed but never purchased
SELECT COUNT(DISTINCT visitorid) as never_purchased
FROM events
WHERE event = 'view'
AND visitorid NOT IN (
    SELECT visitorid FROM events
    WHERE event = 'transaction'
);