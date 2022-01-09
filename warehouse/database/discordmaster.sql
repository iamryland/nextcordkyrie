CREATE TABLE IF NOT EXISTS "levels" (
	"id" INTEGER UNIQUE,
	"stat" INTEGER,
	"type" TEXT,
	"multi"	TEXT,
	"roles"	TEXT,
	"custom" TEXT,
	"exclude" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "config"("id")
);
CREATE TABLE IF NOT EXISTS "mod" (
	"id" INTEGER UNIQUE,
	"stat" INTEGER,
	"reports" TEXT,
	"mods" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "config"("id")
);
CREATE TABLE IF NOT EXISTS "modone" (
	"id" INTEGER UNIQUE,
	"stat" INTEGER,
	"json" TEXT,
	"filters" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "config"("id")
);
CREATE TABLE IF NOT EXISTS "config" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"announce" TEXT,
	"cmds" TEXT,
	PRIMARY KEY("id")
);
