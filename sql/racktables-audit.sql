-- mysql / mariadb
CREATE TABLE `AuditLog` (
  `id` int(11) NOT NULL,
  `object_id_audit` int(11) DEFAULT NULL,
  `chapter_id_audit` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Audit Object Creation, Update and Deletions.
CREATE TRIGGER `racktables`.`AuditLog_ObjectInsert`
AFTER INSERT ON `racktables`.`Object`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (NEW.id);
CREATE TRIGGER `racktables`.`AuditLog_ObjectDelete`
AFTER DELETE ON `racktables`.`Object`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (OLD.id);
CREATE TRIGGER `racktables`.`AuditLog_ObjectUpdate`
AFTER UPDATE ON `racktables`.`Object`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (NEW.id);
-- Audit Dictionary modifications.

CREATE TRIGGER `racktables`.`AuditLog_DictionaryInsert`
AFTER INSERT ON `racktables`.`Dictionary`
FOR EACH ROW
  INSERT INTO AuditLog (chapter_id_audit) VALUES (NEW.chapter_id);
CREATE TRIGGER `racktables`.`AuditLog_DictionaryDelete`
AFTER DELETE ON `racktables`.`Dictionary`
FOR EACH ROW
  INSERT INTO AuditLog (chapter_id_audit) VALUES (OLD.chapter_id);
CREATE TRIGGER `racktables`.`AuditLog_DictionaryUpdate`
AFTER UPDATE ON `racktables`.`Dictionary`
FOR EACH ROW
  INSERT INTO AuditLog (chapter_id_audit) VALUES (NEW.chapter_id);

-- Audit EntityLink
CREATE TRIGGER `racktables`.`AuditLog_EntityLink_Insert`
AFTER INSERT ON `racktables`.`EntityLink`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (NEW.parent_entity_id),(NEW.child_entity_id);

CREATE TRIGGER `racktables`.`AuditLog_EntityLink_Delete`
AFTER DELETE ON `racktables`.`EntityLink`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (OLD.parent_entity_id),(OLD.child_entity_id);

CREATE TRIGGER `racktables`.`AuditLog_EntityLink_Update`
AFTER UPDATE ON `racktables`.`EntityLink`
FOR EACH ROW
  INSERT INTO AuditLog (object_id_audit) VALUES (OLD.parent_entity_id),(OLD.child_entity_id),(NEW.parent_entity_id),(NEW.child_entity_id);
