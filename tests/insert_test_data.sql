-- Temporarily disable foreign key checks to allow test data insertion
SET FOREIGN_KEY_CHECKS = 0;

-- RENTAL
INSERT IGNORE INTO rental (rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
VALUES 
  (9991, '2099-01-01 10:00:00', 1, 1, NULL, 1, NOW()), -- NULL return_date
  (9992, '2006-06-01 10:00:00', 2, 2, '2099-12-31 00:00:00', 1, NOW()); -- far future return_date

-- PAYMENT
INSERT IGNORE INTO payment (payment_id, customer_id, staff_id, rental_id, amount, payment_date, last_update)
VALUES 
  (9991, 1, 1, 9991, 5.99, NOW(), NOW()),  -- valid
  (9992, 2, 1, 9992, NULL, NOW(), NOW());  -- NULL amount (should be handled or cleaned)

-- STAFF
INSERT IGNORE INTO staff (staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture)
VALUES 
  (999, 'Null', NULL, 1, NULL, 1, 1, 'user999', 'pass', NOW(), NULL);

-- STORE
INSERT IGNORE INTO store (store_id, manager_staff_id, address_id, last_update)
VALUES 
  (999, 999, 1, NOW());

-- CUSTOMER
INSERT IGNORE INTO customer (customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update)
VALUES 
  (999, 1, 'Test', NULL, NULL, 1, 1, NOW(), NOW());

-- ADDRESS
INSERT IGNORE INTO address (
  address_id, address, address2, district, city_id, postal_code, phone, last_update, location
)
VALUES (
  999, 'Test St', '', 'Test District', 1, '12345', '000-000-0000', NOW(), ST_GeomFromText('POINT(0 0)')
);

-- FILM
INSERT IGNORE INTO film (film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, special_features, last_update)
VALUES 
  (999, 'Test Film', NULL, 2025, 1, 5, 2.99, 90, 10.0, 'G', 'Trailers', NOW());

-- LANGUAGE
INSERT IGNORE INTO language (language_id, name, last_update)
VALUES 
  (99, , NOW());

-- CATEGORY
INSERT IGNORE INTO category (category_id, name, last_update)
VALUES 
  (99, 'Experimental', NOW());

-- FILM_CATEGORY
INSERT IGNORE INTO film_category (film_id, category_id, last_update)
VALUES 
  (999, 99, NOW());

-- INVENTORY
INSERT IGNORE INTO inventory (inventory_id, film_id, store_id, last_update)
VALUES 
  (999, 999, 999, NOW());

SET FOREIGN_KEY_CHECKS = 1;
