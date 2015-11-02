CREATE INDEX `filebrowser_filedescription_filepath` ON `filebrowser_filedescription` (`file_path`);
CREATE INDEX `productions_production_9246ed76` ON `productions_production` (`title`);
CREATE INDEX `productions_productioninvolvement_0f9f11fd` ON `productions_productioninvolvement` (`production_id`, `sort_order`);
CREATE INDEX `productions_eventinvolvement_a461fcb3` ON `productions_eventinvolvement` (`event_id`, `sort_order`);