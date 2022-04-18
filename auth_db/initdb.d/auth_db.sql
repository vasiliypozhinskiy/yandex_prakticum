--
-- Create model Role
--
CREATE TABLE "roles"
(
    "title" varchar(50) NOT NULL PRIMARY KEY
);
--
-- Create model User
--
CREATE TABLE "users"
(
    "password"    varchar(128)             NOT NULL,
    "last_login"  timestamp with time zone NULL,
    "id"          uuid                     NOT NULL PRIMARY KEY,
    "login"       varchar(100)             NOT NULL UNIQUE,
    "email"       varchar(254)             NOT NULL UNIQUE,
    "first_name"  varchar(100)             NULL,
    "middle_name" varchar(100)             NULL,
    "last_name"   varchar(100)             NULL
);
--
-- Create model UserRole
--
CREATE TABLE "users_roles"
(
    "id"      uuid        NOT NULL PRIMARY KEY,
    "role_id" varchar(50) NOT NULL,
    "user_id" uuid        NOT NULL
);
--
-- Add field roles to user
--
--
-- Create model LoginHistory
--
CREATE TABLE "login_history"
(
    "id"         uuid                     NOT NULL PRIMARY KEY,
    "user_agent" varchar(150)             NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "user_id"    uuid                     NOT NULL
);
CREATE INDEX "roles_title_c2f44585_like" ON "roles" ("title" varchar_pattern_ops);
CREATE INDEX "users_login_3b007138_like" ON "users" ("login" varchar_pattern_ops);
CREATE INDEX "users_email_0ea73cca_like" ON "users" ("email" varchar_pattern_ops);

ALTER TABLE "users_roles"
    ADD CONSTRAINT "users_roles_role_id_fe00bf26_fk_roles_title" FOREIGN KEY ("role_id") REFERENCES "roles" ("title") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "users_roles"
    ADD CONSTRAINT "users_roles_user_id_a7500f73_fk_users_id" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "users_roles_role_id_fe00bf26" ON "users_roles" ("role_id");
CREATE INDEX "users_roles_role_id_fe00bf26_like" ON "users_roles" ("role_id" varchar_pattern_ops);
CREATE INDEX "users_roles_user_id_a7500f73" ON "users_roles" ("user_id");

ALTER TABLE "login_history"
    ADD CONSTRAINT "login_history_user_id_0eeaebb8_fk_users_id" FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "login_history_user_id_0eeaebb8" ON "login_history" ("user_id");
