ALTER TABLE system_contextitem ADD FULLTEXT INDEX `full_text` (additional_search_data, title_en, description_en, title_de, description_de);
