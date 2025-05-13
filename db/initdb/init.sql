-- db/initdb/init.sql

-- Создаём таблицу products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    price NUMERIC(10,2)
);

-- Вставляем ваши тестовые данные
INSERT INTO products (name, category, price) VALUES
  ('Agro Greenhouse', 'agro_industry_and_commerce', 309.90),
  ('Agro Irrigation', 'agro_industry_and_commerce', 159.00),
  ('Agro Silo', 'agro_industry_and_commerce', 49.99),
  ('Compost Crop', 'agro_industry_and_commerce', 189.00),
  ('Compost Fertilizer', 'agro_industry_and_commerce', 28.45),
  ('Compost Sprayer', 'agro_industry_and_commerce', 31.00),
  ('Compost Tractor', 'agro_industry_and_commerce', 18.60);
